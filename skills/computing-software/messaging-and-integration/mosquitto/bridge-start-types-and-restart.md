---
id: computing-software.messaging-and-integration.mosquitto.bridge-start-types-and-restart
name: bridge-start-types-and-restart
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [start-type, restart-timeout, lazy, idle-timeout]
level: advanced
status: docs-checked
description: "Control when a bridge connects with start_type (automatic, lazy, once), threshold, idle_timeout and restart_timeout backoff."
sources:
  - https://mosquitto.org/man/mosquitto-conf-5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: decide how a bridge starts, stops and reconnects.

`start_type automatic|lazy|once`:
- `automatic` (default): starts when the broker starts and restarts after a short delay if the connection fails.
- `lazy`: starts when queued messages exceed `threshold` (default 10 messages) and stops after `idle_timeout` seconds idle (default 60).
- `once`: starts with the broker and is not restarted if the connection fails.

The RSMB "manual" type is not supported.

`restart_timeout base cap [stable]` or `restart_timeout constant` sets the wait before reconnecting for automatic bridges, as a constant number of seconds or "Decorrelated Jitter" backoff from base up to cap. Base is 1-3600 seconds; cap is at least base and at most 7200. The backoff resets to base after a successful connection; with `stable` it resets only if the connection stays open at least that many seconds.

```
restart_timeout 20
restart_timeout 10 60
restart_timeout 10 60 30
```

Default: jitter with base 5 seconds and cap 30 seconds.

`keepalive_interval seconds` (default 60, minimum 5) is the idle time before the bridge pings.

`bridge_reload_type lazy|immediate`: config changes apply on bridge reconnection; `lazy` (default) waits for a natural reconnect, `immediate` forces one.

## Checked

2026-11-03. Claims, option names, defaults and version notes were compared with the Mosquitto manual pages in `sources` (mosquitto(8), mosquitto.conf(5), mosquitto_pub, mosquitto_sub, mosquitto_rr, mosquitto_ctrl, and the Dynamic Security page where relevant). Nothing removed.

Method: documentation only; no commands were run.
