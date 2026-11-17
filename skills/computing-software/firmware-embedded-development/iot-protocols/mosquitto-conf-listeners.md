---
id: computing-software.firmware-embedded-development.iot-protocols.mosquitto-conf-listeners
name: mosquitto-conf-listeners
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [mosquitto-conf-listeners, mosquitto-broker, mosquitto, listener, mosquitto-conf, iot-protocols]
level: practitioner
status: docs-checked
description: "Mosquitto listeners and configuration: Write a minimal, safe mosquitto.conf for Mosquitto 2.x."
sources:
  - https://mosquitto.org/man/mosquitto-conf-5.html
  - https://mosquitto.org/man/mosquitto-8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mosquitto listeners and configuration

**Goal:** Write a minimal, safe mosquitto.conf for Mosquitto 2.x.

## Steps
1. With no listeners defined, allow_anonymous becomes true but connections are only accepted from the local machine; once you define a listener, allow_anonymous defaults to false
2. Declare each listener with `listener port [bind address]`, for example `listener 8883` followed by cafile, certfile and keyfile, and `listener 1883 127.0.0.1` for local clients
3. Add `protocol websockets` under a further listener for browsers (protocol defaults to mqtt; http_api is the third value)
4. per_listener_settings true makes password_file, acl_file, psk_file, allow_anonymous and plugin settings apply to the listener being configured; the manual marks it deprecated in favour of plugins
5. max_connections (per listener, -1 is unlimited), message_size_limit and max_inflight_messages (default 20) protect the broker
6. Use `include_dir conf.d` for split files
7. Test with `mosquitto -c file -v`

## Gotcha
With per_listener_settings true, the authentication and ACL options belong to the listener they follow, so put them after that listener line; with false (the default) they apply to all listeners.

## Verify
- [ ] mosquitto_sub on both listeners works as designed
- [ ] Unauthenticated remote client refused
- [ ] Log shows no config warnings

## Checked

2026-11-03. Confirmed in the mosquitto.conf(5) and mosquitto(8) man pages: the no-listener behaviour of allow_anonymous, listener syntax, protocol values, per_listener_settings and the options it affects, max_connections, message_size_limit, max_inflight_messages default, include_dir, and the -c and -v options. Removed: the claim that Mosquitto 2 binds only to localhost (the manual says anonymous local-only access when no listener is defined) and the "applies globally" wording for options placed before the first listener.
Method: documentation only; no commands were run.
