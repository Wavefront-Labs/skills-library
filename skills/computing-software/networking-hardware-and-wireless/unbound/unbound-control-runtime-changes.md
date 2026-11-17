---
id: computing-software.networking-hardware-and-wireless.unbound.unbound-control-runtime-changes
name: unbound-control-runtime-changes
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, unbound-control, set-option, forward-add, stub-add, local-zone, runtime]
level: practitioner
status: docs-checked
description: "Change Unbound without a reload using unbound-control: set_option and get_option, forward and stub zones, local zones and data, and root forwarders."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-control.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# unbound-control runtime changes
None of these are written to the config file. The manual says `set_option` values are not saved and that `forward` changes are gone after a reload.

- `set_option "opt: val"` changes an option without reload or cache flush; the name needs a trailing colon and whitespace before the value. Not all options work. Supported include statistics-interval, statistics-cumulative, do-not-query-localhost, selected harden-*, prefetch, prefetch-key, log-queries, hide-identity/version, identity, version, val-log-level, val-log-squelch, ignore-cd-flag, tcp-upstream, ssl-upstream, max-udp-size, ratelimit, ip-ratelimit, cache-max-ttl, cache-min-ttl, cache-max-negative-ttl.
- `get_option opt` prints a value without the colon.
- `forward_add [+it] zone addr...` and `forward_remove [+i] zone`; `stub_add [+ipt] zone addr...` and `stub_remove [+i] zone` (`+i` domain-insecure, `+t` TLS, `+p` prime).
- `forward [off | addr...]` shows, disables or sets root forwarders (optional `@port`); other forward zones are unaffected.
- `local_zone name type`, `local_zone_remove name`, `local_data RR data`, `local_data_remove name`, plus bulk `local_zones`, `local_datas` and their `_remove` forms from stdin.
- `list_stubs`, `list_forwards`, `list_insecure`, `list_local_zones`, `list_local_data` show current state.

## Checked

2026-11-08. Read the unbound-control manual page source in full. Tightened the persistence statement to what the manual says and noted not all options work with set_option.

Method: documentation only; no commands were run.
