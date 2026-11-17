---
id: computing-software.messaging-and-integration.mosquitto.message-and-packet-size-limits
name: message-and-packet-size-limits
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [message-size-limit, max-packet-size, payload, limits]
level: practitioner
status: docs-checked
description: "Limit publish payload size with message_size_limit and total packet size with max_packet_size."
sources:
  - https://mosquitto.org/man/mosquitto-conf-5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reject oversized messages.

`message_size_limit limit` sets the maximum publish payload size. Larger messages are not accepted: they are not forwarded to subscribers, but the QoS flow is completed for QoS 1 and 2. MQTT v5 clients using QoS 1 or 2 receive a PUBACK or PUBREC with the "implementation specific error" reason code. Default 0, meaning all valid MQTT messages are accepted; MQTT itself imposes a maximum payload of 268435455 bytes.

`max_packet_size value` applies to the full MQTT packet, not only the payload. MQTT v5 clients are told the maximum via the "maximum packet size" property; a client that sends a larger packet is disconnected. It applies to all clients regardless of version, but v3.1.1 and earlier clients cannot be notified. Default 2000000 bytes since 2.1; earlier versions had no limit. Values below 20 bytes are forbidden because they would interfere with normal client operation.

```
message_size_limit 1048576
max_packet_size 2000000
```

Both options are global and reloaded on the reload signal.

For bridges, `bridge_max_packet_size` restricts message size sent to a remote bridge, including headers and payload; the smaller of it and the remote broker's maximum-packet-size is used; 0 means unlimited.

## Checked

2026-11-03. Claims, option names, defaults and version notes were compared with the Mosquitto manual pages in `sources` (mosquitto(8), mosquitto.conf(5), mosquitto_pub, mosquitto_sub, mosquitto_rr, mosquitto_ctrl, and the Dynamic Security page where relevant). Nothing removed.

Method: documentation only; no commands were run.
