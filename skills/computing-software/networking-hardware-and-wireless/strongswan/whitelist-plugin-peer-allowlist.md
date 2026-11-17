---
id: computing-software.networking-hardware-and-wireless.strongswan.whitelist-plugin-peer-allowlist
name: whitelist-plugin-peer-allowlist
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, whitelist, allowlist, peer-identity, authentication]
level: practitioner
status: docs-checked
description: "Restrict which authenticated identities may connect to strongSwan with the whitelist plugin: enable flag, in-memory list, and the whitelist add, remove, list and flush commands."
sources:
  - https://docs.strongswan.org/docs/latest/plugins/whitelist.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# whitelist plugin peer allowlist
The whitelist plugin checks every successfully authenticated identity, in every authentication round and by any method, against an in-memory list. Identities not listed are rejected with AUTHENTICATION_FAILED. The plugin is disabled by default: build with `--enable-whitelist`.

The list is a hashtable held in memory, so it is volatile and lost when the daemon restarts.

Options in `charon.plugins.whitelist`:
- `enable` (default no): turns checking on. It can also be changed at runtime.
- `socket`: default `unix://${piddir}/charon.wlst`.

Manage it with the `whitelist` ipsec utility, usually `/usr/libexec/ipsec/whitelist`:

| Command | Effect |
|---|---|
| `whitelist add <identity>` | add one identity |
| `whitelist remove <identity>` | remove one identity |
| `whitelist add-from [<file>]` | add newline-separated identities, default stdin |
| `whitelist remove-from [<file>]` | remove identities read from a file or stdin |
| `whitelist flush [<pattern>]` | flush, optionally matching with wildcards |
| `whitelist list [<pattern>]` | list, optionally matching with wildcards |
| `whitelist enable` | enable checking |
| `whitelist disable` | disable checking |

The socket message format is in `whitelist_msg.h` and the tool source `whitelist.c` in the whitelist plugin source directory.

## Checked
2026-11-04. Confirmed against the strongSwan whitelist plugin page: --enable-whitelist, AUTHENTICATION_FAILED rejection, volatile in-memory list, enable and socket options, all whitelist commands. Nothing removed.

Method: documentation only; no commands were run.
