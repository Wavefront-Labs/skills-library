---
id: computing-software.systems-network-administration.linux.cis-benchmark-remediation
name: cis-benchmark-remediation
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, cis-benchmark, cis-remediation, hardening-playbook, oscap-remediate, ansible-lockdown, usg, compliance, hardening, security, sysadmin]
level: advanced
status: draft
description: "Bring Linux hosts to a CIS Benchmark level safely: generating remediation from SCAP content, Ansible hardening roles, the controls that break things, exceptions, and rescanning."
sources:
  - https://www.cisecurity.org/cis-benchmarks
  - https://static.open-scap.org/openscap-1.3/oscap_user_manual.html
  - https://complianceascode.readthedocs.io/en/latest/
  - https://ubuntu.com/security/certifications/docs/usg
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CIS Benchmark remediation

**Goal:** move a fleet from "scanned, 60 % pass" to the agreed CIS level with automation,
documented exceptions, and no outage caused by hardening.

## 1. Decide scope first
- Level 1 (Server/Workstation): low-impact, broadly applicable. Level 2: defence-in-depth, more breakage risk.
- Write down the exceptions process before touching hosts (owner, reason, compensating control, review date).
- Baseline scan (`oscap xccdf eval --profile cis_server_l1 ...`) and keep the report.

## 2. Remediation sources (pick one per fleet)
**From SCAP content (exactly matches the scan):**
```bash
DS=/usr/share/xml/scap/ssg/content/ssg-rhel9-ds.xml
oscap xccdf generate fix --profile cis_server_l1 --fix-type ansible $DS > cis-l1.yml
oscap xccdf generate fix --profile cis_server_l1 --fix-type bash    $DS > cis-l1.sh
# fix only what failed on a given host:
oscap xccdf generate fix --fix-type ansible --result-id <RESULT_ID> /var/tmp/results.xml > fix-failed.yml   # the TestResult id inside the results file
```
Profile ids differ per content file; the OpenSCAP manual shows both short ids and full `xccdf_org.ssgproject.content_profile_*` ids, so confirm the id in your data stream before use.
**Ubuntu Pro:** the Ubuntu Security Guide (`usg`) audits and applies CIS profiles; see the USG documentation for profile names.
**Community roles:** public Ansible roles for the CIS benchmarks exist, usually with per-control toggles in variables.
Avoid `oscap xccdf eval --remediate` on production: it fixes everything in place with no review.

## 3. Roll out safely
1. Run in `--check --diff` on a canary host per role (web, db, bastion).
2. Apply to canaries; run the service's smoke tests and a reboot.
3. Expand in waves; rescan after each.

## 4. Controls that commonly break things
| Control | Breaks | Mitigation |
|---|---|---|
| Separate `/tmp`, `/var/tmp` with `noexec` | installers, some JVM/npm builds | per-app `TMPDIR`, exception |
| Disable unused filesystems (`cramfs`, `squashfs`, `udf`, `vfat`) | snaps (squashfs), UEFI ESP (vfat) | keep `vfat` on UEFI, `squashfs` with snaps |
| SSH: `AllowGroups`, `MaxAuthTries`, ciphers | automation accounts, old clients | add service groups first |
| Password/lockout (`pam_faillock`) | service accounts locked by scanners | exclude system accounts, monitor |
| auditd `-e 2` immutable rules | rule changes need a reboot | stage rules before enabling |
| Firewall default deny | monitoring, backups | open from inventory, not guesses |
| `sysctl` IP forwarding off | containers, VPN gateways | role-based exception |

## 5. Rescan and report
```bash
oscap xccdf eval --profile cis_server_l1 --tailoring-file exceptions.xml --results after.xml --report after.html $DS
```
Model exceptions as tailoring (unselected rules with reasons) so the report reflects reality.

## Gotchas
- CIS PDFs are licensed; reference control IDs, don't redistribute text.
- Benchmarks are version-specific (e.g. "CIS RHEL 9 v2.0.0"); record which version you meet.
- Re-apply on a schedule (config drift) — Ansible in check mode weekly or a scan in CI for images.

## Verify
- [ ] Post-remediation scan reaches the target score with every remaining fail covered by a documented exception.
- [ ] Canary services pass smoke tests and survive reboot; no hardening-related tickets after each wave.
