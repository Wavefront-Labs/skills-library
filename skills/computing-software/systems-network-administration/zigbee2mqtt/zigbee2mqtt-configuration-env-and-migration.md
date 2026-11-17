---
id: computing-software.systems-network-administration.zigbee2mqtt.zigbee2mqtt-configuration-env-and-migration
name: zigbee2mqtt-configuration-env-and-migration
category: computing-software
field: systems-network-administration
product: zigbee2mqtt
tags: [zigbee2mqtt, configuration-yaml, environment-variables, zigbee2mqtt-data, migration, config-version, runtime-options]
level: practitioner
status: docs-checked
description: "Handle Zigbee2MQTT configuration.yaml location, ZIGBEE2MQTT_CONFIG_ env overrides, runtime option changes, and the v2 automatic settings migration with its backup and log."
sources: ["https://www.zigbee2mqtt.io/guide/configuration/", "https://www.zigbee2mqtt.io/guide/configuration/configuration-update.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Zigbee2MQTT configuration file, env overrides and migration

- `configuration.yaml` lives in the `data` directory, which must be writable because the frontend edits the file. Relocate with `ZIGBEE2MQTT_DATA`.
- Override any key with an environment variable named `ZIGBEE2MQTT_CONFIG_` plus the uppercase dotted path with underscores: `mqtt.base_topic` becomes `ZIGBEE2MQTT_CONFIG_MQTT_BASE_TOPIC`.
- Change options without a restart where possible by publishing to `zigbee2mqtt/bridge/request/options`; some options still need a restart (the response carries `restart_required`).
- The documentation warns not to trust LLM-generated configurations; check keys against the reference.

Migration (from v2.0.0): on start the settings migration rewrites `configuration.yaml` to the current schema, repeating until up to date.
- It first backs up the file as `data/configuration_backup_v1.yaml` (named by the old version).
- It writes `data/migration-1-to-2.log` listing each `[REMOVAL]`, `[TRANSFER]`, `[CHANGE]` and `[ADDITION]`. Examples from the v1 to v2 notes: `advanced.baudrate` and `advanced.rtscts` moved to `serial`, `ban` renamed `passlist`, log level `warn` renamed `warning`, `advanced.legacy_api` and per-device `retrieve_state` removed.
- Never edit the `version` key by hand; it can corrupt the migration chain.
- Values supplied through the Home Assistant add-on page or environment variables are not stored in the file, so they are not migrated; fix them yourself.
- Migration cannot update third parties such as Home Assistant automations that used removed MQTT topics; read the log and the linked discussion.

## Checked

2026-11-03. Confirmed against the Configuration and Configuration update pages and the bridge/request/options entry of MQTT Topics and Messages: data directory and ZIGBEE2MQTT_DATA, env override naming, runtime options and restart_required, LLM caution, v2.0.0 migration, backup and log file names, migration tags and examples, version warning, add-on and env values not migrated. Removed: the unconfirmed stop-before-editing advice and the generic verify line.
Method: documentation only; no commands were run.
