---
id: computing-software.networking-hardware-and-wireless.juniper-junos.chassis-redundancy
name: chassis-redundancy
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, graceful-restart, gres, nsr, dual-re]
level: practitioner
status: draft
description: "Configure Junos graceful routing engine switchover, nonstop routing and commit synchronize on dual-RE systems."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GRES, NSR and dual-RE redundancy
Goal: survive a routing-engine failure without dropping routes.

```
set chassis redundancy graceful-switchover
set routing-options nonstop-routing
set system commit synchronize
set routing-options graceful-restart
set protocols layer2-control nonstop-bridging
```

```
user@host> show chassis routing-engine
user@host> request chassis routing-engine master switch
user@host> show task replication
```

- GRES keeps the forwarding plane running during RE failover. NSR keeps protocol state on the backup RE so neighbors see no flap.
- NSR requires GRES and `commit synchronize`.
- Graceful restart is a helper-based alternative and cannot be mixed casually with NSR (confirm on your release).

Gotcha: run `commit synchronize` as a permanent setting, else the backup RE has a stale config and NSR replication breaks. Test switchovers in maintenance windows.

Operational tip: after enabling GRES and NSR, test with `request chassis routing-engine master switch` in a window and watch neighbor states from an adjacent router to confirm no flap occurred.

## Verify
- `show task replication` shows each protocol `Complete`; `show system switchover` shows ready.
