This Farmbot client is made to allow synchronous programming against the Farmbot MQTT API.
It currently only implements commands that are useful to run your own sequences.

The current implementation expects an `rpc_ok` return message with the same uuid as the command message. If this message is not sent this client will block indefinitely. It's known that there are some commands where there is no `rpc_ok` return message, so that still needs to be fixed.

## Installation

This code will not run on Python 2.

This code depends on the `paho-mqtt` and `request` libraries (`pip install`...).


You will need to add your own `config.py` with:

```
my_device_id = "device_\<your device number>"
my_token = "\<your encoded token>"
```

## Basic usage

This code will turn pin 7 to 1 and 0 four times. An initial call to `bot.start()` is possible but not needed, this will be called lazily before the first command is executed.

```
bot = FarmBot(FarmBotConnection(my_device_id, my_token, "brisk-bear.rmq.cloudamqp.com"))
try:
    for i in range(4):
        bot.write_pin(7, 1)
        bot.write_pin(7, 0)
    # ...any code you want.
finally:
    bot.stop()
```

See the `FarmBot` class to see all implemented commands.

## The listener

The farmbot_listener can be used to monitor all messages, you can run it independently.

## Testing

Run unittests with `python -m unittest discover -v -s ./test -t .` from the project root