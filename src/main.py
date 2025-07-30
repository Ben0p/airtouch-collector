from services.envservice import ENV
from services.fluxservice import flux
from services.airservice import Air
from services import pointservice
import pyairtouch
import asyncio



'''
Main entrypoint module to collect AirTouch device metrics and write to InfluxDB
'''



async def main():
    '''
    Main entrypoint loop
    '''

    # Connect Influx
    flux.connect()
    # Init air
    air = Air()
    await air.setup()
    # Loop
    while True:
        points = []
        ac_data = air.get_aircon_data()
        if ac_data:
            print(f"Retrieved AC data")
            points.append(pointservice.ac_point(ac_data))

        zones_data = air.get_zones_data()
        if zones_data:
            print(f"Retrieved zones data")
            points.extend(pointservice.zones_points(zones_data))

        if points:
            try:
                flux.write_points(points)
                print(f"Wrote {len(points)} points to InfluxDB")
            except RuntimeError:
                print("Error writing points to InfluxDB")
        
        await asyncio.sleep(int(ENV.INTERVAL_SECONDS))

if __name__ == "__main__":
    asyncio.run(main())