---
id: computing-software.systems-network-administration.linux.openscap-oscap-scan
name: openscap-oscap-scan
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, openscap, oscap, scap-security-guide, ssg, xccdf, datastream, compliance-scan, oscap-ssh, tailoring, rhel, security, hardening, sysadmin]
level: practitioner
status: docs-checked
description: "Scan Linux hosts for compliance with OpenSCAP: install scap-security-guide, list profiles in the datastream, run oscap xccdf eval locally or over SSH, tailoring, and reading results."
sources:
  - https://github.com/OpenSCAP/openscap/blob/main/docs/manual/manual.adoc
  - https://github.com/OpenSCAP/openscap/blob/main/utils/oscap.8
  - https://github.com/OpenSCAP/openscap/blob/main/utils/autotailor.8
  - https://github.com/ComplianceAsCode/content/tree/master/products/rhel9/profiles
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenSCAP scanning with oscap

**Goal:** measure a host against a baseline (CIS, STIG, PCI-DSS, ANSSI…) with the
standard SCAP content and get a pass/fail list you can act on.

## 1. Install content
```bash
dnf install openscap-scanner scap-security-guide        # RHEL/Fedora
apt install openscap-scanner                             # Debian/Ubuntu; content comes from your distro's SCAP Security Guide package or a ComplianceAsCode release
ls /usr/share/xml/scap/ssg/content/                      # ssg-rhel9-ds.xml etc. (datastreams; the OpenSCAP manual uses this path)
```
Use the datastream matching the OS release exactly. Profile names differ per product: RHEL 9 has `cis_server_l1`, `cis`, `stig`, `pci-dss`, `ospp`, `anssi_bp28_high`; Ubuntu 24.04 and Debian 12 content use names such as `cis_level1_server` (check with `oscap info`).

## 2. Find profiles
```bash
DS=/usr/share/xml/scap/ssg/content/ssg-rhel9-ds.xml
oscap info $DS                                   # lists profile IDs and titles
oscap info --profile cis_server_l1 $DS           # profile description
oscap info --profile cis_server_l1 --list-rules $DS   # rules (--list-vars lists variables; both need --profile)
```
Full IDs look like `xccdf_org.ssgproject.content_profile_cis_server_l1`; the short suffix (`cis_server_l1`) works for `--profile`.

## 3. Scan
```bash
oscap xccdf eval --profile cis_server_l1 \
  --results-arf /var/tmp/results-arf.xml --report /var/tmp/report.html \
  --oval-results $DS
echo $?            # 0 = all rules pass, 2 = at least one rule fail or unknown, 1 = error
```
`--results-arf` is the option the oscap man page recommends over `--results` for data streams.
Remote scan from an admin host (OpenSCAP must be installed on the target; the tool copies the content over SSH):
`oscap-ssh root@host 22 xccdf eval --profile stig --report report.html $DS`.
Container images: `oscap-podman <image-id> xccdf eval --profile ... $DS` (Fedora and RHEL 8 or newer; use `oscap-docker` elsewhere).

## 4. Tailoring
Disable rules that don't apply or change values (password length, etc.) without forking content:
- SCAP Workbench (GUI) → save a tailoring file, or `autotailor` (part of the `openscap-utils` package):
```bash
autotailor --unselect partition_for_var_tmp \
  --var-value var_password_pam_minlen=16 \
  --output tailoring.xml $DS cis_server_l1
oscap xccdf eval --tailoring-file tailoring.xml --profile cis_server_l1_customized ...
```
`autotailor` accepts full or suffix-only rule and variable IDs, and names the new profile `<base profile>_customized` unless you pass a new profile ID.
Record why each rule was unselected — auditors ask.

## 5. Read results
```bash
oscap xccdf generate report /var/tmp/results-arf.xml > report.html     # regenerate HTML from ARF results
```
The HTML report gives per-rule rationale, check details and remediation snippets (bash/Ansible).

## Gotchas
- Run scans off-peak: some rules examine the whole filesystem, so they can take a while.
- "notapplicable" is reported for rules that do not apply to the platform; "notchecked" means no check could be evaluated (a check engine OpenSCAP does not support, or a rule with no check implemented), so it needs manual evidence.
- Results only compare to the content version; update scap-security-guide when the benchmark revs.

## Verify
- [ ] `oscap info` shows the expected profile; the scan exits 0 or 2 (not 1) and produces both the ARF results and the HTML report.
- [ ] Score and fail list are archived with the date and content version for comparison after remediation.

## Checked

Checked 2026-10-26 against OpenSCAP/openscap (last commit 2026-10-22: docs/manual/manual.adoc, utils/oscap.8, utils/autotailor.8) and ComplianceAsCode/content (last commit 2026-10-23: products/*/profiles). Confirmed: datastream path, oscap info with --profile, --list-rules and --list-vars, short profile IDs, --results-arf, --report and --oval-results options, autotailor options and package, oscap-ssh and oscap-podman behaviour, notchecked meaning, rhel9 profile names. Corrected: exit status 2 covers fail or unknown results; autotailor takes suffix IDs and --new-profile-id; ARF is recommended over --results; profile names differ on Debian and Ubuntu. Removed: the autotailor 1.3.8 version gate, Debian ssg package names, the Ubuntu Pro usg remark and the grep-based failure count.

Method: documentation only; no commands were run.
