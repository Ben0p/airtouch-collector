import asyncio

import pyairtouch

from typing import cast


async def main() -> None:
    # Automatically discover AirTouch devices on the network.
    discovered_airtouches = await pyairtouch.discover("10.0.11.147")
    if not discovered_airtouches:
        print("No AirTouch discovered")
        return

    for airtouch in discovered_airtouches:
        print(f"Discovered: {airtouch.name} ({airtouch.host})")

    # In this example we use the first discovered AirTouch (typically there is only one per network)
    airtouch = discovered_airtouches[0]

    # Connect to the AirTouch and read initial state.
    success = await airtouch.init()

    async def _on_ac_status_updated(ac_id: int) -> None:
        aircon: pyairtouch.AirConditioner = airtouch.air_conditioners[ac_id]
        print(f"{aircon.current_temperature=}")
        print(f"{aircon.target_temperature=}")
        airspeed_name: pyairtouch.AcFanSpeed = aircon.active_fan_speed.name # type: ignore
        print(f"{aircon.active_fan_speed.name=}") # type: ignore
        print(f"{aircon.active_fan_speed.value=}") # type: ignore
        print(f"{aircon.active_fan_speed=}")
        print(f"{aircon.active_mode=}")
        print(f"{aircon.active_mode.name=}") # type: ignore
        print(f"{aircon.error_info=}") 
        print(f"{aircon.max_target_temperature=}")
        print(f"{aircon.min_target_temperature=}")
        print(f"{aircon.name=}")
        print(f"{aircon.power_state=}")
        print(f"{aircon.power_state.name=}") # type: ignore
        print(f"{aircon.selected_fan_speed=}")
        print(f"{aircon.selected_fan_speed.name=}") # type: ignore
        print(f"{aircon.selected_mode=}")
        print(f"{aircon.selected_mode.name=}") # type: ignore
        print(f"{aircon.spill_state=}")
        print(f"{aircon.spill_state.name=}")
        for zone in aircon.zones:
            print("-"*50)
            print(f"{zone.name=}")
            print(f"{zone.control_method=}")
            print(f"{zone.has_temp_sensor=}")
            print(f"{zone.current_temperature=}")
            print(f"{zone.current_damper_percentage=}")
            print(f"{zone.power_state=}")
            print(f"{zone.sensor_battery_status=}")
            print(f"{zone.spill_active=}")
            print(f"{zone.target_temperature=}")
            print(f"{zone.zone_id=}")
        # print(
        #     f"AC Status  : {aircon.power_state.name} {aircon.mode.name}  "
        #     f"temp={aircon.current_temperature:.1f} set_point={aircon.target_temperature:.1f}"
        # )

        # for zone in aircon.zones:
        #     print(
        #         f"Zone Status: {zone.name:10} {zone.power_state.name:3}  "
        #         f"temp={zone.current_temperature:.1f} set_point={zone.target_temperature:.1f} "
        #         f"damper={zone.current_damper_percentage}"
        #     )

    # Subscribe to AC status updates:
    for aircon in airtouch.air_conditioners:
        aircon.subscribe(_on_ac_status_updated)

        # Print initial status
        await _on_ac_status_updated(aircon.ac_id)

    # Keep the demo running for a few minutes
    await asyncio.sleep(300)

    # Shutdown the connection
    await airtouch.shutdown()


if __name__ == "__main__":
    asyncio.run(main())