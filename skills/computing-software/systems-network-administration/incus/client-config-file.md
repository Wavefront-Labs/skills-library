---
id: computing-software.systems-network-administration.incus.client-config-file
name: client-config-file
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, client, config-yml, incus-conf, incus-remote, incus-project, list-format, defaults]
level: practitioner
status: docs-checked
description: "Incus CLI client config.yml: location, INCUS_CONF/INCUS_REMOTE/INCUS_PROJECT overrides, built-in remotes, remote keys, defaults."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/client-config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Client configuration

- File: `$HOME/.config/incus/config.yml`; set `INCUS_CONF` to a directory containing `config.yml` to relocate it. Missing file means built-in defaults.
- Do not hand-edit; use `incus remote` and `incus alias`.
- Built-in remotes: `local` (protocol `incus`, `unix://`) and `images` (protocol `simplestreams`, public, `https://images.linuxcontainers.org`).
- Overrides: `INCUS_REMOTE` or a `<remote>:` prefix beats the default remote; `--project` and `INCUS_PROJECT` beat a remote's project.

Remote keys: `addr` (comma-separated for several), `last_working_address`, `auth_type` (`tls` or `oidc`), `keepalive` (seconds), `project`, `protocol` (`incus`, `oci`, `public`, `simplestream`), `credentials_helper` (OCI auth), `public` (image-only).

`defaults` section:
- `list_format`: same as `--format`; `csv`, `json`, `table`, `yaml`, `compact`, `markdown`.
- `console_type`: `console` or `vga`.
- `console_spice_command`: alternative SPICE viewer command.
- `no_color`: disable colours.

## Checked

2026-11-09. Confirmed against the Incus doc client-config.md (CLI configuration file): file location, INCUS_CONF, default file contents, remote keys and values, default remote override, and the defaults keys. Removed: nothing needed removing.

Method: documentation only; no commands were run.
