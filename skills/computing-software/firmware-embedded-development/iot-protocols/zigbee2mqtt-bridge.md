---
id: computing-software.firmware-embedded-development.iot-protocols.zigbee2mqtt-bridge
name: zigbee2mqtt-bridge
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [zigbee2mqtt-bridge, zigbee-ops, zigbee2mqtt, zigbee, mqtt-bridge, coordinator-adapter, iot-protocols]
level: practitioner
status: draft
description: "Zigbee2MQTT bridge: Bridge a Zigbee network to MQTT with Zigbee2MQTT."
sources:
  - https://www.zigbee2mqtt.io/guide/configuration/
  - https://www.zigbee2mqtt.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Zigbee2MQTT bridge

**Goal:** Bridge a Zigbee network to MQTT with Zigbee2MQTT.

## Steps
1. Needs a coordinator adapter (e.g. Silicon Labs EFR32 or TI CC2652 flashed with coordinator firmware)
2. configuration.yaml: mqtt server, serial port, advanced.network_key, pan_id, channel
3. Devices publish zigbee2mqtt/<friendly_name> JSON; send commands to zigbee2mqtt/<name>/set
4. Bridge status at zigbee2mqtt/bridge/state
5. Home Assistant discovery via homeassistant: true
6. Enable permit_join in the frontend for pairing only
7. Back up coordinator_backup.json

## Gotcha
Changing the network key or channel later forces a re-pair of every device; set them before pairing.

## Verify
- [ ] Device state arrives on MQTT
- [ ] /set command toggles device
- [ ] Bridge state online
