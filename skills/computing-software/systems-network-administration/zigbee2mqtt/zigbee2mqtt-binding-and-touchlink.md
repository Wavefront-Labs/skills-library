---
id: computing-software.systems-network-administration.zigbee2mqtt.zigbee2mqtt-binding-and-touchlink
name: zigbee2mqtt-binding-and-touchlink
category: computing-software
field: systems-network-administration
product: zigbee2mqtt
tags: [zigbee2mqtt, binding, bind, unbind, touchlink, zll, factory-reset, reporting, remote, tradfri]
level: advanced
status: docs-checked
description: "Bind Zigbee remotes directly to bulbs or groups in Zigbee2MQTT, restrict clusters, clear binds, and use Touchlink to scan, identify or factory reset nearby devices."
sources: ["https://www.zigbee2mqtt.io/guide/usage/binding.html", "https://www.zigbee2mqtt.io/guide/usage/touchlink.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Zigbee2MQTT binding and Touchlink

Binding lets a device (for example an IKEA TRADFRI dimmer) control another device or group directly, giving smoother dimming and working even when Zigbee2MQTT, the broker or the coordinator is down.

Topics (frontend: device Bind tab):
- `zigbee2mqtt/bridge/request/device/bind` and `.../unbind` with `{"from": "my_remote", "to": "my_bulb"}`.
- `"clusters": ["genOnOff"]` restricts it; options are `genScenes`, `genOnOff`, `genLevelCtrl`, `lightingColorCtrl`, `closuresWindowCovering`.
- Endpoints: `from_endpoint` and `to_endpoint`, or `"from": "my_remote/left"`; most setups do not need this.
- `bridge/request/device/binds/clear` with `{"target": "my_device"}` (optionally `"ieee_list": [...]`) clears real bindings and resyncs Zigbee2MQTT's cache.
- A battery device must be awake: press a button immediately before sending.

Remote to several bulbs: create a group, add both bulbs with `group/members/add`, then bind `{"from": "my_remote", "to": "my_group"}`. A group target must be given by friendly name, not id.

Binding configures reporting on the target so Zigbee2MQTT sees state changes made via the remote. Old Philips Hue, GLEDOPTO and Muller Licht lamps report little or nothing; for such lamps bind to a group, which makes Zigbee2MQTT poll. Unbinding removes manually set reportings of those clusters when no binds remain.

Touchlink works between physically close devices (about 10 cm, up to 1 m on strong adapters) regardless of network. Supported: Texas Instruments adapters fully, Silicon Labs partially. Compatible devices expose the Touchlink cluster (most Philips and IKEA). Some disable it after a few minutes, so power-cycle first.
- Scan: `bridge/request/touchlink/scan`, empty payload; takes up to a minute and interrupts communication.
- Identify: `.../touchlink/identify` with `{"ieee_address": "0x12345678", "channel": 12}`.
- Factory reset: `.../touchlink/factory_reset`; empty targets the first device found (power off others), or pass ieee_address and channel. Permit join afterwards to re-pair.

## Checked

2026-11-03. Confirmed against the Binding and Touchlink pages: bind/unbind payloads, cluster list, endpoints, group target by friendly name, clear binds payloads, reporting behaviour and device table, Touchlink range, adapter support, scan/identify/factory_reset topics and payloads, power-cycle advice. Nothing removed.
Method: documentation only; no commands were run.
