---
id: computing-software.networking-hardware-and-wireless.check-point.cpinfo-and-support-tools
name: cpinfo-and-support-tools
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, cpinfo, diagnostics, support-package]
level: practitioner
status: draft
description: "Collect cpinfo and the main diagnostic outputs Check Point Support asks for, with version, Jumbo, and log selection."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_CLI_ReferenceGuide/Default.htm
  - https://support.checkpoint.com/results/sk/sk98348
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# cpinfo and diagnostic collection

```
cpinfo -y all                       # collect with all products, scrubbed output
cpinfo -o /var/tmp/gw1.info -z
cp_info_collect                      # (confirm) alternative on some builds
fw ver ; cpinfo -v                   # version and hotfix level
installed_jumbo_take
cpwd_admin list
fw stat
```
- cpinfo creates an info file with configuration, OS versions and hotfixes; load it in the CPinfo viewer or attach to the SR. The `-y` flag assumes yes (the licence agreement prompt), and `-o` names the output.
- `installed_jumbo_take` prints the current Jumbo Hotfix take; compare against the latest take in the CPUSE recommended list.
- `cpwd_admin list` shows each process, state and restart count (`T` ok, `N` not running); a high `START`/restart count signals crash loops. Core files live under `/var/log/dump/usermode` and `/var/crash`.
- For kernel debugging tools (zdebug, fw monitor) see the drop-analysis skill. For packet capture to attach: `tcpdump` or `fw monitor -F`.
- Gotcha: cpinfo includes configuration data and IP addresses; review before attaching to a ticket, and avoid placing it on shared storage.

Verify: `ls -lh /var/tmp/*.info*`; open the file's header to confirm the product, take and hostname; `cpstat os -f all` gives basic hardware health.
