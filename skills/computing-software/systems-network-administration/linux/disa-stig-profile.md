---
id: computing-software.systems-network-administration.linux.disa-stig-profile
name: disa-stig-profile
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, disa-stig, stig-profile, stig, stig-viewer, ckl, cat-i, fips, oscap, scap-security-guide, rhel, compliance, security, sysadmin]
level: advanced
status: draft
description: "Apply and evidence the DISA STIG on RHEL-family or Ubuntu: STIG profile at install, oscap scan and remediation, CAT I/II/III triage, FIPS mode, and producing checklists for STIG Viewer."
sources:
  - https://public.cyber.mil/stigs/
  - https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/security_hardening/scanning-the-system-for-configuration-compliance-and-vulnerabilities_security-hardening
  - https://complianceascode.readthedocs.io/en/latest/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DISA STIG profile on Linux

**Goal:** a host that meets the DISA Security Technical Implementation Guide for its OS,
with scan evidence and a checklist the assessor accepts.

## 1. Build it in from install
- RHEL Anaconda: "Security Policy" spoke → DISA STIG profile; Kickstart:
```
%addon com_redhat_oscap
    content-type = scap-security-guide
    profile = xccdf_org.ssgproject.content_profile_stig
%end
```
  This applies partition layout and settings at install (separate `/var`, `/var/log`, `/var/log/audit`, `/tmp`, `/home`).
- STIG with GUI: profile `stig_gui`.
- Ubuntu: Ubuntu Pro `usg fix disa_stig` (Canonical-supplied content).
Retrofitting partitioning later is painful; get it right at install.

## 2. Scan and remediate
```bash
DS=/usr/share/xml/scap/ssg/content/ssg-rhel9-ds.xml
oscap xccdf eval --profile stig --results stig.xml --report stig.html $DS
oscap xccdf generate fix --profile stig --fix-type ansible $DS > stig.yml
```
DISA also publishes its own SCAP benchmark zips (`U_RHEL_9_V*_STIG_SCAP_*_Benchmark.zip`) — use them for the official
assessment; SSG content tracks them closely and gives automation.

## 3. Triage by category
- **CAT I** (high): fix immediately — e.g. no blank passwords, FIPS, no `rsh`/`telnet`, SSH root login, unsigned packages (`gpgcheck=1`).
- **CAT II** (medium): bulk of the work — auditd rules, PAM settings, banners, session timeout, USB storage.
- **CAT III** (low): fix where cheap; document the rest.
Each finding not fixed needs a POA&M entry or a documented "not applicable".

## 4. FIPS mode
```bash
fips-mode-setup --enable && reboot        # RHEL 8/9; RHEL 10: enable at install (fips=1 boot option)
fips-mode-setup --check
update-crypto-policies --show              # FIPS (or FIPS:OSPP)
```
FIPS changes crypto behaviour: MD5 disallowed, some SSH keys/ciphers rejected, apps with bundled crypto may fail. Test first.

## 5. Checklist evidence
Import the XCCDF results into DISA **STIG Viewer** (3.x) to produce a `.ckl`/`.cklb` checklist;
add manual-check findings (policy, procedures) by hand. Keep: scan date, content version, host, reviewer.

## Gotchas
- STIG banner + `TMOUT` + session lock break unattended automation logins unless service accounts are handled.
- `fapolicyd` (application allowlisting) and USBGuard are STIG items on RHEL 9 — roll out in permissive/trust-building mode first.
- Audit rules volume: STIG audit rules can generate GBs/day on busy hosts; size `/var/log/audit` and forward logs.

## Verify
- [ ] STIG scan shows zero CAT I failures; every remaining CAT II/III fail has a POA&M or N/A justification.
- [ ] `fips-mode-setup --check` reports enabled (if required); STIG Viewer checklist exported and stored with the scan results.
