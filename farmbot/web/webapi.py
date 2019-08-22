import json
from urllib.request import Request, urlopen
from farmbot.config import FarmBotConfiguration
from pprint import pprint
from farmbot.web.model import Sensor


class WebAPI(object):
    def __init__(self, config: FarmBotConfiguration):
        self.cfg = config

    def _headers(self):
        return {'Authorization': f'access_token {self.cfg.token}'}

    def _get(self, request_type):
        req = Request(f"https://my.farm.bot/api/{request_type}",
                      headers=self._headers())
        with urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def _post(self, request_type, post_data):
        req = Request(f"https://my.farm.bot/api/{request_type}",
                      data=json.dumps(post_data).encode('UTF-8'),
                      headers=self._headers())
        with urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))

    @property
    def plants(self):
        return self._post("points/search", {"pointer_type": "Plant"})

    @property
    def tool_slots(self):
        return self._post("points/search", {"pointer_type": "ToolSlot"})

    @property
    def sensor_readings(self):
        return self._get("sensor_readings")

    @property
    def sensors(self):
        return self._get("sensors")

    @property
    def farm_events(self):
        return self._get("farm_events")

    @property
    def farmware_envs(self):
        return self._get("farmware_envs")

    @property
    def images(self):
        return self._get("images")

    @property
    def logs(self):
        return self._get("logs")

    @property
    def peripherals(self):
        return self._get("peripherals")

    @property
    def pin_bindings(self):
        return self._get("pin_bindings")

    @property
    def plant_templates(self):
        return self._get("plant_templates")

    @property
    def points(self):
        return self._get("points")

    @property
    def sequences(self):
        return self._get("sequences")

    @property
    def tools(self):
        return self._get("tools")

    @property
    def users(self):
        return self._get("users")

    @property
    def device(self):
        return self._get(f"device/{self.cfg.device_id}")


if __name__ == '__main__':
    api = WebAPI(FarmBotConfiguration('./config.json'))
    print("\nDevice\n")
    pprint(api.device)
    print("\nPlants\n")
    pprint(api.plants)
    print("\nSensors\n")
    pprint(api.sensors)
    sensors = [Sensor(item) for item in api.sensors]
    print("\nSensor readings\n")
    pprint(api.sensor_readings)
    readings = api.sensor_readings
    for sensor in sensors:
        sensor.add_readings(readings)
    print("\nSensor objects\n")
    for sensor in sensors:
        pprint(str(sensor))


