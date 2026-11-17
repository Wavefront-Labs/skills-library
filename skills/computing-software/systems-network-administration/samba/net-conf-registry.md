---
id: computing-software.systems-network-administration.samba.net-conf-registry
name: net-conf-registry
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, net-conf-registry, net-conf, registry-config, net, smb-conf]
level: advanced
status: docs-checked
description: "Manage Samba configuration in the registry with net conf: list, import, setparm, getparm, addshare and delshare, and the config backend and include = registry settings."
sources:
  - https://www.samba.org/samba/docs/current/man-html/net.8.html
  - https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# net conf registry
```
net conf list
net conf import [--test|-T] <filename> [section]
net conf setparm <section> <parameter> <value>
net conf getparm <section> <parameter>
net conf addshare <sharename> <path> [writeable={y|N} [guest_ok={y|N} [comment]]]
net conf delshare <sharename>
```
`global` is a valid section for setparm/getparm (setparm creates the section if missing), but `addshare` cannot use the name `global`. `import` without a section clears the existing registry configuration first; `--test` prints the result instead of applying it. Other subcommands include listshares, showshare, delparm, drop and the includes commands.

smb.conf hooks:
- `config backend`: default `file`; example value `registry`.
- `config backend = registry` gives a registry-only configuration (the recommended method per smb.conf) and sets `registry shares` to yes.
- `include = registry` (special value) reads the global options from the registry in a mixed setup and activates registry shares.
- `registry shares` defaults to `no`; shares in smb.conf take priority over same-named registry shares.

Example: `net conf import --test /path/to/smb.conf` prints the resulting configuration without changing the registry.

`addshare` takes `y`/`N` flags for writeable and guest_ok (capital N is the default).

## Checked
2026-11-04: command list and syntax compared with the net man page; config backend, registry shares and include = registry compared with the smb.conf man page. Removed: the vfs_btrfs source and its FSRVP aside, which were not rechecked here; reworded the import test note to match the page.
Method: documentation only; no commands were run.
