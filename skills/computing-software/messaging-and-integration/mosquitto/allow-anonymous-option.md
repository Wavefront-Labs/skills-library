---
id: computing-software.messaging-and-integration.mosquitto.allow-anonymous-option
name: allow-anonymous-option
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [allow-anonymous, authentication, listener-allow-anonymous]
level: practitioner
status: docs-checked
description: "Control whether clients without a username may connect, globally with allow_anonymous or per listener with listener_allow_anonymous."
sources:
  - https://mosquitto.org/man/mosquitto-conf-5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: decide whether unauthenticated clients may connect.

`allow_anonymous true|false` is a global boolean deciding whether clients that connect without a username are allowed. If false, another means of connection must be created to control authenticated client access.

Default: false, unless no listeners are defined in the configuration file, in which case it is true but connections are only allowed from the local machine. In version 1.6.x and earlier the default was true unless another security option was set.

`listener_allow_anonymous` overrides it for one listener; if not set explicitly the value of `allow_anonymous` is used. It is not reloaded on the reload signal, while `allow_anonymous` is.

The page also states that setting `allow_anonymous true` while `password_file` is defined is valid. Combined with `acl_file` it can give, for example, read-only guest accounts alongside defined users that can publish.

The page marks the per-listener behaviour of `allow_anonymous` under `per_listener_settings` as deprecated, and points to `listener_allow_anonymous` for per-listener control.

## Checked

Method: 2026-11-08 docs-only. Read the cited man page in full and compared each claim. Claims checked against mosquitto.conf(5). Removed the unsupported Dynamic Security anonymous group claim; reworded the deprecation note to what the page says.
