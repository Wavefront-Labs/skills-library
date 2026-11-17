---
id: computing-software.systems-network-administration.patch-management.patch-testing-and-rollback-strategy
name: patch-testing-and-rollback-strategy
category: computing-software
field: systems-network-administration
product: patch-management
tags: [patch-management, patch-testing, smoke-test, health-check, test-matrix, canary, synthetic-monitoring, rollback, roll-forward, rollback-plan, irreversible-change, servicing-stack-update, ssu, lcu, combined-cumulative-update, dism-remove-package, wusa, known-issue-rollback, kir, release-health, snapshot-revert, usn-rollback, vm-generation-id, boot-environment, zfs, btrfs, snapper, rpm-ostree, dnf-history, apt-pinning, ios-xe-install-mode, auto-abort-timer, firmware-anti-rollback, blue-green]
level: advanced
status: draft
description: "Test patches with a hardware/app matrix and scripted smoke checks, know which updates cannot be undone (SSU, firmware, schema), and pick the right rollback: redeploy, snapshot, DISM, boot environment."
sources:
  - https://learn.microsoft.com/en-us/windows/release-health/
  - https://learn.microsoft.com/en-us/windows/deployment/update/servicing-stack-updates
  - https://docs.fedoraproject.org/en-US/fedora-coreos/
  - https://www.cisco.com/c/en/us/support/ios-nx-os-software/ios-xe-17/series.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Patch testing and rollback strategy — prove it works, and know before you start whether you can undo it

**Goal:** catch a bad patch in the test ring with evidence, not "nobody complained", and
have a rollback that actually works for *this* kind of update. Ring structure, cadence
and windows are in
`computing-software.systems-network-administration.patch-management.patch-cycle-and-maintenance-windows`.

## 1. Build a test matrix, not a test box
List the combinations that matter and make sure each has at least one patched system in
the first ring:
- OS build × hardware model (drivers and firmware break per model);
- line-of-business apps, especially anything with kernel drivers: EDR/AV, VPN clients,
  backup agents, storage multipath, GPU and printer drivers;
- roles: domain controller, SQL, IIS/web, file server, hypervisor host, Citrix/RDS;
- network gear: one device per platform/model and feature set (e.g. the switch that also
  runs routing and NAC).
Each row has a named owner who signs off.

## 2. Script the smoke test
Run the same checks before and after on every test system, and compare:
```powershell
# Windows example: services, recent errors, an app transaction
Get-Service | Where {$_.StartType -eq 'Automatic' -and $_.Status -ne 'Running'}
Get-WinEvent -FilterHashtable @{LogName='System';Level=1,2;StartTime=(Get-Date).AddHours(-1)}
Invoke-WebRequest https://app01.corp.example/health -UseBasicParsing | Select StatusCode
```
```bash
# Linux example
systemctl --failed
journalctl -p err -b
needrestart -b                         # services still running old libraries
curl -fsS https://app01.corp.example/health
```
Also check: boot time, authentication (Kerberos/LDAP/SSO login), printing, VPN connect,
backup job success, and a performance baseline for heavy servers. Keep scripts in Git and
make the result a pass/fail gate for promoting the ring.

Read the vendor's known-issues page first (Windows release health, distro errata, Cisco
field notices). Many "bad patches" are already documented within 48 h.

## 3. Classify reversibility before the window
| Update type | Reversible? | Rollback route |
|---|---|---|
| App/package update | usually | package downgrade, redeploy |
| Windows LCU (combined with SSU since 2021) | partly | `wusa /uninstall` does **not** work on the combined package; use `DISM /Online /Get-Packages` then `DISM /Online /Remove-Package /PackageName:<Package_for_RollupFix~...>`. The SSU part stays. |
| Servicing stack update | **no** | none; test well |
| Linux kernel | yes | boot the previous kernel (keep ≥2 installed) |
| BIOS/UEFI, BMC, NIC/HBA firmware | often **no** (anti-rollback on some platforms; unconfirmed per vendor) | vendor recovery image; check release notes |
| Secure Boot DBX/revocation updates | effectively no | re-image media may be needed |
| DB schema / app data migrations | **no** without restore | backup + tested restore, or roll forward |
| AD schema / functional level | **no** (functional level raise reversible only in narrow cases) | forest recovery |
Anything marked "no" needs a full backup and a longer pilot, and the change record must
say "roll forward only".

## 4. Pick the rollback mechanism (best first)
1. **Redeploy the previous image** (immutable/containers, golden images, blue-green):
   fastest, cleanest. Keep the last known-good image tagged.
2. **Boot environments / filesystem snapshots:** ZFS boot environments, btrfs + snapper,
   `rpm-ostree rollback` (Fedora CoreOS/RHEL image mode). Reboot back into the old OS.
3. **VM snapshot revert:** fine for stateless servers. Not for domain controllers without
   VM-Generation ID support (USN rollback) or for databases and anything that replicates
   or takes writes after the snapshot (you lose those writes). Remove snapshots within
   ~72 h.
4. **Uninstall/downgrade:** `DISM /Remove-Package`, `dnf history undo <ID>`,
   `apt install pkg=<VERSION>` with pinning so it is not re-upgraded overnight.
5. **Network gear:** IOS-XE install mode
   (`install add file flash:<IMAGE> activate auto-abort-timer 30` then `install commit`)
   reverts automatically if you lose access and never commit; `install rollback to committed`.
6. **Microsoft Known Issue Rollback (KIR):** for non-security regressions Microsoft may
   ship a KIR that disables the change via policy; check before uninstalling the LCU.

## 5. Decide roll back vs roll forward
Write the trigger before you start: "roll back if health check fails 15 min after reboot,
or any P1 in the first 2 h". Roll forward (hotfix, config workaround, newer package) when:
the update is irreversible, it fixes an actively exploited vulnerability, or the vendor has
a fix out. Time-box the troubleshooting (e.g. 30 min in the window) before executing the
rollback.

## 6. After a rollback
- Block the update from re-installing (WSUS decline, Intune pause/expedite rules, `apt-mark
  hold`, `dnf versionlock`).
- Record the compensating control if the update was security-relevant, and set a
  re-test date.
- Feed the failure into the test matrix so the next run would have caught it.

## Verify
- [ ] Test matrix covers every hardware model, kernel-driver app and server role in production.
- [ ] Smoke-test scripts ran before and after; the diff is the gate evidence.
- [ ] Each update in the window classified reversible / not; irreversible ones have backups.
- [ ] Rollback method chosen and rehearsed in test for each class.
- [ ] Rolled-back updates are held and have a re-test date.
