from services.envservice import ENV
import asyncio
import pyairtouch


class Air:
    def __init__(self):
        self.discovered: bool = False
        self.aircon_data: dict = {}  # Latest air conditioner properties
        self.zones_data: list = []   # Latest zones properties

    async def setup(self):
        discovered_airtouches = await pyairtouch.discover(ENV.AIRTOUCH_IP)
        if not discovered_airtouches:
            self.discovered = False
            print("No AirTouch discovered")
        else:
            self.discovered = True
            print("Found the AirTouch")
            self.ac = discovered_airtouches[0]
            await self.ac.init()
            self._subscribe_to_updates()
            # Manually trigger an update so the initial state is captured
            await self._initial_update()

    def _subscribe_to_updates(self):
        # Subscribe each air conditioner to status updates
        for aircon in self.ac.air_conditioners:
            aircon.subscribe(self._on_ac_status_updated)

    async def _on_ac_status_updated(self, ac_id: int) -> None:
        aircon: pyairtouch.AirConditioner = self.ac.air_conditioners[ac_id]
        self.aircon_data = {
            "current_temperature": aircon.current_temperature,
            "target_temperature": aircon.target_temperature,
            "active_fan_speed": aircon.active_fan_speed.name,
            "active_mode": aircon.active_mode.name,
            "error_info": aircon.error_info,
            "max_target_temperature": aircon.max_target_temperature,
            "min_target_temperature": aircon.min_target_temperature,
            "name": aircon.name,
            "power_state": aircon.power_state.name,
            "selected_fan_speed": aircon.selected_fan_speed.name,
            "selected_mode": aircon.selected_mode.name,
            "spill_state": aircon.spill_state.name,
        }
        self.zones_data = [
            {
                "name": zone.name,
                "control_method": zone.control_method.name,
                "has_temp_sensor": zone.has_temp_sensor,
                "current_temperature": zone.current_temperature,
                "current_damper_percentage": zone.current_damper_percentage,
                "power_state": zone.power_state.name,
                "sensor_battery_status": zone.sensor_battery_status.name,
                "spill_active": zone.spill_active,
                "target_temperature": zone.target_temperature,
                "zone_id": zone.zone_id,
            }
            for zone in aircon.zones
        ]

    async def _initial_update(self):
        # Force an update on each air conditioner after initialization so that
        # the initial state is captured.
        for aircon in self.ac.air_conditioners:
            await self._on_ac_status_updated(aircon.ac_id)

    def get_aircon_data(self):
        """Retrieve the latest air conditioner data."""
        return self.aircon_data

    def get_zones_data(self):
        """Retrieve the latest zones data."""
        return self.zones_data