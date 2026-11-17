---
id: computing-software.systems-network-administration.patch-management.ios-xe-install-mode-upgrades
name: ios-xe-install-mode-upgrades
category: computing-software
field: systems-network-administration
product: patch-management
tags: [ios-xe-install-commit, ios-xe, install-mode, cisco-catalyst, network-device-patching, patch-management]
level: practitioner
status: docs-checked
description: "Upgrade Cisco IOS-XE in install mode: add/activate/commit workflow, auto-abort timer, cleaning flash, stacks, and converting from bundle mode safely."
sources:
  - https://www.cisco.com/c/en/us/support/docs/switches/catalyst-9300-series-switches/216231-upgrade-guide-for-cisco-catalyst-9000-sw.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IOS-XE install mode upgrades

Catalyst 9000 switches on IOS-XE should run in **install mode** (boot from `packages.conf`), not bundle mode (boot the `.bin` directly). Cisco calls install mode the newer, recommended mode: it supports rollback, boots faster and uses memory better. On the 9200, 9400 and 9600 it is the only option.

## Check mode and space
```text
show install summary
show run | include boot system
dir flash:
install remove inactive          ! lists what it will delete; also removes old .bin files, so run it before copying the new one
```

## Copy and verify image
```text
copy tftp://repo.example.com/cat9k_iosxe.17.12.04.SPA.bin flash:
! verify the image checksum against the value on the Cisco download page
```

## Three-step upgrade (preferred)
```text
install add file flash:cat9k_iosxe.17.12.04.SPA.bin
install activate auto-abort-timer 60     ! reloads; rolls back after 60 min (range 30-1200, default 120) unless committed
! after reload and checks:
install commit
```
One-shot alternative: `install add file flash:...bin activate commit` (add, activate and commit in one command). `install auto-abort-timer stop` stops the rollback timer.

## Rollback
- Before commit: `install abort` (or let the timer expire) returns to previous version.
- After commit: `install rollback to id <n>` (see `show install rollback`; `install label <n> label-name <name>` names a rollback point). You can only roll back to versions whose files are still on flash.

## Stacks and redundancy
A normal install upgrade of StackWise Virtual or a dual-sup chassis reloads both at once. Dual-sup chassis and StackWise Virtual can use ISSU (`install add file ... activate issu commit`), which needs install mode and starts reloading without a confirmation prompt; the 9200 and 9300 do not support ISSU. `reloadfast` (16.8.1 or later, install mode only) shortens downtime but is not supported when a microcode or FPGA upgrade is needed.

## Bundle to install conversion
```text
configure terminal
no boot system
boot system flash:packages.conf
end
write
install add file flash:cat9k_iosxe.17.12.04.SPA.bin activate commit
```

## Gotchas
- Do not change the boot statement to another .conf file mid-upgrade; it can make the upgrade fail. After `install add`, either activate the added package or clean it out and start again.
- Too little flash space blocks copying the .bin; `install remove inactive` clears unused files.
- A stack member in V-Mismatch state runs different software from the active; in install mode Cisco's guide resolves it with auto-upgrade (`software auto-upgrade enable` or `install autoupgrade`).

## Verify
`show version` shows the new release; `show install summary` shows the new package as Committed (C) and the auto abort timer inactive; interfaces, neighbours and routing tables match the pre-checks.

## Checked
2026-10-28. Confirmed against Cisco's Upgrade Guide for Cisco Catalyst 9000 Switches (install and bundle modes, add/activate/commit/abort, auto-abort-timer range and default, rollback by id and labels, packages.conf boot statement, ISSU and reloadfast limits, cleanup, V-Mismatch, `show install summary` states). Removed: ISR/ASR scope, `install rollback to committed`, md5 verify command, https copy, ROMMON, `write memory` and "Installation mode is INSTALL" wording (not in the guide); dead 17.9 configuration guide source (404).
Method: documentation only; no commands were run.
