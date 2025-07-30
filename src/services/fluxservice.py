from services.envservice import ENV
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS



'''
Flux service class to handle the InfluxDB connection and writes
'''



class Flux:
    def __init__(self):
        self.connect()


    def connect(self) -> None:
        try:
            self.client = InfluxDBClient(
                url=str(ENV.INFLUXDB_URL),
                token=str(ENV.INFLUXDB_TOKEN),
                org=str(ENV.INFLUXDB_ORG)
            )
            self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        except Exception as e:
            raise ConnectionError(f"Failed to connect to InfluxDB: {e}")


    def check_health(self):
        try:
            health = self.client.health()
            if health.status != "pass":
                raise ConnectionError(f"InfluxDB health check failed: {health.message}")
        except Exception as e:
            raise ConnectionError(f"Error during InfluxDB health check: {e}")


    def write_points(self, points: Point):
        try:
            self.write_api.write(bucket=str(ENV.INFLUXDB_BUCKET), org=str(ENV.INFLUXDB_ORG), record=points)
        except Exception as e:
            raise RuntimeError(f"Failed to write point to InfluxDB: {e}")


flux = Flux()