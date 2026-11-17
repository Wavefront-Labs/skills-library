---
id: computing-software.messaging-and-integration.mosquitto.bridge-notifications
name: bridge-notifications
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [notifications, notification-topic, bridge-state, lwt]
level: practitioner
status: docs-checked
description: "Publish bridge connection state with notifications, notification_topic and notifications_local_only."
sources:
  - https://mosquitto.org/man/mosquitto-conf-5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let other clients see whether a bridge is up.

`notifications true|false` (default true) publishes notification messages to the local and remote brokers about bridge state. Retained messages go to `$SYS/broker/connection/<remote_clientid>/state` unless `notification_topic` is set. The value is 1 when the connection is active and 0 if it failed. It uses the Last Will and Testament feature.

- `notifications_local_only true` publishes only to the local broker; default false.
- `notification_topic topic` sets a custom topic; the default is `$SYS/broker/connection/<remote_clientid>/state`.

Subscribe with:
```
mosquitto_sub -v -t '$SYS/broker/connection/#'
```

mosquitto(8) says this status topic is provided by default within `$SYS/broker/connection/`.

With Dynamic Security, the `sys-notify` role allows bridges to publish connection state messages.

Because `remote_clientid` defaults to `name.hostname` (the connection name plus this computer's hostname), the default notification topic for a bridge named `br1` is `$SYS/broker/connection/br1.<hostname>/state` unless you set `remote_clientid` or `notification_topic`.

## Checked

2026-11-03. Claims, option names, defaults and version notes were compared with the Mosquitto manual pages in `sources` (mosquitto(8), mosquitto.conf(5), mosquitto_pub, mosquitto_sub, mosquitto_rr, mosquitto_ctrl, and the Dynamic Security page where relevant). Removed the $SYS write-access note and the ACL pattern line (not on the pages).

Method: documentation only; no commands were run.
