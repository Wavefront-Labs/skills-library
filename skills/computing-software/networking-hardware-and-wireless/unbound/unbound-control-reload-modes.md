---
id: computing-software.networking-hardware-and-wireless.unbound.unbound-control-reload-modes
name: unbound-control-reload-modes
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, unbound-control, reload, fast-reload, reload-keep-cache, lifecycle]
level: practitioner
status: docs-checked
description: "Choose between unbound-control reload, reload_keep_cache and fast_reload, with the +d, +p and +v flags and what each cannot change."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-control.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# unbound-control reload modes
- `start` runs unbound(8) from PATH; `stop` makes the daemon exit.
- `reload` flushes the cache and rereads the config.
- `reload_keep_cache` keeps the RRset and message caches if the new config allows; cache sizes and thread count must be unchanged.
- `fast_reload [+dpv]` (experimental) loads and prepares the config in a thread, then pauses briefly to apply it. The cache is kept and in-progress queries continue under the new options. Needs threads; temporary memory is about twice the config size.

Flags:
- `+d` drops queries being worked on (like `flush_requestlist`); implied, with a warning, for `define-tag` changes unless tags are only appended.
- `+p` does not pause threads (pause about 3 microseconds instead of about 0.3 ms) but threads may briefly see mixed settings; options that plain fast_reload does handle, such as val-bogus-ttl, val-sig-skew-min/max, target-fetch-policy, private-address, ratelimit and ip-ratelimit, are not reloaded.
- `+v` prints timing (the reload time is the pause); `+vv` adds temporary memory.

Not changeable by `fast_reload`: interface, outgoing-interface, remote-control, outgoing-port-permit/avoid, msg-buffer-size, any `*-slabs`, statistics-interval, and most dnstap transport settings.

Changeable includes forwards, stubs, views, auth, RPZ, local zones, access-control and trust anchors.

## Checked

2026-11-08. Read the unbound-control manual page source in full. Replaced a vague val-* claim with the options the manual lists as not reloaded under +p.

Method: documentation only; no commands were run.
