---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.snat-automap
name: snat-automap
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, snat, automap, source-address-translation]
level: practitioner
status: draft
description: "Understand and configure SNAT on BIG-IP virtual servers: automap, SNAT pools, and when the default gateway design makes it unnecessary."
sources:
  - https://www.f5.com/pdf/certification/exams/blueprint-tmos-administration.pdf
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-local-traffic-manager-implementations.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SNAT and SNAT automap

```
tmsh modify ltm virtual vs_web source-address-translation { type automap }
tmsh create ltm snatpool snatpool_app members add { 10.1.20.200 10.1.20.201 }
tmsh modify ltm virtual vs_web source-address-translation { type snat pool snatpool_app }
tmsh list ltm virtual vs_web source-address-translation
```
- Without SNAT, the pool member sees the client IP and its return route must point to the BIG-IP; otherwise replies bypass it and clients reset. With SNAT, the member sees the BIG-IP self IP, so any route works, but source IP-based logging and ACLs lose the client (use X-Forwarded-For).
- `automap` uses a floating self IP on the egress VLAN if one exists (else the non-floating); this means failover moves the source address with the traffic group. Automap supports about 64k connections per destination address:port tuple, as source ports are the limit.
- `snat pool` adds more addresses to extend the port range for heavy traffic to one backend; traffic is spread across the pool.
- Gotcha: members on the same VLAN as the client can bypass the BIG-IP (member replies directly to client L2); SNAT is mandatory in that "one-armed" case.
- A SNAT with no available port logs "Cannot allocate port ... SNAT" in `/var/log/ltm`.

Verify: on a backend, `tcpdump -nn port 80` shows source = SNAT address. Port exhaustion is visible with `tmsh show sys connection | wc -l` and `tmsh show ltm snat-translation`.
