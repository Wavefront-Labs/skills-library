---
id: computing-software.systems-network-administration.keepalived.stop-and-respawn-behaviour
name: stop-and-respawn-behaviour
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, dont-release-vrrp, dont-release-ipvs, dont-respawn, shutdown, command-line]
level: advanced
status: docs-checked
description: "Options changing Keepalived stop and child-restart behaviour: -V keeps VIPs and routes, -I keeps the IPVS table, -R disables respawn of VRRP and checker children."
sources:
  - https://keepalived.readthedocs.io/en/latest/programs_synopsis.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stop and respawn behaviour

Defaults: on exit, VRRP VIPs and VROUTEs are removed and the IPVS virtual server table is cleared; VRRP and checker children are restarted if they exit.

| Option | Changes |
|---|---|
| `-V`, `--dont-release-vrrp` | On stop, leave VIPs and VROUTEs in place |
| `-I`, `--dont-release-ipvs` | On stop, leave the IPVS topology in place |
| `-R`, `--dont-respawn` | Do not restart the VRRP and checker children when they exit |

Use `-V` or `-I` only when you deliberately want addresses or the IPVS table to survive a daemon stop, for example during a controlled restart; otherwise stale VIPs can remain on a node that is no longer MASTER.

Verify: after stopping the daemon, ip address and the IPVS table show exactly what you intended to keep or remove.

## Checked

2026-11-04. Confirmed the -V, -I and -R options and the stated defaults on the Keepalived programs synopsis page. The closing caution about stale VIPs is the author's reasoning, not page text. Nothing removed.

Method: documentation only; no commands were run.
