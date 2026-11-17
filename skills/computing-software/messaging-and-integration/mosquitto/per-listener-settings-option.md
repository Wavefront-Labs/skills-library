---
id: computing-software.messaging-and-integration.mosquitto.per-listener-settings-option
name: per-listener-settings-option
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [per-listener-settings, listener, authentication]
level: advanced
status: docs-checked
description: "Decide whether authentication and ACL options apply globally or per listener with per_listener_settings."
sources:
  - https://mosquitto.org/man/mosquitto-conf-5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: scope authentication settings to one listener or to all.

`per_listener_settings true|false` defaults to false, which maintains the behaviour of previous versions.

When true, authentication and access control settings are controlled per listener. The affected options are `password_file`, `acl_file`, `psk_file`, `allow_anonymous`, `allow_zero_length_clientid`, `auto_id_prefix`, `plugin` and `plugin_opt_*`. Each such option placed after a `listener` line then applies to that listener only.

A durable client (clean session false) that has disconnected will use the ACL settings defined for the listener it was most recently connected to.

When false, those options apply to all listeners.

The page describes `per_listener_settings` as deprecated in the notes for `acl_file` and `password_file`, which suggest the `mosquitto_acl_file` and `mosquitto_password_file` plugins instead, since plugins let you control which listeners they apply to without it.

`global_plugin` loads a plugin for all listeners regardless of this setting. If it is true and you define both a `global_plugin` and a `plugin`, the global plugin is always processed first; if false, `global_plugin` behaves identically to `plugin`.

The option is reloaded on the reload signal.

## Checked

Method: 2026-11-08 docs-only. Read the cited man page in full and compared each claim. Claims checked against mosquitto.conf(5). Removed the unsupported claim about the Dynamic Security page; tied the deprecation note to the acl_file and password_file entries.
