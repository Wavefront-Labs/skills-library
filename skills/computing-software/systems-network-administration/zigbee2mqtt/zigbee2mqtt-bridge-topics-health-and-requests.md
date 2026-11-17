---
id: computing-software.systems-network-administration.zigbee2mqtt.zigbee2mqtt-bridge-topics-health-and-requests
name: zigbee2mqtt-bridge-topics-health-and-requests
category: computing-software
field: systems-network-administration
product: zigbee2mqtt
tags: [zigbee2mqtt, mqtt-api, bridge-request, bridge-health, health-check, networkmap, backup, transaction, bridge-info, restart]
level: practitioner
status: docs-checked
description: "Use the Zigbee2MQTT bridge MQTT API: request/response with transactions, set/get topics, networkmap, backup, restart, reporting configure and the bridge/health payload."
sources: ["https://www.zigbee2mqtt.io/guide/usage/mqtt_topics_and_messages.html", "https://www.zigbee2mqtt.io/guide/usage/health.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Zigbee2MQTT bridge API and health

Device topics: `zigbee2mqtt/<friendly_name>` (state), `/set` (JSON commands, or `/set/state` with a bare `ON`), `/get` (payload such as `{"state": ""}`; what is gettable is listed under Exposes on the device page), `/availability`. Example: `mosquitto_pub -t 'zigbee2mqtt/0x0fffffffffffffff/set' -m '{ "state": "ON" }'`.

Requests go to `zigbee2mqtt/bridge/request/<name>` and answers arrive on `zigbee2mqtt/bridge/response/<name>` with `status` of `ok` or `error` (plus an `error` string) and `data`. Add `"transaction": 23` to a request to match it to its response. Select an endpoint with a suffix on the device name, e.g. `my_remote/left`.

Useful requests: `permit_join`, `health_check`, `coordinator_check`, `restart` (empty payload), `networkmap`, `backup` (base64 zip of the data folder without logs; not all adapters support coordinator backup), `device/configure` (re-run configure when reporting is wrong), `device/interview` (after a firmware update adds features), `device/options` (`{"id": "my_bulb", "options": {"transition": 1}}`), `device/rename`, `device/reporting/configure` and `reporting/read`, `group/*`, `options`.

Other state topics: `bridge/state`, `bridge/info` (includes the settings JSON schema as `config_schema`), `bridge/devices`, `bridge/groups`, `bridge/event`, `bridge/logging`.

Health publishes to `zigbee2mqtt/bridge/health`: OS load and memory, process uptime and memory, MQTT connected/queued/published/received, and per device `leave_count`, `network_address_changes`, `messages`, `messages_per_sec`.

```yaml
health:
    interval: 10          # minutes
    reset_on_check: false # reset counters each check
```

## Checked

2026-11-03. Confirmed against the MQTT Topics and Messages and Health pages: set, set/state, get, mosquitto_pub example, request/response with status and transaction, endpoint suffix, request names, bridge info/devices/groups/event/logging topics, config_schema, health payload fields and health settings. Fixed: backup adapter claim now matches the page. Removed: the diagnostic inference about leaves and address changes.
Method: documentation only; no commands were run.
