---
id: computing-software.networking-hardware-and-wireless.check-point.securexl-acceleration
name: securexl-acceleration
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, securexl, fwaccel, acceleration-templates]
level: practitioner
status: draft
description: "Check SecureXL status, acceleration templates and F2F reasons with fwaccel and fw ctl affinity, and when to disable it temporarily."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_PerformanceTuning_AdminGuide/Default.htm
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_CLI_ReferenceGuide/Default.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SecureXL acceleration and fwaccel

```
fwaccel stat                  # status: enabled, accelerated blades, templates
fwaccel stats -s              # summary: accelerated/F2F/medium-path connections
fwaccel stats -p              # F2F (forward to firewall) reasons
fwaccel conns | head
fwaccel off ; fwaccel on      # temporary, maintenance only
fwaccel templates
```
- SecureXL accelerates established flows and connections matching **templates** (accept templates), through the SXL fast path; the rest go via the **medium path (PXL)** or the **slow path (F2F)** which uses the full firewall kernel.
- A low accelerated percentage in `fwaccel stats -s` suggests rules/blades prevent templates: Application Control, URL Filtering, rules with Time objects or Identity Awareness access roles, services with protocol handlers (e.g. FTP), and the "Hits Counter".
- Rule order tweak: place heavily used simple "Any service" rules before complex ones so templates are created. Rules with the `Anti-Bot`/`IPS` protections still pass via PXL.
- Disabling SecureXL with `fwaccel off` is for testing/troubleshooting only (e.g., fw monitor). Do not leave it off; CPU load may increase sharply.
- Gotcha: after policy install, templates are rebuilt; a spike in F2F immediately after is normal.

Verify: `fwaccel stats -s` shows accelerated conns percentage and `fwaccel stat` shows `Accelerator Status: on`.
