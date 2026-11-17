---
id: computing-software.messaging-and-integration.mosquitto.queue-and-inflight-limits
name: queue-and-inflight-limits
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [max-queued-messages, max-queued-bytes, max-inflight-messages, queue-qos0-messages]
level: advanced
status: docs-checked
description: "Bound per-client message queues and in-flight QoS 1/2 messages with max_queued_*, max_inflight_* and queue_qos0_messages."
sources:
  - https://mosquitto.org/man/mosquitto-conf-5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: protect the broker from slow or offline clients.

All options are global and reloaded on the reload signal.

- `max_queued_messages count`: maximum QoS 1 or 2 messages held per client above those in flight. Default 1000; 0 means no maximum (not recommended).
- `max_queued_bytes count`: byte limit for the same queue; default 0 (no maximum). If both limits are set, packets are queued until the first is reached. Once reached, further messages are silently dropped.
- `max_inflight_messages count`: maximum outgoing QoS 1 or 2 messages being transmitted at once, including handshakes and retries. Default 20; 0 for no maximum; 1 guarantees in-order delivery.
- `max_inflight_bytes count`: byte limit for in-flight messages; default 0 (no limit). With a limit of 100, messages over 100 bytes are still allowed, but only one can be in flight.
- `queue_qos0_messages true`: queue QoS 0 messages for a disconnected persistent client; included in the `max_queued_messages` limit; default false; non-standard. With bridge topics at QoS 1 or 2, incoming QoS 0 messages for those topics are queued too.

Dropped messages show up in `$SYS/broker/mqtt/publish/dropped` (also `$SYS/broker/publish/messages/dropped`) and `$SYS/broker/load/publish/dropped/+`.

## Checked

2026-11-03. Claims, option names, defaults and version notes were compared with the Mosquitto manual pages in `sources` (mosquitto(8), mosquitto.conf(5), mosquitto_pub, mosquitto_sub, mosquitto_rr, mosquitto_ctrl, and the Dynamic Security page where relevant). Nothing removed.

Method: documentation only; no commands were run.
