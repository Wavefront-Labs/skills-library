---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.licensing-and-provisioning
name: licensing-and-provisioning
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, license, provisioning, sys-provision]
level: practitioner
status: draft
description: "Activate a BIG-IP license from the CLI and provision modules with correct resource levels, then verify with tmsh."
sources:
  - https://www.f5.com/pdf/certification/exams/blueprint-tmos-administration.pdf
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-system-initial-configuration.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Licensing and module provisioning

```
tmsh show sys license
get_dossier -b <REGKEY>            # offline: paste the dossier at the F5 activation site
tmsh install sys license file /var/tmp/license.txt
tmsh restart sys service tmm       # or: reloadlic
tmsh list sys provision
tmsh modify sys provision asm level nominal
tmsh modify sys provision ltm level nominal
tmsh save sys config
```
- `SOL`: online activation needs outbound HTTPS from the management interface; otherwise use the dossier method.
- Levels: `none`, `minimum`, `nominal`, `dedicated`. Total allocation is limited by CPU and memory; the unit rejects over-commitment. `dedicated` starves other modules.
- Provisioning a module restarts services and the box can stop passing traffic for minutes; do it in a window on standby first. `tmsh show sys mem` before and after.
- After the licence expires/renews, run `reloadlic`; new add-on keys appear only after reactivation.
- Gotcha: HA peers must carry compatible licence modules or sync warns of module mismatches; hostname changes do not need relicensing, but a base MAC change does.

Verify: `tmsh show sys license` lists active modules and a service check date after activation; `tmsh show sys provision` shows the new levels; `tmsh show sys mem` shows no module memory shortfall.
