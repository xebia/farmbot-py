from farmbot.config import FarmBotConfiguration
from farmbot.connection import FarmBotConnection
from farmbot.celery import RPCRequest
import logging

logger = logging.getLogger(__name__)


class MockFarmBotConnection(FarmBotConnection):
    def __init__(self, config: FarmBotConfiguration):
        self.cfg = config

    @property
    def tool_mounted(self):
        return self._tool_mounted

    def send_command(self, rpc_request, wait_time=0):
        logger.debug(f"Sent command {rpc_request.to_json()}")

    def start(self):
        pass

    def stop(self):
        pass


class MockReplayFarmBotConnection(MockFarmBotConnection):
    def __init__(self, config: FarmBotConfiguration):
        super().__init__(config)
        self.expected_commands = list()

    def add_expected_command(self, command):
        self.expected_commands.append(RPCRequest(command))

    @property
    def commands_empty(self):
        return len(self.expected_commands) == 0

    def send_command(self, rpc_request, wait_time=10):
        assert len(self.expected_commands) > 0, f"Did not expect command {rpc_request}"
        assert self.expected_commands[0].is_same(
            rpc_request), f"\nExpected: {self.expected_commands[0]}\nActual:   {rpc_request}"
        self.expected_commands.pop(0)
