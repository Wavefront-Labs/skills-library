---
id: computing-software.firmware-embedded-development.esphome.esphome-native-api-and-encryption
name: esphome-native-api-and-encryption
category: computing-software
field: firmware-embedded-development
product: esphome
tags: [esphome, native-api, home-assistant, api-encryption, noise, reboot-timeout, max-connections, batch-delay, actions, aioesphomeapi]
level: practitioner
status: docs-checked
description: "Configure the ESPHome native API used by Home Assistant: port, connection limits, encryption key, batch delay, reboot timeout, user actions and connection triggers."
sources: ["https://esphome.io/components/api/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Esphome native api and encryption

The native API is a custom TCP protocol on protocol buffers (definitions in `api.proto`) used by the ESPHome tool, Home Assistant and ioBroker; the Python client library is `aioesphomeapi`. Add `api:` and the device appears under discovered integrations in Home Assistant (up to 5 minutes), or add it manually by `<NODE_NAME>.local` or IP. "Services" were renamed "Actions"; the `services` YAML keys remain supported.

Options:
- `port` (default 6053).
- `encryption` with `key`: a 32-byte base64 string; if present, encryption is enabled. If no key is provided it can be set at runtime, but encryption is not used until then.
- `max_connections` (1 to 20; defaults 4 on ESP8266/RP2040, 5 on ESP32 and similar, 8 on host). It is compile-time: slots are statically allocated and each active connection uses roughly 500 to 1000 bytes of RAM, so keep it low on ESP8266.
- `max_send_queue` (1 to 64): a client whose queue overflows is disconnected and an error logged; raise it if legitimate clients drop.
- `listen_backlog` (1 to 10).
- `batch_delay` (0 to 65535ms, default 100ms) batches state updates; `0ms` sends immediately, useful for fast ON/OFF transitions like IR sensors, at the cost of traffic.
- `reboot_timeout` (default 15min, `0s` disables): reboots if no authenticated client connects, since a connection that never authenticates (port scan, stale key) does not count.
- `actions`: user-defined actions callable from Home Assistant.
- `custom_services`, `homeassistant_services`, `homeassistant_states`: compile support for external C++ components.
- `wizard`: setup wizard shown when the device is added.
- Triggers: `on_client_connected`, `on_client_disconnected`.

For security guidance, the docs point to the Security Best Practices guide.

## Checked

2026-11-04. Prose, option names, defaults and ranges were compared with https://esphome.io/components/api/ (fetched this batch). Nothing needed removing.

Method: documentation only; no commands were run.
