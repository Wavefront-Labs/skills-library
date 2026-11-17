---
id: computing-software.networking-hardware-and-wireless.frrouting.route-map-flow-control
name: route-map-flow-control
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, route-map, call, on-match, continue, default-deny, optimization]
level: advanced
status: docs-checked
description: "Control FRR route-map evaluation order with call, on-match next, continue and goto, understand the default deny, and use show, clear and optimization."
sources:
  - https://docs.frrouting.org/en/latest/routemap.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Route-map flow control
- `call NAME` runs another route-map after the set actions. If it returns deny, the route is denied regardless of the match policy or exit policy.
- Exit policy: `on-match next` proceeds to the next entry; `continue (1-65535)` proceeds to the specified sequence; `on-match goto N` proceeds to the first entry whose order is >= N. Jumping to a previous entry is not permitted.
- Default action: if no entries match, the route is denied. To change that, add an empty `permit` entry as the last entry.

Inspection:
- `show route-map [WORD] [json]` shows each daemon's knowledge of route-maps.
- `show route-map-unused [json]` lists unused route-maps.
- `clear route-map counter [WORD]` resets counters and CPU time.
- `route-map ROUTE-MAP-NAME optimization` is enabled by default; it uses a per-route-map prefix tree instead of checking each sequence in order.
- `debug routemap [detail]` turns on route-map debugging; detail adds more data.

In a BGP route server context, `call WORD` returns to the caller depending on the result.

## Checked

2026-11-04. Confirmed against the FRR Route Maps, Basic Commands and BGP (route server call) pages: call, exit policy commands, default deny, show and clear commands, optimization default. Reworded the debug routemap line.
Method: documentation only; no commands were run.
