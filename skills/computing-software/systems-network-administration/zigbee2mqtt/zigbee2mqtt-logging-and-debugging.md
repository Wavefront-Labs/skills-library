---
id: computing-software.systems-network-administration.zigbee2mqtt.zigbee2mqtt-logging-and-debugging
name: zigbee2mqtt-logging-and-debugging
category: computing-software
field: systems-network-administration
product: zigbee2mqtt
tags: [zigbee2mqtt, logging, log-level, namespaces, syslog, debug, zigbee-herdsman, log-rotation]
level: practitioner
status: docs-checked
description: "Configure Zigbee2MQTT logging: levels, namespaced levels, outputs including syslog, rotation, debug capture from startup, debug to MQTT and namespace filtering by regex."
sources: ["https://www.zigbee2mqtt.io/guide/configuration/logging.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Zigbee2MQTT logging and debugging

```yaml
advanced:
    log_level: info                       # debug, info, warning, error
    log_output: [console, file]           # also syslog; [] silences
    log_directory: data/log/%TIMESTAMP%
    log_directories_to_keep: 10
    log_file: log.txt
    log_rotation: true                    # 10MB around 3 files
    log_console_json: false
    log_symlink_current: false
```

Runtime change: use the frontend, or publish to `zigbee2mqtt/bridge/request/options` the payload `{"options": {"advanced": {"log_level": "debug"}}}`.

Namespaces: `z2m` (Zigbee2MQTT), `zh` (zigbee-herdsman, the Zigbee library), `zhc` (zigbee-herdsman-converters, device support). A level set in `log_namespaced_levels` applies to that namespace and everything below it:

```yaml
advanced:
    log_level: warning
    log_namespaced_levels:
        zhc: info
        zhc:legacy:fz: debug
```
Here `zhc:ota:common` logs at info, `zhc:legacy:fz:tuya` at debug, `z2m:mqtt` at warning.

Cut MQTT traffic from logs: only info and above are published to MQTT; raise `z2m:mqtt` to `warning` as it is a large contributor. Debug lines are not published to MQTT or the frontend unless `log_debug_to_mqtt_frontend: true`.

Hide noisy debug namespaces with an ECMAScript regex: `log_debug_namespace_ignore: '^zhc:legacy:fz:(tuya|moes)|^zh:ember:uart:|^zh:controller'`.

To capture a full startup for a bug report: `log_level: debug`, `log_rotation: false`, `log_output: [file]`. Syslog needs a `log_syslog` block (host, port, protocol, facility, `type: '5424'` for RFC 5424, `app_name`).

## Checked

2026-11-03. Confirmed against the Logging page and the bridge/request/options entry of MQTT Topics and Messages: levels, options with defaults, rotation, namespaces and hierarchy example, MQTT publishing rules, debug capture settings, log_debug_namespace_ignore regex, syslog block, runtime log_level payload. Nothing removed.
Method: documentation only; no commands were run.
