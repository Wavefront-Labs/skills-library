---
id: computing-software.networking-hardware-and-wireless.check-point.cpwd-services-and-restart
name: cpwd-services-and-restart
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, cpwd-admin, cpstop-cpstart, fwd]
level: practitioner
status: draft
description: "Restart Check Point services correctly, read the watchdog list, and know which service restart disrupts traffic."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_CLI_ReferenceGuide/Default.htm
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_Gaia_AdminGuide/Default.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Check Point services: cpstop, cpstart and cpwd_admin

```
cpwd_admin list                      # APP, PID, STAT, #START, START_TIME
cpstop ; cpstart                     # all Check Point processes (traffic impact!)
cpstop -fwflag -proc                 # stop processes but keep the policy loaded (keeps firewall running)
fwm ver ; api restart                # management side
cpwd_admin stop -name FWM -path "$FWDIR/bin/fw" -command "fw kill fwm"
cpwd_admin start -name FWM -path "$FWDIR/bin/fwm" -command "fwm"
fwd -n ; fw kill fwd                 # watchdog restarts fwd
```
- `cpwd` is the Check Point WatchDog: it starts, monitors and restarts processes (`fwd`, `fwm`, `cpd`, `cpm`, `cvpnd`, `vpnd`). `cpwd_admin list` columns: STAT `E` = executing, `T` = terminated, `N` = not running; `#START` counts restarts, so a high count marks a crash loop.
- `cpstop` stops the firewall and **unloads policy** (the gateway forwards without filtering unless IP forwarding is off; on a Gaia gateway, "default filter" policy applies, which blocks inbound except management). Never run on a production gateway without a plan; use `cpstop -fwflag -proc` for a service-only stop if documented for your task.
- Management-only restarts: `api restart` for the Management API; `cpstop; cpstart` on a management server affects SmartConsole connections only, not gateway traffic.
- Specific logs: `$FWDIR/log/fwd.elg`, `$CPDIR/log/cpd.elg`, `$FWDIR/log/cpm.elg`.
- Gotcha: after `cpstop` on a cluster member, ClusterXL goes `Down` on that member; make sure the peer is Active first.

Verify: `cpwd_admin list` shows all `E` and counters stable; `cphaprob stat` and `fw stat` confirm normal operation.
