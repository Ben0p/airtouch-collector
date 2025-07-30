from services.envservice import ENV



def ac_point(ac_data):
    return {
            "measurement": "ac",
            "tags": {
                "name" : ac_data['name'],
                "ip" : ENV.AIRTOUCH_IP
            },
            "fields": {
                "current_temperature" : ac_data['current_temperature'],
                "target_temperature" : ac_data['target_temperature'],
                "active_fan_speed" : ac_data['active_fan_speed'],
                "active_mode" : ac_data['active_mode'],
                "error_info" : ac_data['error_info'],
                "max_target_temperature" : ac_data['max_target_temperature'],
                "min_target_temperature" : ac_data['min_target_temperature'],
                "power_state" : ac_data['power_state'],
                "selected_fan_speed" : ac_data['selected_fan_speed'],
                "selected_mode" : ac_data['selected_mode'],
                "spill_state" : ac_data['spill_state']
            }
        }


def zones_points(zones):
    return [
        {
            "measurement": "zones",
            "tags": {
                "name" : zone['name'],
                "zone_id" : zone["zone_id"]
            },
            "fields": {
                "control_method" : zone['control_method'],
                "has_temp_sensor" : zone['has_temp_sensor'],
                "current_temperature" : zone['current_temperature'],
                "current_damper_percentage" : zone['current_damper_percentage'],
                "power_state" : zone['power_state'],
                "sensor_battery_status" : zone['sensor_battery_status'],
                "spill_active" : zone['spill_active'],
                "target_temperature" : zone['target_temperature']
            }
        }
    for zone in zones]