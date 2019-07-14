import json


class FarmBotStatus(object):
    def __init__(self, status_json):
        self.data = json.loads(status_json)

    @property
    def location(self):
        loc = self.data['location_data']['position']
        return loc['x'], loc['y'], loc['z']

    def pin(self, nr):
        return self.data['pins'][str(nr)]['value']


if __name__ == '__main__':
    with open("./status.json") as f:
        status = FarmBotStatus(f.read())
    print(status.location)
    print(status.pin(8))
