---
id: computing-software.firmware-embedded-development.iot-protocols.mosquitto-bridge
name: mosquitto-bridge
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [mosquitto-bridge, mosquitto-broker, mosquitto, bridge, connection, iot-protocols]
level: practitioner
status: docs-checked
description: "Mosquitto bridge configuration: Forward topics between an edge broker and a cloud broker."
sources:
  - https://mosquitto.org/man/mosquitto-conf-5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mosquitto bridge configuration

**Goal:** Forward topics between an edge broker and a cloud broker.

## Steps
1. Start a bridge with `connection name` (the name is also the client id on the remote broker unless remote_clientid is set), then `address host:port`
2. Add `topic pattern [[[out|in|both] qos] local-prefix remote-prefix]`, for example `topic sensors/# out 1 local/ remote/`; direction defaults to out and QoS to 0
3. Prefixes remap topics: outgoing messages lose the local prefix and gain the remote prefix, incoming the reverse; `""` is an empty prefix
4. For TLS set bridge_cafile (or bridge_capath or bridge_tls_use_os_certs) and, if the remote requires a client certificate, bridge_certfile and bridge_keyfile; bridge_tls_version is tlsv1.3 or tlsv1.2 and defaults to tlsv1.2
5. try_private (default true) asks the remote broker to treat the connection as a bridge, which improves loop detection and retained-message propagation; set false if the remote broker will not accept it
6. cleansession defaults to false, so the remote broker keeps the bridge subscriptions across link loss; local_clientid defaults to local.<remote_clientid>
7. restart_timeout takes a constant (`restart_timeout 20`) or `base cap [stable]` backoff (default base 5 s, cap 30 s); keepalive_interval defaults to 60 s with a 5 s minimum
8. bridge_protocol_version is mqttv50, mqttv311 or mqttv31 (default mqttv311)

## Gotcha
Care must be taken that topic patterns do not create a loop, where each broker keeps forwarding the same messages to the other; high CPU load on a broker is a symptom. Changing a topic list while cleansession is false can leave stale subscriptions on the remote broker; reconnect once with cleansession true to clear them.

## Verify
- [ ] Message published locally appears remotely
- [ ] Link drop then recovery replays queued QoS 1
- [ ] No loops in log

## Checked

2026-11-03. Confirmed in the mosquitto.conf(5) man page (Configuring Bridges): connection, address, topic syntax with direction, QoS and prefix remapping, the loop warning, try_private, cleansession (default false), local_clientid default, restart_timeout syntax and defaults, keepalive_interval default and minimum, bridge_cafile/capath/tls_use_os_certs, bridge_certfile, bridge_keyfile, bridge_tls_version, bridge_protocol_version. Removed: the claim that distinct prefixes per direction avoid loops, and the claim that local_clientid is what keeps queued messages (the page ties that to cleansession).
Method: documentation only; no commands were run.
