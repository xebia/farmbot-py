This Farmbot client is made to allow synchronous programming against the Farmbot MQTT API.
It currently only implements commands that are useful to run your own sequences.

The current implementation expects an `rpc_ok` return message with the same uuid as the command message. If this message is not sent this client will block indefinitely. It's known that there are some commands where there is no `rpc_ok` return message, so that still needs to be fixed.

There are also some compound commands for common sequences, like picking up a tool. All these compound commands use a safe move by first moving the tool mount to max height before moving horizontally.

This code has used the examples in https://github.com/FarmBot-Labs/FarmBot-Python-Examples.

## Installation

This code will not run on Python 2.

This code depends on the `paho-mqtt` and `request` libraries (`pip install`...).

You will need to add your own `config.json` in your project root. Use the template `src/farmbot/config-template.json` for this. You will need your device ID and token to be able to connect to your FarmBot.

```
  ...
  "device_id": "device_9999",
  "token": "iufhahwiawfhaw....",
  ...
```

## Basic usage

This code will blink lights, plant a seed and water it. An initial call to `bot.start()` is possible but not needed, this will be called lazily before the first command is executed. bot.stop() is needed to cleanly end the MQTT client loop.

```
cfg = FarmBotConfiguration('./config.json')
bot = FarmBot(cfg, FarmBotConnection(cfg))
try:
    print("Hello Farmbot! Blinking the lights!")
    bot.blink_lights(3)
    print("Planting a seed from the Seed Bin into (100, 100, -100)..."
    bot.plant_seed(ToolBay.SeedBin, (100, 100, -100))
    # Smartly returning tools is a TODO
    bot.return_tool(ToolBay.Seeder)
    print("Watering at location (100, 100) for 4 seconds...")
    bot.water((100, 100), 4)
finally:
    bot.stop()
```

See the `FarmBot` class to see all implemented commands.

## The listener

The farmbot_listener can be used to monitor all messages, you can run it independently.

## Testing

Run unittests with `python -m unittest discover -v -s ./test -t .` from the project root