---
id: computing-software.systems-network-administration.cisco-networking.show-tech-support-and-crashinfo-for-tac
name: show-tech-support-and-crashinfo-for-tac
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ios-xe, show-tech-support, crashinfo, core-dump, tac-case, system-report, troubleshooting]
level: practitioner
status: draft
description: "Collect what Cisco TAC needs after a crash or fault: show tech-support variants to file, crashinfo and system-report archives, core files, and safe off-box transfer."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ios-nx-os-software/ios-xe-16/216095-collect-system-report-and-core-files-on.html
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sys_mgmt/b_179_sys_mgmt_9300_cg.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# show tech-support and crash files for TAC

A TAC case moves at the speed of the first data upload. Collect before you reload: a reload
destroys buffers, counters and process state that explain the fault.

## Before touching anything
```
show clock
show version | include uptime|reason|System image
show logging | redirect bootflash:pre-reload-log.txt
```
`Last reload reason` in `show version` tells you if it was a crash (`Critical software exception`,
`Watchdog`), a power loss, or a manual reload.

## show tech to a file (never to the terminal)
```
show tech-support | redirect bootflash:R1-tech-20261018.txt
```
Feature-specific variants are smaller and often what TAC actually wants:
```
show tech-support platform          ! Catalyst/ASR forwarding plane
show tech-support wireless          ! 9800 WLC
show tech-support ipsec
show tech-support cef
show tech-support diagnostic
```
On a large chassis plain `show tech` can take minutes and spike CPU; run it off-peak or use the
feature variant. Always `redirect`; a VTY session timeout mid-output loses everything.

## Crash artefacts on IOS XE
```
dir bootflash:core/          ! *.core.gz process cores, system-report_*.tar.gz
dir crashinfo:               ! crashinfo_RP_00_00_<date>, tracelogs
request platform software trace archive    ! packs btrace logs into a .tar.gz
```
The `system-report_*.tar.gz` bundles cores, tracelogs and crashinfo; upload it whole. On classic IOS
the file is `crashinfo:crashinfo_<date>` or `flash:crashinfo`.

## Move files off the box
```
copy bootflash:core/system-report_RP_0_20261018-0412-UTC.tar.gz scp://user@10.0.0.30/tac/
copy bootflash:R1-tech-20261018.txt ftp://user:pw@10.0.0.30/tac/
```
Or upload straight to the case: Cisco's CXD (Customer eXperience Drive) accepts SCP/HTTPS uploads
with the case number as username and a per-case token.

## Gotchas
- Free space: a core file can be hundreds of MB. Check `dir bootflash: | include free` and delete
  old images first (`install remove inactive` in install mode).
- Stacks: collect from the active member; cores for other members live on their own flash
  (`dir flash-2:core/`).
- Remove passwords before sharing with non-Cisco parties; show tech masks most secrets but
  `show running` pasted elsewhere does not.
- Tracelogs roll quickly; archive them within hours of the event.

## Verify
- [ ] Files copied off-box and sizes match `dir` output.
- [ ] TAC case has: show tech, last reload reason, timeline of the event, system-report if a crash.
