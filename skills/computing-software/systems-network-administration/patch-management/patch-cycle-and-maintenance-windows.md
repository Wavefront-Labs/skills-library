---
id: computing-software.systems-network-administration.patch-management.patch-cycle-and-maintenance-windows
name: patch-cycle-and-maintenance-windows
category: computing-software
field: systems-network-administration
product: patch-management
tags: [patch-management, patching, vulnerability-management, maintenance-window, patch-tuesday, deployment-rings, pilot-group, cvss, epss, cisa-kev, rollback, unattended-upgrades, dnf-automatic, needrestart, wsus, intune, windows-autopatch, windows-update-for-business, configmgr, ansible, powershell-dsc, configuration-baseline, configuration-drift, change-management, livepatch, kpatch, monthly-patch-cycle]
level: practitioner
status: draft
description: "Run a patch cycle: rings and pilots, Patch Tuesday cadence, CVSS/EPSS/KEV prioritisation, maintenance windows, rollback, unattended-upgrades, WSUS/Intune, drift."
sources:
  - https://www.cisa.gov/known-exploited-vulnerabilities-catalog
  - https://www.first.org/epss/
  - https://wiki.debian.org/UnattendedUpgrades
  - https://learn.microsoft.com/en-us/windows/deployment/update/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Patch cycle and maintenance windows — fast for what is exploited, steady for the rest

**Goal:** a predictable monthly rhythm that patches the whole fleet with low breakage,
an emergency lane for actively exploited bugs, and baselines that stop configuration
drifting between cycles.

## 1. Inventory first
You cannot patch what you do not know about. Keep an asset list with OS, version, owner,
criticality, and patch group; reconcile it monthly against your RMM/MDM/CMDB and a
network scan. Unsupported OS versions (no more patches) go on a risk register with an
end date.

## 2. Rings
| Ring | Who | Delay after release | Purpose |
|---|---|---|---|
| 0 Test | lab VMs, IT-owned | day 0–1 | does it install and boot |
| 1 Pilot | ~5–10% across every hardware/app combination, incl. willing power users | day 2–3 | real-workload breakage |
| 2 Broad | most workstations and non-critical servers | day 7 | |
| 3 Critical | DCs, DBs, clustered/line-of-business servers | day 10–14, in windows | |

Pilot must be representative, not "IT's laptops only". Define a **halt condition** (e.g.
any P1 incident or >2% failed installs) that pauses promotion automatically.

## 3. Cadence and windows
- Microsoft releases on **Patch Tuesday** (second Tuesday of the month, ~10:00 US Pacific)
  with occasional out-of-band fixes. Many Linux vendors publish continuously; batch them
  into the same monthly cycle.
- Windows workstations: Windows Update for Business / **Intune** update rings
  (deferral days + deadline + grace period), or Windows Autopatch. Servers: WSUS or
  ConfigMgr, Azure Update Manager, or Ansible. WSUS is deprecated (no new features) but
  still supported at the time of writing; plan the move.
- Maintenance windows: fixed, published, agreed with owners (e.g. "Group B: 3rd Wednesday
  22:00–02:00"). Include time for reboot, verification and rollback inside the window.
- Clustered/HA services: patch one node at a time, drain first (cluster-aware updating,
  `kubectl drain`, load balancer pool removal).

## 4. Prioritise: not all criticals are equal
1. **CISA KEV listed** (known exploited) or vendor says "exploitation detected": emergency
   lane, internet-facing first, target 24–72 h. (US federal BOD 22-01 gives KEV items
   dated deadlines, often 2–3 weeks; treat as an upper bound.)
2. **High EPSS** (probability of exploitation in the next 30 days) plus internet exposure.
3. **CVSS** 9.0+ on exposed services; then the normal monthly cycle.
CVSS measures severity, not likelihood; a 9.8 in an unreachable component can wait for
the cycle, a 7.5 on your VPN appliance cannot. Firmware, hypervisors, network gear and
third-party apps (browsers, Java, PDF readers, VPN clients) need the same treatment as the OS.

## 5. Linux automation
```bash
# Debian/Ubuntu
sudo apt install unattended-upgrades && sudo dpkg-reconfigure -plow unattended-upgrades
# /etc/apt/apt.conf.d/50unattended-upgrades: security origin only on servers;
#   Unattended-Upgrade::Automatic-Reboot "false";  (reboot inside your window instead)
# RHEL/Rocky/Alma/Fedora
sudo dnf install dnf-automatic
# /etc/dnf/automatic.conf: upgrade_type = security, apply_updates = yes
sudo systemctl enable --now dnf-automatic.timer
```
Kernel and glibc/openssl updates need a reboot or service restarts:
`needrestart` (Debian/Ubuntu), `dnf needs-restarting -r` (RHEL), or check
`/var/run/reboot-required`. Live patching (Canonical Livepatch, kpatch) buys time; it does
not replace reboots.

## 6. Rollback
- Snapshot VMs immediately before patching (delete within 72 h); for physical/critical
  systems, confirm a recent backup.
- Windows: `wusa /uninstall /kb:<KB_NUMBER>` (not all updates are removable; servicing
  stack updates are not). Pause the ring in Intune/WSUS by declining or expiring approval.
- Linux: `dnf history undo <ID>`; on apt, pin and downgrade (`apt install pkg=<VERSION>`);
  keep the previous kernel and choose it at boot.
- Write the rollback trigger before the window: "if service health check fails 15 min
  after reboot, roll back".

## 7. Baselines and drift
Patching fixes code; configuration drifts independently. Define a baseline (CIS
Benchmarks or vendor security baselines) as code and enforce it:
- **Ansible:** idempotent playbooks run on a schedule; `ansible-playbook site.yml --check --diff`
  reports drift without changing anything.
- **PowerShell DSC / Azure Machine Configuration / Intune** for Windows; `Test-DscConfiguration`
  reports compliance.
Alert on drift, fix it in code, then re-apply; hand fixes on servers get overwritten
next run, which is the point.

## 8. Measure
Track per cycle: % of fleet compliant at day 14 and day 30, mean time to patch KEV items,
failed installs, rollbacks, and devices not reporting.

## Verify
- [ ] Every device is in a ring and the ring schedule is published.
- [ ] Pilot ring covers each hardware model and critical app.
- [ ] KEV-listed vulnerabilities have a separate, faster SLA and it is being met.
- [ ] Linux hosts auto-install security updates and pending reboots are tracked.
- [ ] Each window has a written rollback trigger and a tested rollback path.
- [ ] A drift check (`--check --diff` or DSC test) runs on a schedule and alerts.
