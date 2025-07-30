from dotenv import load_dotenv
import os



'''
Service to load environment variables and do basic checks
'''



class Environment():
    def __init__(self):
        load_dotenv()
        self.AIRTOUCH_IP: str | None = os.getenv("AIRTOUCH_IP")
        self.INFLUXDB_URL: str | None = os.getenv("INFLUXDB_URL")
        self.INFLUXDB_TOKEN: str | None = os.getenv("INFLUXDB_TOKEN")
        self.INFLUXDB_ORG: str | None = os.getenv("INFLUXDB_ORG")
        self.INFLUXDB_BUCKET: str | None = os.getenv("INFLUXDB_BUCKET")
        self.INTERVAL_SECONDS: int | None = os.getenv("INTERVAL_SECONDS", "10")
        self.check()        

    def check(self):
        missing_vars = []
        for var_name, value in vars(self).items():
            if value is None or value.strip() == "":
                missing_vars.append(var_name)
        
        if missing_vars:
            raise ValueError(f"Missing or empty environment variables: {', '.join(missing_vars)}")
        


ENV = Environment()