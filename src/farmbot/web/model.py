from datetime import datetime


class SensorReading(object):
    def __init__(self, data):
        self._data = data
        self._created = datetime.strptime(self._data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')

    @property
    def value(self):
        return self._data['value']

    @property
    def location(self):
        return self._data['x'], self._data['y'], self._data['z']

    @property
    def created(self):
        return self._created

    def __lt__(self, other):
        return self.created < other.created

    def __str__(self):
        return f"SensorReading({self._data})"


class Sensor(object):
    def __init__(self, data):
        self._data = data
        self._readings = []

    @property
    def id(self):
        return self._data['id']

    @property
    def label(self):
        return self._data['label']

    @property
    def pin(self):
        return self._data['pin']

    @property
    def readings(self):
        return self._readings

    def add_readings(self, readings):
        self._readings.extend([SensorReading(reading) for reading in readings if reading['pin'] == self.pin])
        self._readings = sorted(self._readings)

    def __str__(self):
        return f"Sensor({self._data}, {[str(reading) for reading in self._readings]})"
