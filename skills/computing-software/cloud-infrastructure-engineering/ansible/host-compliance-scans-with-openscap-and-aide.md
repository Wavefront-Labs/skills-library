---
id: computing-software.cloud-infrastructure-engineering.ansible.host-compliance-scans-with-openscap-and-aide
name: host-compliance-scans-with-openscap-and-aide
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, drift-detection, compliance-scan, openscap, aide, scap-security-guide, cis-benchmark, file-integrity, rhel-system-roles]
level: advanced
status: draft
description: "Detect host configuration drift and compliance gaps with Ansible-driven OpenSCAP (SSG profiles, reports, remediation playbooks) and AIDE file integrity checks."
sources: ["RHEL 9 Security hardening - Scanning the system for configuration compliance (https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/security_hardening/)", "ComplianceAsCode / SCAP Security Guide project (https://github.com/ComplianceAsCode/content)", "aide(1) and aide.conf(5) man pages; rhel-system-roles aide role documentation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Host compliance scans with OpenSCAP and AIDE

Goal: know continuously whether hosts still meet the hardening baseline (CIS, STIG, PCI-DSS)
and whether critical files changed outside of automation.

## OpenSCAP with SCAP Security Guide
```yaml
- hosts: rhel
  become: true
  vars:
    scap_profile: xccdf_org.ssgproject.content_profile_cis_server_l1
    scap_ds: /usr/share/xml/scap/ssg/content/ssg-rhel9-ds.xml
  tasks:
    - ansible.builtin.dnf: {name: [openscap-scanner, scap-security-guide], state: present}
    - name: Scan
      ansible.builtin.command: >
        oscap xccdf eval --profile {{ scap_profile }}
        --results /var/tmp/scap-results.xml --report /var/tmp/scap-report.html {{ scap_ds }}
      register: scan
      changed_when: false
      failed_when: scan.rc not in [0, 2]       # 2 = some rules failed (not an error)
    - ansible.builtin.fetch: {src: /var/tmp/scap-report.html, dest: "reports/{{ inventory_hostname }}.html", flat: true}
    - ansible.builtin.fetch: {src: /var/tmp/scap-results.xml, dest: "reports/{{ inventory_hostname }}.xml", flat: true}
```
List profiles: `oscap info /usr/share/xml/scap/ssg/content/ssg-rhel9-ds.xml`.
Score/fail counts for dashboards: parse the results XML (`rule-result/result` = `fail`) or use
`oscap xccdf generate report`.

## Remediation as Ansible
SSG ships per-profile playbooks: `/usr/share/scap-security-guide/ansible/rhel9-playbook-cis_server_l1.yml`.
Or generate from scan results (only the failed rules):
```bash
oscap xccdf generate fix --fix-type ansible --result-id "" --output remediate.yml /var/tmp/scap-results.xml
```
Review before running: some rules (partitioning, FIPS, disabling services) break workloads.
Prefer moving accepted controls into your own roles and keeping the scan as the check.

## AIDE file integrity
```yaml
- ansible.builtin.dnf: {name: aide, state: present}
- name: Initialise database (once, after hardening)
  ansible.builtin.command: aide --init
  args: {creates: /var/lib/aide/aide.db.new.gz}
- ansible.builtin.copy: {src: /var/lib/aide/aide.db.new.gz, dest: /var/lib/aide/aide.db.gz, remote_src: true, force: false}
- name: Check
  ansible.builtin.command: aide --check
  register: aide
  changed_when: false
  failed_when: aide.rc >= 8          # bits 1/2/4 = added/removed/changed files; >=8 = error
```
`rhel-system-roles.aide` (newer RHEL releases) wraps init/check/update. After every *intended*
change (patching), run `aide --update` and rotate the DB, or every patch day becomes an alert.
Keep a copy of the DB off-host; an attacker with root can rewrite the local one.

## Schedule and report
Run scans weekly from the controller, publish reports, and alert on new failures compared with
the previous run (diff the failed rule IDs), not on the absolute number.

## Gotchas
- Scanning containers/VMs with different OS versions needs the matching datastream (`ssg-rhel8-ds.xml` vs rhel9).
- `oscap` returns 2 when rules fail; treat only 1 as a tool error.
- AIDE on busy dirs (`/var/log`, `/tmp`) produces noise; tune `aide.conf` to watch binaries and config only.

## Verify
- [ ] Reports exist for every host; the failed-rule count trends down after remediation.
- [ ] Editing a watched file (e.g. `/etc/ssh/sshd_config`) by hand makes the next AIDE check report it.
