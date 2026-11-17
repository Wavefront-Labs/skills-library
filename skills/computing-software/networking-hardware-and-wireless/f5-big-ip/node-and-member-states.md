---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.node-and-member-states
name: node-and-member-states
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, member-states, force-offline, connection-draining]
level: practitioner
status: draft
description: "Take BIG-IP pool members and nodes in and out of service with disable versus force offline and read availability reasons."
sources:
  - https://www.f5.com/pdf/certification/exams/blueprint-tmos-administration.pdf
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-local-traffic-manager-implementations.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Node and pool member states: enable, disable, force offline

```
tmsh modify ltm node 10.1.20.11 session user-disabled         # disable: persistent + existing flows only
tmsh modify ltm node 10.1.20.11 session user-disabled state user-down   # force offline: existing connections only
tmsh modify ltm pool pool_web members modify { 10.1.20.11:80 { session user-enabled state user-up } }
tmsh show ltm pool pool_web members field-fmt
```
- Enabled: accepts new connections. Disabled (`session user-disabled`): receives only persistent sessions and existing connections; new, non-persistent ones skip it.
- Force offline (`state user-down`): lets established connections finish but accepts no new ones, including persistent ones.
- Availability reason fields: `offline` monitor-down vs `unavailable` disabled/user-down, and `parent-down` (node down).
- Disabling a node affects every pool containing that IP; disabling a member only that pool.
- To drain, wait until `tmsh show ltm pool pool_web members` shows 0 `cur-conns`; persistence entries may keep a client pinned for the persistence timeout (default 180 s cookie/source-addr 180 s in the default profile, confirm).
- Gotcha: a member set `user-disabled` is shown with a black diamond/"disabled" but still gets persistence hits; use force offline when the server is truly being removed.

Verify: `tmsh show ltm pool pool_web members` current connections fall to 0; `tmsh show ltm persistence persist-records` shows remaining pinned clients.
