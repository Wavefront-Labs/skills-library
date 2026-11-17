---
id: computing-software.networking-hardware-and-wireless.check-point.gaia-clish-basics
name: gaia-clish-basics
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, clish, gaia, expert-mode]
level: practitioner
status: draft
description: "Navigate Gaia clish, save configuration, use expert mode safely and find where settings live."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_Gaia_AdminGuide/Default.htm
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_CLI_ReferenceGuide/Default.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Gaia clish and expert mode basics

```
clish
show configuration
set hostname gw1
set interface eth1 ipv4-address 10.1.10.1 mask-length 24 state on
set static-route default nexthop gateway address 10.1.10.254 on
save config
show asset all
show version all
exit
expert                         # prompts for the expert password
```
- `clish` is the restricted shell for Gaia OS settings. Changes apply immediately in memory but survive reboot only after `save config`. The WebUI saves automatically.
- `set expert-password` (clish) sets the expert password; `lock database override` takes the configuration lock from another session (`set` fails with "database locked" otherwise).
- Use `clish -c "show interfaces all"` or `clish -f script.txt` for scripting from expert mode; `clish -s` (not saving) vs normal save behaviour differs by version (confirm).
- Command completion: `?` and Tab. `show commands` lists everything available to your role; role-based access (RBA) limits which feature commands a user can run.
- Gotcha: expert mode is Linux bash with root rights, and editing files under `/etc` or `/opt/CPsuite*` by hand bypasses clish validation. Prefer clish for network settings; use `$FWDIR/conf` files only for documented tweaks.

Verify: `show configuration | grep hostname` before and after reboot; `cat /config/active` (expert) is the saved file that Gaia reloads at boot.
