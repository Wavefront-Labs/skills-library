---
id: computing-software.networking-hardware-and-wireless.powerdns.lua-records-health-checks
name: lua-records-health-checks
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, lua-records, ifportup, ifurlup, ifurlextup, pickselfweighted, failover]
level: practitioner
status: docs-checked
description: "PowerDNS LUA health-checked selection: ifportup, ifurlup, ifurlextup, pickselfweighted and their options."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/lua-records/functions.rst
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/lua-records/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LUA health-checked selection

- `ifportup(portnum, addresses[, options])`: an address is up if a TCP connect to the port succeeds. If none is up (after the first run) a random address from the full list is returned. Mixing IPv4 into AAAA, or the reverse, is an error. `addresses` may be nested sets: the first set with a live address wins.
- `ifurlup(url, addresses[, options])`: fetches the URL from each address; up means HTTP 200 plus `stringmatch` if set. `addresses` is a list of sets, tried in order.
- `ifurlextup(groups[, options])`: each IP has its own URL, as `{{['ip']='url', ...}, {...}}`; later groups are checked only if the previous is all down.
- `pickselfweighted(url, addresses[, options])` (5.0.0+): weights come from the health URL's response; addresses above 0 are chosen by weighted hash of `bestwho`.

Options:
- `selector`: `pickclosest`, `random`, `hashed`, `all` (default `random`). `backupSelector`: same plus `empty` (default `random`).
- `source`, `timeout` (default 2 s), `interval`, `minimumFailures` (default 1).
- `failOnIncompleteCheck`: SERVFAIL rather than the backup selector while checks are pending.
- `ifurlup` extras: `stringmatch`, `useragent` (default "PowerDNS Authoritative Server"), `byteslimit` (0 unlimited), `headers` (`_` becomes `-`).
- `pickselfweighted` also takes `httpcode` (default 200).

Example idea: an A record returning only the addresses with port 443 up, nearest first, via `{selector='pickclosest'}`.

On the first call these functions treat every address as failing, so the backup behaviour applies to the first resolution.

## Checked

2026-11-08. Read in full: PowerDNS docs lua-records/functions.rst and lua-records/index.rst. Confirmed ifportup, ifurlup, ifurlextup and pickselfweighted behaviour, the 5.0.0 note, every option name and default listed, the nested-set rule, and the first-run warning. Nothing removed; added the first-run warning.

Method: documentation only; no commands were run.
