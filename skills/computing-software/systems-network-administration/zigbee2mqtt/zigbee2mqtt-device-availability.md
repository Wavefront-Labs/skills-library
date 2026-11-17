---
id: computing-software.systems-network-administration.zigbee2mqtt.zigbee2mqtt-device-availability
name: zigbee2mqtt-device-availability
category: computing-software
field: systems-network-administration
product: zigbee2mqtt
tags: [zigbee2mqtt, availability, offline, online, ping, backoff, passive-devices, battery-devices, lwt]
level: practitioner
status: docs-checked
description: "Enable and tune Zigbee2MQTT availability: timeouts for active and battery devices, ping backoff, per-device overrides, state retrieval on reconnect and coordinator load."
sources: ["https://www.zigbee2mqtt.io/guide/configuration/device-availability.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Zigbee2MQTT device availability

Enable it:

```yaml
availability:
    enabled: true
```

State is a retained message on `zigbee2mqtt/<friendly_name>/availability` with `{"state":"online"}` or `{"state":"offline"}`.

How it works:
- Active (mains-powered) devices must check in every 10 minutes by default; if not, Zigbee2MQTT pings them, and a failed ping marks them offline.
- Passive (battery) devices cannot be pinged; they must check in within 25 hours (1500 min) or go offline.
- A check-in is any Zigbee message reaching Zigbee2MQTT, including internal ones. The timeout persists across restarts, so stopping Zigbee2MQTT longer than 10 minutes marks active devices offline until they speak again.

Tuning:

```yaml
availability:
    enabled: true
    active:
        timeout: 10
        max_jitter: 30000
        backoff: true
        pause_on_backoff_gt: 0
    passive:
        timeout: 1500
devices:
    '0x12345678':
        friendly_name: my_bulb
        availability: false      # off for this device
    '0x87654321':
        friendly_name: my_switch
        availability:
            timeout: 3
```

`backoff` multiplies the ping interval x1.5, x3, x6, x12 after failures (10, 15, 30, 60, 120 min). `pause_on_backoff_gt` stops pinging above a backoff level until the device speaks. To enable for only some devices, omit the global `enabled` and set `availability: true` per device.

On reconnect or announce, Zigbee2MQTT reads `state`, `brightness`, `color_temp` and `color`, which fixes bulbs that power on after mains returns. Groups are available when at least one member is.

Pinging is heavy on a CC2530 or CC2531; a higher active timeout means less load.

## Checked

2026-11-03. Confirmed against the Device Availability page: enabled flag, retained availability topic, active 10 min and passive 1500 min defaults, check-in definition, persisted timeout, max_jitter, backoff pattern, pause_on_backoff_gt, per-device overrides, state retrieval attributes, CC2530/CC2531 load note, group availability. Nothing removed.
Method: documentation only; no commands were run.
