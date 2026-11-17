---
id: computing-software.systems-network-administration.linux.patch-compliance-reporting
name: patch-compliance-reporting
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, patch-compliance-report, patch-management, security-updates, dnf-updateinfo, apt-security, fleet-reporting]
level: practitioner
status: draft
description: "Report patch status across a Linux fleet: pending security updates per host (dnf updateinfo, apt), kernel and reboot state, aggregating with Ansible, and an SLA-based report."
sources:
  - https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/managing_software_with_the_dnf_tool/assembly_updating-rhel-9-content_managing-software-with-the-dnf-tool
  - https://manpages.debian.org/bookworm/apt/apt-get.8.en.html
  - https://docs.ansible.com/ansible/latest/collections/ansible/builtin/package_facts_module.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Patch compliance reporting

**Goal:** answer "which hosts are missing critical/important security updates older than our SLA, and
which need a reboot?" with evidence.

## Per-host data points
RHEL/Fedora:
```bash
dnf updateinfo summary --security
dnf updateinfo list --security --sec-severity=Critical,Important   # advisory IDs (RHSA) and packages
dnf needs-restarting -r ; echo $?          # 1 = reboot needed
rpm -q --last kernel | head -1 ; uname -r   # newest installed vs running
```
Debian/Ubuntu:
```bash
apt-get -s upgrade | grep -i security | awk '/^Inst/{print $2}'
/usr/lib/update-notifier/apt-check --human-readable      # Ubuntu summary
[ -f /var/run/reboot-required ] && cat /var/run/reboot-required.pkgs
pro security-status                                      # Ubuntu Pro/ESM coverage
```

## Aggregate with Ansible (no extra agents)
```yaml
- hosts: all
  gather_facts: true
  tasks:
    - name: Pending security updates (RHEL)
      ansible.builtin.command: dnf -q updateinfo list --security
      register: sec
      changed_when: false
      when: ansible_os_family == "RedHat"
    - name: Reboot needed (RHEL)
      ansible.builtin.command: dnf needs-restarting -r
      register: rb
      failed_when: rb.rc not in [0, 1]
      changed_when: false
      when: ansible_os_family == "RedHat"
    - ansible.builtin.lineinfile:
        path: /tmp/patch-report.csv
        line: "{{ inventory_hostname }},{{ sec.stdout_lines | default([]) | length }},{{ rb.rc | default('na') }},{{ ansible_kernel }}"
        create: true
      delegate_to: localhost
```
Products that do this centrally: Red Hat Satellite/Insights, Landscape, SUSE Manager, Foreman, Wazuh/OpenSCAP vulnerability scans.

## Report contents
Host, OS/version, count of pending critical/important advisories, oldest advisory date vs SLA (e.g. critical 14 days),
kernel running vs installed, reboot pending, last successful patch run, exceptions with expiry.

## Gotchas
- "Package update available" ≠ vulnerable if mitigated/backported — use advisory data, not version strings.
- Hosts that are unreachable must appear as non-compliant, not be silently missing.

## Verify
- [ ] Report count of hosts equals inventory count; a known-unpatched test host shows as non-compliant.
