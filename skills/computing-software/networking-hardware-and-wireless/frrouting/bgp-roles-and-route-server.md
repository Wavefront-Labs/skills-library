---
id: computing-software.networking-hardware-and-wireless.frrouting.bgp-roles-and-route-server
name: bgp-roles-and-route-server
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, bgpd, route-server, bgp-roles, otc, rfc9234, ixp]
level: advanced
status: docs-checked
description: "Configure FRR as a BGP route server with route-server-client and per-client import and export policy, and set RFC 9234 BGP roles with local-role."
sources:
  - https://docs.frrouting.org/en/latest/bgp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP roles and route server
Route server:
- `neighbor PEER-GROUP|A.B.C.D|X:X::X:X route-server-client` marks an RS-client. It enables transparent mode (no AS-path, next-hop or MED changes) and creates a dedicated Loc-RIB per client.
- `neighbor <peer> route-map WORD in|out` sets the import (in) or export (out) policy for an RS-client.
- `match peer A.B.C.D|X:X::X:X`: in import maps it matches the sending peer; in export maps it matches the RS-client receiving into its Loc-RIB.
- `call WORD` jumps to another route-map; depending on that route-map's result, the original one continues or not.
- Announcements from normal (non-RS-client) peers are also considered for every RS-client's Loc-RIB without passing an export policy; RS-clients do not receive announcements from the main Loc-RIB.

Roles (RFC 9234, Only to Customers):
- `neighbor PEER local-role LOCAL-ROLE [strict-mode]` where role is `provider`, `rs-server`, `rs-client`, `customer` or `peer`; with `strict-mode` the session does not establish until the neighbor sets its role too (otherwise a Role Mismatch notification is sent). Default: disabled.
- Setting a local-role automatically enables the Only to Customer (OTC) attribute handling, which helps detect and mitigate route leaks. Pairs are Provider-Customer, Peer-Peer and RS-Server-RS-Client.

ASPA verification direction is set by route-map (`match aspa`), not derived from local-role; the docs call the two features deliberately independent.

## Checked

2026-11-09. Read the FRR BGP page sections "BGP Roles" (local-role, strict-mode, OTC), "Route Server" (route-server-client, route-map in/out, match peer, call) and the ASPA direction note via a local text copy. Removed: `match src-peer` (not in the docs), `bgp reject-as-sets` and `bgp default-originate` (unrelated here; the docs also give conflicting defaults for reject-as-sets).
Method: documentation only; no commands were run.
