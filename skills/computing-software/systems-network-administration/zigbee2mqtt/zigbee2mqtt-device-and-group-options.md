---
id: computing-software.systems-network-administration.zigbee2mqtt.zigbee2mqtt-device-and-group-options
name: zigbee2mqtt-device-and-group-options
category: computing-software
field: systems-network-administration
product: zigbee2mqtt
tags: [zigbee2mqtt, friendly-name, debounce, throttle, retain, qos, filtered-attributes, optimistic, device-options, disabled]
level: practitioner
status: docs-checked
description: "Use Zigbee2MQTT per-device options (friendly_name, debounce, throttle, retain, qos, filtered_attributes, optimistic, disabled), device_options defaults, groups and split files."
sources: ["https://www.zigbee2mqtt.io/guide/configuration/devices-groups.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Zigbee2MQTT device and group options

`configuration.yaml` keys each device by IEEE address; only `friendly_name` is required.

```yaml
devices:
    '0x00158d0001d82999':
        friendly_name: 'kitchen/occupancy'
        retain: true
        qos: 1
        debounce: 0.5
        debounce_ignore: [action]
device_options:
    retain: true
```

Option semantics:
- `friendly_name` forms the MQTT topic; `/` creates folders (`kitchen/floor_light`). It must not end in `/`, `/` plus an endpoint name such as `left`, or `/` plus a number.
- `debounce: N` waits for N seconds of silence and merges messages (useful for sensors that send temperature, humidity and pressure separately). Keep it below the sensor's report interval or nothing is published. `debounce_ignore` keeps unique values of listed properties (e.g. `action`).
- `throttle: N` processes the first message then drops everything for N seconds, whole messages, not attributes. `debounce` wins if both are set.
- `filtered_attributes: [battery]` stops publishing those attributes; `filtered_cache` keeps them out of the cache so unchanged values do not republish.
- `optimistic` (default true): after a successful command the state updates before the device confirms. `filtered_optimistic` limits which attributes are optimistically published.
- `disabled: true` does not stop the device talking; it only stops pings, startup configure, network-map scans and group optimistic updates, and marks it unavailable in Home Assistant. Use for seasonal devices.
- `retention` (seconds) needs `mqtt.version: 5`. `icon` is a file under `device_icons/` or a URL. `homeassistant:` overrides discovery payloads; `homeassistant: null` skips discovery.
- Device-type options such as `occupancy_timeout` appear on the device's page.

Groups: key must be a quoted integer; options `friendly_name`, `retain`, `transition`, `optimistic`, `homeassistant`. Devices and groups can be moved to `devices: devices.yaml` and `groups: groups.yaml`.

## Checked

2026-11-03. Confirmed against the Devices and Groups page: required keys, friendly_name rules, debounce and debounce_ignore, throttle and precedence, filtered_attributes, filtered_cache, optimistic and filtered_optimistic, disabled effects, retention with MQTT 5, qos, icon rules, homeassistant overrides, device_options, group keys and external files. Removed: the stop-before-editing advice, which is not on the page.
Method: documentation only; no commands were run.
