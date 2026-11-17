---
id: computing-software.networking-hardware-and-wireless.powerdns.pdns-control-server-commands
name: pdns-control-server-commands
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, pdns-control, ping, reload, rediscover, purge, current-config, flush]
level: practitioner
status: docs-checked
description: "pdns_control options and server commands: ping, rediscover, reload, purge, current-config, set query-logging, flush, token-login."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/manpages/pdns_control.1.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pdns_control server commands

Usage: `pdns_control [OPTION]... <COMMAND>`. Options: `--config-dir=<DIR>`, `--config-name=<NAME>` (virtual instance), `--socket-dir=<DIR>`, `--remote-address=<ADDRESS>`, `--remote-port=<PORT>`, `--secret=<SECRET>`, `--chroot=<DIR>`.

- `ping`: replies PONG (works inside a guardian); `rping` for servers without one.
- `version`: version of the running daemon.
- `quit` / `stop`: exit the server.
- `rediscover`: backends look for new zones (database, or `named.conf` for BIND).
- `reload`: reload existing zones; it does not add new ones.
- `purge [RECORD]`: drop cache entries; a name ending in `$` drops all entries that end with that name; no argument clears the whole cache. `ccounts` shows cache contents.
- `current-config [diff]`: running configuration in `pdns_server --config` format; `diff` shows only changed options.
- `cycle`: restart to reload configuration (guardian mode only).
- `set <VARIABLE> <VALUE>`: currently only `query-logging` can be set.
- `flush`: write backend data to stable storage; normally nothing to flush, except LMDB with write notification updates disabled.
- `token-login <MODULE> <SLOT> <PIN>`: log in to a PKCS#11 slot once; needs PKCS#11 support at compile time.
- `cookie-secret list|add|delete`: EDNS cookie secrets (changes are not saved to or removed from the config file).

## Checked

2026-11-08. Read in full: PowerDNS docs manpages/pdns_control.1.rst. Confirmed the usage line, all seven listed options, and the general, cache, cookie-secret, configuration, data and PKCS#11 command descriptions. Tightened the purge wording to match the page.

Method: documentation only; no commands were run.
