---
id: computing-software.systems-network-administration.zigbee2mqtt.zigbee2mqtt-pairing-and-removing-devices
name: zigbee2mqtt-pairing-and-removing-devices
category: computing-software
field: systems-network-administration
product: zigbee2mqtt
tags: [zigbee2mqtt, permit-join, pairing, interview, remove-device, force-remove, blocklist, passlist, install-code]
level: practitioner
status: docs-checked
description: "Permit joining in Zigbee2MQTT, pair through a chosen router, confirm the interview, remove devices (force, keep_config, clear_cache, block) and use blocklist or passlist."
sources: ["https://www.zigbee2mqtt.io/guide/usage/pairing_devices.html", "https://www.zigbee2mqtt.io/guide/usage/mqtt_topics_and_messages.html", "https://www.zigbee2mqtt.io/guide/configuration/block-pass-list.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Zigbee2MQTT pairing and removing devices

Permit join:
- Frontend button opens the network for 254 seconds; the arrow beside "Permit join (All)" lets you pair via the coordinator or a specific router (no guarantee it is chosen; helps awkward devices such as Aqara).
- MQTT: `zigbee2mqtt/bridge/request/permit_join` with `{"time": 254}`; `{"time": 0}` disables; `{"time": 60, "device": "bulb"}` or `"device": "coordinator"` restricts the join path.

Put the device in pairing mode (device page, else a factory reset). Success looks like `Successfully interviewed '0x00158d0001dc126a', device has successfully been paired`. Rename the last joined device with `{"last": true, "to": "new_name"}` on `bridge/request/device/rename`; add `"homeassistant_rename": true` to rename the HA entity id too.

Zigbee 3.0 devices that need an install code (QR code on the device): `bridge/request/install_code/add`.

Remove: publish `{"id": "my_bulb"}` to `bridge/request/device/remove`. The coordinator can only ask a device to leave, so a sleeping battery device may not respond (error such as `mgmtLeaveRsp after 10000ms`); factory reset it instead. Options:
- `force: true` deletes only from the database; the device still holds the network key until it is factory reset.
- `keep_config: true` keeps its saved config for later re-pairing.
- `clear_cache: true` forces a full interview next join (useful when developing a device, e.g. ESPHome).
- `block: true` makes Zigbee2MQTT request removal every time it tries to join.

Config-level control:

```yaml
blocklist: ['0x000b57fffec6a5b2']
passlist: ['0x000b57fffec6a5b3']
```
Everything not on the passlist is removed from the network, so test carefully.

## Checked

2026-11-03. Confirmed against the Allowing devices to join, MQTT Topics and Messages and Device blocklist/passlist pages: 254 second join, pairing via a chosen device, permit_join payloads, interview log line, install_code/add, device/remove and its force/keep_config/clear_cache/block options, rename with last and homeassistant_rename, blocklist and passlist keys and passlist removal warning. Nothing removed.
Method: documentation only; no commands were run.
