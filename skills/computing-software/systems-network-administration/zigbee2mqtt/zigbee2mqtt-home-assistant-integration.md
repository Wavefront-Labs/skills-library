---
id: computing-software.systems-network-administration.zigbee2mqtt.zigbee2mqtt-home-assistant-integration
name: zigbee2mqtt-home-assistant-integration
category: computing-software
field: systems-network-administration
product: zigbee2mqtt
tags: [zigbee2mqtt, home-assistant, mqtt-discovery, discovery-topic, birth-message, event-entities, rename-entity]
level: practitioner
status: docs-checked
description: "Enable Zigbee2MQTT Home Assistant MQTT discovery and tune it: discovery and status topics, experimental event entities, legacy action sensor, per-device discovery overrides."
sources: ["https://www.zigbee2mqtt.io/guide/configuration/homeassistant.html", "https://www.zigbee2mqtt.io/guide/configuration/devices-groups.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Zigbee2MQTT Home Assistant integration

```yaml
homeassistant:
    enabled: true
    discovery_topic: homeassistant
    status_topic: homeassistant/status
    experimental_event_entities: false
    legacy_action_sensor: false
```

- `discovery_topic` should differ from the MQTT `base_topic` or Home Assistant reports errors.
- `status_topic` is the Home Assistant status topic (default `homeassistant/status`).
- `experimental_event_entities: true` discovers an `event` entity per action; `event_type` carries the action and extra attributes like `button` hold detail. It may change in future.
- `legacy_action_sensor: true` sends an empty `action` after each one and discovers a `sensor_action`.
- Integration needs `advanced.cache_state: true` (the default).

Per device or group, override discovery payloads:

```yaml
devices:
    '0x00158d0001d82999':
        friendly_name: my_occupancy_sensor
        homeassistant:
            expire_after: 30
            temperature:
                icon: mdi:oil-temperature
                device_class: null
```
Top-level keys apply to every entity of the device; a key named after an entity (here `temperature`) applies only to it; `null` omits a value. `homeassistant: null` skips discovery entirely. Disabled devices show as unavailable.

Rename with `bridge/request/device/rename` plus `"homeassistant_rename": true` to rename the entity id as well. The add-on frontend port is fixed at 8099, and the `frontend.url` setting is used for the HA device configuration link. If you use the retention option set `mqtt.version: 5`.

## Checked

2026-11-03. Confirmed against the Home Assistant integration, Devices and Groups, Frontend and MQTT pages: homeassistant options and defaults, discovery_topic caveat, event entities, legacy action sensor, per-device discovery overrides and null handling, disabled devices, rename flag, add-on port 8099, frontend url, cache_state, mqtt version 5 for retention. Removed: the description of what status_topic does (not stated on the page) and the unverified verify line.
Method: documentation only; no commands were run.
