---
id: computing-software.messaging-and-integration.mosquitto.connection-limits
name: connection-limits
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [max-connections, global-max-clients, global-max-connections, limits]
level: practitioner
status: docs-checked
description: "Cap clients per listener with max_connections, note the Windows connection limits and bound heap use with memory_limit."
sources:
  - https://mosquitto.org/man/mosquitto-conf-5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: bound how many clients the broker accepts.

- `max_connections count` limits the total number of clients connected to the current listener. Set -1 for unlimited. The page notes other limits may be imposed outside Mosquitto's control, for example limits.conf. Not reloaded on the reload signal.

On Windows, concurrent connections are limited by the Windows API: approximately 8192 on modern versions such as Windows 10 or Windows Server 2019, and 2048 on earlier versions.

`memory_limit limit` sets a hard cap on heap bytes the broker will allocate; denied requests drop the incoming message and disconnect the publisher, or drop the outgoing message and disconnect the receiver. It is only available if memory tracking is compiled in, and lowering it on reload does not free memory.

## Checked

2026-11-03. Claims, option names, defaults and version notes were compared with the Mosquitto manual pages in `sources` (mosquitto(8), mosquitto.conf(5), mosquitto_pub, mosquitto_sub, mosquitto_rr, mosquitto_ctrl, and the Dynamic Security page where relevant). Removed the global_max_clients and global_max_connections options and their example (not on the page).

Method: documentation only; no commands were run.
