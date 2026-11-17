---
id: computing-software.messaging-and-integration.mosquitto.dynsec-install-and-init
name: dynsec-install-and-init
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [dynsec-init, plugin-opt-config-file, password-init-file, mosquitto-dynsec-password, dynsec]
level: practitioner
status: docs-checked
description: "Load mosquitto_dynamic_security.so, create its JSON config, and set the first admin password by file, variable or init command."
sources:
  - https://mosquitto.org/documentation/dynamic-security/
  - https://mosquitto.org/man/mosquitto_ctrl_dynsec-1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: activate the plugin and bootstrap an admin user.

Broker configuration:
```
plugin /path/to/mosquitto_dynamic_security.so
plugin_opt_config_file /path/to/dynamic-security.json
```
On Windows use the `.dll`. The page recommends `per_listener_settings false`. The JSON file is rewritten at each change; during normal operation the configuration stays in memory.

From 2.1, if the file does not exist the plugin generates a default one. Roles created: broker-admin, client (read/write on `#`), dynsec-admin, super-admin (any `$CONTROL` API), sys-notify, sys-observe, topic-observe. Group created: unauthenticated (for anonymous clients, if allowed). Admin password sources:
- `plugin_opt_password_init_file path/to/init-file`: a single-line file whose line is the admin password; delete it after first run. Suited to docker secrets.
- The `MOSQUITTO_DYNSEC_PASSWORD` environment variable.
- Neither: random passwords written in plain text to `<config file>.pw` (for example dynamic-security.json.pw). Delete it once known. Users `admin` and `democlient` (read/write on `#`) are created.

In 2.0.x use:
```
mosquitto_ctrl dynsec init path/to/dynamic-security.json admin-user [admin-password]
```
It asks for a password and creates the admin role user, which does not get access to publish to normal application topics; keep it for administration. It is the only mosquitto_ctrl step that does not connect to a broker.

## Checked

2026-11-08. Confirmed against the Dynamic Security plugin documentation page (and the mosquitto_ctrl_dynsec man page for the init synopsis). Plugin lines, per_listener_settings advice, 2.1 generated roles and group, the three password sources, the .pw file, admin and democlient users, and the 2.0 init command with optional admin password match. Claims unchanged.

Method: documentation only; no commands were run.
