---
id: computing-software.messaging-and-integration.mosquitto.plugin-loading-options
name: plugin-loading-options
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [plugin, global-plugin, plugin-opt, extension]
level: advanced
status: docs-checked
description: "Load Mosquitto plugins with plugin and global_plugin, pass settings with plugin_opt_*, and understand ordering and reload limits."
sources:
  - https://mosquitto.org/man/mosquitto-conf-5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: extend the broker with authentication, access control or other plugins.

`plugin file path` specifies an external module for authentication, access control and other features. It can be specified multiple times; plugins are processed in the order specified. If `password_file` or `acl_file` are also used, the plugin checks run before the built-in checks.

`plugin_opt_* value` passes options to the most recent `plugin` or `global_plugin` defined in the file; see the specific plugin's instructions for which options exist.

```
plugin /path/to/plugin.so
plugin_opt_<name> value
```

The older names `auth_plugin` and `auth_opt_*` are also available but deprecated and to be removed in a future version.

`global_plugin file path` loads a plugin for use across all listeners regardless of `per_listener_settings`. With `per_listener_settings` true and both kinds defined, the global plugin is processed first; with it false, `global_plugin` behaves identically to `plugin`.

If `per_listener_settings` is true, a `plugin` is loaded for the current listener only.

Plugins are not currently reloaded on the reload signal (the page does not say a restart is required, but that follows from it).

The page points to the Dynamic Security plugin documentation for a plugin that handles username/password authentication and access control.

## Checked

Method: 2026-11-08 docs-only. Read the cited man page in full and compared each claim. Claims checked against mosquitto.conf(5). Removed the unsupported Dynamic Security example options and Windows dll claim; marked the restart implication as inference.
