---
id: computing-software.messaging-and-integration.mosquitto.retained-message-options
name: retained-message-options
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [retain-available, retain-expiry-interval, check-retain-source, retained]
level: practitioner
status: docs-checked
description: "Configure retained messages with retain_available, retain_expiry_interval and check_retain_source."
sources:
  - https://mosquitto.org/man/mosquitto-conf-5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control how the broker handles retained messages.

- `retain_available true|false` (global, default true): if false, retained messages are not supported, and clients that send a message with the retain bit set are disconnected.
- `retain_expiry_interval minutes`: by default, retained messages that reached their message-expiry-interval are removed the next time they are accessed, either by being replaced or on the next matching subscription. If many retained messages with an expiry are published but never subscribed to, they remain in memory. A value greater than zero makes the broker check the retained tree at that interval in minutes. Default off.
- `check_retain_source true|false` (default true, applies globally regardless of `per_listener_settings`): the publisher of a retained message is checked for access rights before the message is republished, in case their access was removed after publishing. If false, no check is made.

```
retain_available true
retain_expiry_interval 60
check_retain_source true
```

`retain_available` and `retain_expiry_interval` are reloaded on the reload signal; the page gives no reload note for `check_retain_source`.

## Checked

Method: 2026-11-08 docs-only. Read the cited man page in full and compared each claim. Claims checked against mosquitto.conf(5). Removed unsupported claims about clearing retained messages and $SYS; clarified which options are reloaded.
