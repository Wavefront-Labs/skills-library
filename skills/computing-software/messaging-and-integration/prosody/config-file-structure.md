---
id: computing-software.messaging-and-integration.prosody.config-file-structure
name: config-file-structure
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, configuration, virtualhost, component, lua]
level: intro
status: docs-checked
description: "Prosody prosody.cfg.lua layout: global section, VirtualHost and Component scoping, list and map syntax, modules_enabled, and Include."
sources:
  - https://prosody.im/doc/configure
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prosody config file structure

Everything lives in one Lua file, `prosody.cfg.lua` (`/etc/prosody/prosody.cfg.lua` on GNU/Linux). A `prosody.cfg.lua.dist` example ships with Prosody.

Settings above the first `VirtualHost` are global and inherited by every host. A setting under a `VirtualHost` or `Component` line applies only to that host. At least one VirtualHost is required to start.

```lua
example_setting = "global"
VirtualHost "example.com"
example_setting = "only example.com"
Component "groups.example.com" "muc"
```

Syntax: strings, numbers, booleans, plus lists and maps in braces.

```lua
example_list = { "this"; "that"; }
example_map = { this = "that"; some = 7; }
```

Key options: `modules_enabled` (names without `mod_` or `.lua`), `modules_disabled`, `admins`, `authentication` (default `"internal_hashed"`), `enabled`, `allow_registration` (default false, needs mod_register), `tls_profile` (default `intermediate`).

Ports such as `c2s_ports` (5222) and `s2s_ports` (5269) are global-only. `Include "conf.d/*.cfg.lua"` loads other files relative to the main file; `ENV_NAME` reads an environment variable.

After editing, restart or reload.

Verify: `prosodyctl check config` reports no errors and `prosodyctl reload` succeeds.

## Checked

2026-11-04. Read the Configuring Prosody page: single prosody.cfg.lua at /etc/prosody on GNU/Linux, the .dist example, global versus VirtualHost and Component scoping, at least one VirtualHost required, list and map syntax, modules_enabled without mod_ prefix, authentication default internal_hashed, allow_registration false needing mod_register, tls_profile default intermediate, c2s_ports 5222 and s2s_ports 5269 as global settings, Include with globbing relative to the main file, and ENV_ variables all match. Nothing removed.

Method: documentation only; no commands were run.
