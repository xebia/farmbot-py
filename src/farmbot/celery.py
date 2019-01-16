import json
import uuid
from enum import Enum


def coordinate(coords):
    x, y, z = coords
    return {'kind': 'coordinate', 'args': {'x': x, 'y': y, 'z': z}}


class CeleryNode(object):
    def __init__(self, kind, args, body=None, comment=None):
        self._node = dict()
        self._node['kind'] = kind
        self._node['args'] = args
        self.add_to_body(body)
        if comment:
            self._node['comment'] = comment

    def add_to_body(self, item):
        if item:
            if not self.body:
                self._node['body'] = list()
            self._node['body'].append(item)

    def as_node(self):
        return self._node

    @property
    def kind(self):
        return self._node['kind']

    @property
    def args(self):
        return self._node['args']

    @property
    def body(self):
        return self._node.get('body', None)

    @property
    def comment(self):
        return self._node.get('comment', None)

    def __eq__(self, other):
        """Don't care about the comments."""
        return (self.kind == other.kind) and (self.args == other.args) and (self.body == other.body)

    def __str__(self):
        body_str = f", {str(self.body)}" if self.body else ""
        comment_str = f", {str(self.comment)}" if self.comment else ""
        return "{}('{}', {}{}{})".format(self.__class__.__name__, self.kind, self.args, body_str, comment_str)


class MoveAbsolute(CeleryNode):
    def __init__(self, location, offset=(0, 0, 0), speed=100):
        super().__init__('move_absolute',
                         {'location': coordinate(location),
                          'offset': coordinate(offset),
                          'speed': speed})


class MoveRelative(CeleryNode):
    def __init__(self, x=0, y=0, z=0, speed=100):
        super().__init__('move_relative', {'x': x, 'y': y, 'z': z, 'speed': speed})


class GoHome(CeleryNode):
    def __init__(self, axis, speed=100):
        if isinstance(axis, Enum):
            axis = axis.value
        assert axis in ('x', 'y', 'z', 'all')
        super().__init__('find_home', {'speed': speed, 'axis': axis})


class ExecuteSequenceID(CeleryNode):
    def __init__(self, sequence_id):
        super().__init__('execute', {'sequence_id': sequence_id})


class WritePin(CeleryNode):
    def __init__(self, pin_nr: int, value, mode=0):
        assert type(pin_nr) is int
        super().__init__('write_pin', {'pin_number': pin_nr, 'pin_value': value, 'pin_mode': mode})


class ReadPin(CeleryNode):
    def __init__(self, pin_nr: int, mode=0):
        assert type(pin_nr) is int
        super().__init__('read_pin', {'pin_number': pin_nr, 'label': "---", 'pin_mode': mode})


class TakePhoto(CeleryNode):
    def __init__(self):
        super().__init__('take_photo', {})


class DumpInfo(CeleryNode):
    def __init__(self):
        super().__init__('dump_info', {})


class ReadStatus(CeleryNode):
    def __init__(self):
        super().__init__('read_status', {})


class Calibrate(CeleryNode):
    def __init__(self, axis):
        if isinstance(axis, Enum):
            axis = axis.value
        assert axis in ('x', 'y', 'z', 'all')
        super().__init__('calibrate', {'axis': axis})


class RPCRequest(CeleryNode):
    """Translates a FarmBot command to the corresponding CeleryScript RPC request."""

    def __init__(self, command: CeleryNode):
        self._uuid = str(uuid.uuid4())
        self.command = command
        super().__init__('rpc_request', {'label': self._uuid})
        self.add_to_body(command.as_node())

    def to_json(self):
        return json.dumps(self.as_node())

    @property
    def uuid(self):
        return self._uuid

    @property
    def kind(self):
        return self.command.kind

    @property
    def args(self):
        return self.command.args

    def __copy__(self):
        return RPCRequest(self.command)

    def __equals__(self, other):
        return self.uuid == other.uuid

    def is_same(self, other):
        """Requests are the same if their contents are the same, uuid may differ."""
        return self.command == other.command

    def __str__(self):
        return f"RPCRequest({self.command})"
