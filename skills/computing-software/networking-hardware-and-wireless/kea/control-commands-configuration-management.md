---
id: computing-software.networking-hardware-and-wireless.kea.control-commands-configuration-management
name: control-commands-configuration-management
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, control-channel, config-set, config-test, config-reload, config-write]
level: practitioner
status: docs-checked
description: "Use the Kea control commands config-test, config-set, config-reload and config-write to check, apply, reload and save configurations safely."
sources:
  - https://kea.readthedocs.io/en/latest/arm/ctrl-channel.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# configuration control commands
- `config-test`: checks whether a full configuration supplied in `arguments` could be loaded, sanity-checked as far as possible without loading it. A configuration that passes can still fail in `config-set` or at launch.
- `config-set`: replaces the running configuration with the full one supplied. The structure is `{"command": "config-set", "arguments": {"Dhcp6": { ... }}}` where the key is the server element name such as Dhcp4 or Dhcp6. Include the logger configuration: without it the server reverts to its default logging.
- `config-reload`: reloads the file Kea originally started with, picking up external edits. After a `config-set`, it reloads the original file and may lose changes made through `config-set` or other commands.
- `config-write`: writes the current configuration to disk. Optional argument `filename`; the default is the name passed with `-c`. Relative paths are written in the directory where Kea runs. Since 2.7.9 the file may only be written to the same directory as the startup config file.

Other related commands listed on the same page include `config-get`, `config-hash-get` and `build-report`.

## Checked
2026-11-04. Confirmed against the Kea Administrator Reference Manual (Management API chapter, config-test, config-set, config-reload and config-write sections). Removed: nothing.
Method: documentation only; no commands were run.
