---
id: computing-software.systems-network-administration.zigbee2mqtt.zigbee2mqtt-ota-firmware-updates
name: zigbee2mqtt-ota-firmware-updates
category: computing-software
field: systems-network-administration
product: zigbee2mqtt
tags: [zigbee2mqtt, ota, firmware-update, zigbee-ota, downgrade, schedule-update, ota-index]
level: advanced
status: docs-checked
description: "Update Zigbee device firmware over the air in Zigbee2MQTT: check, update, abort, downgrade and schedule topics, update states, check intervals and custom OTA index files."
sources: ["https://www.zigbee2mqtt.io/guide/usage/ota_updates.html", "https://www.zigbee2mqtt.io/guide/configuration/ota-device-updates.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Zigbee2MQTT OTA firmware updates

Read the release notes first; updates can change behaviour or break compatibility. Images come from the Koenkk/zigbee-OTA repository by default (internet required).

State appears on `zigbee2mqtt/<device>` as `{"update":{"state":"available"}}`; states are `idle`, `available`, `scheduled`, `updating` (with `progress` percent and `remaining` seconds every 30 s).

Topics (payload `{"id":"my_remote"}`, id is IEEE address or friendly name):
- `zigbee2mqtt/bridge/request/device/ota_update/check` (add `/downgrade` for downgrades)
- `.../ota_update/update` (and `/update/downgrade`)
- `.../ota_update/update/abort`
- `.../ota_update/schedule` (and `/schedule/downgrade`, `.../unschedule`)

A check response contains `update_available`, plus `source`, `release_notes` and `downgrade` when one exists. Wake sleeping devices with a button press right before check or update, or schedule the update to start on the device's next update request (some Legrand models only update this way).

Expect 10 to 100 minutes and heavy mesh traffic: update one device at a time during quiet periods. The device reboots afterwards, which may switch a light on, and Zigbee2MQTT re-interviews and reconfigures it, possibly overwriting custom reporting intervals.

```yaml
ota:
    update_check_interval: 1440        # minutes, device-initiated checks ignored inside this
    disable_automatic_update_check: false
    image_block_response_delay: 250    # ms; raise if the network is unstable
    default_maximum_data_size: 50
    zigbee_ota_override_index_location: my_index.json
```

The override index is a file in the config directory, a full path (careful in containers) or an HTTP(S) URL; it is how you add images for DIY devices or replace official ones. `disable_automatic_update_check` also exists per device and does not block scheduled OTA.

## Checked

2026-11-03. Confirmed against the OTA updates and OTA device firmware update pages: default image source, update states and progress, check/update/abort/schedule/unschedule and downgrade topics, check response fields, wake-up advice, 10-100 minute duration, re-interview, ota settings with defaults, override index forms and precedence. Nothing removed.
Method: documentation only; no commands were run.
