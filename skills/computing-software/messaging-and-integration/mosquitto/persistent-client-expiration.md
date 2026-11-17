---
id: computing-software.messaging-and-integration.mosquitto.persistent-client-expiration
name: persistent-client-expiration
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [persistent-client-expiration, clean-session, session-expiry, expiry]
level: advanced
status: docs-checked
description: "Remove disconnected persistent client sessions after a set time with persistent_client_expiration."
sources:
  - https://mosquitto.org/man/mosquitto-conf-5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop abandoned persistent sessions accumulating.

`persistent_client_expiration duration` removes the session of persistent clients (clean session false) that are not connected and do not reconnect within the time frame. It is non-standard in MQTT v3.1; v3.1.1 and v5.0 allow brokers to remove sessions. If not set, persistent clients never expire.

The duration is an integer followed by one of `s h d w m y` (second, hour, day, week, month, year):

```
persistent_client_expiration 2m
persistent_client_expiration 14d
persistent_client_expiration 1y
```

Motivation from the page: badly designed clients may set clean session to false while using a randomly generated client id, which leads to persistent clients that connect once and never reconnect. The docs add that although you can specify seconds, that is not a suggestion to use a short interval; where possible fix the clients instead.

The option is global and reloaded on the reload signal.

Related: `global_max_clients` counts disconnected persistent sessions toward its limit, so unexpired sessions consume client slots.

## Checked

Method: 2026-11-08 docs-only. Read the cited man page in full and compared each claim. Claims checked against mosquitto.conf(5). Removed the unsupported $SYS expired counter claim; other claims unchanged.
