---
id: computing-software.cybersecurity-defensive.system-hardening.ansible-lockdown-cis-stig-roles
name: ansible-lockdown-cis-stig-roles
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [ansible-lockdown, cis-benchmarks, stig, ansible, hardening-automation]
level: practitioner
status: draft
description: "Apply CIS or STIG hardening to Linux and Windows with Ansible Lockdown roles: variables, tags, check mode, audit, and safe rollout."
sources: ["https://github.com/ansible-lockdown"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ansible Lockdown roles

**Goal:** automate benchmark remediation consistently, with explicit exceptions.

## What it is
The ansible-lockdown GitHub organisation publishes roles per OS and benchmark (RHEL, Ubuntu, Windows, ...; CIS and DISA STIG), usually with a matching audit component. Role variables, rule ids and tags follow the OS-specific prefix; read the role's README and `defaults/main.yml`.

## Use
```yaml
- hosts: hardened
  become: true
  roles:
    - role: RHEL9-CIS          # install via requirements.yml / ansible-galaxy
  vars:
    rhel9cis_level_1: true
    rhel9cis_level_2: false
```
```bash
ansible-playbook -i inventory site.yml --check --diff          # preview
ansible-playbook -i inventory site.yml --tags level1-server     # subset
ansible-playbook -i inventory site.yml --skip-tags rule_5.1.1   # skip a rule (naming varies)
```
Variable names, tags and the toggles for individual rules differ per role and version; confirm in the role.

## Safe rollout
1. Test on a clone of the target image, then a canary group, then fleet.
2. Review changes touching SSH, firewall, PAM, mounts, services, kernel modules: they can lock you out or break apps. Keep console access.
3. Set exceptions as variables in group_vars with a comment (owner, reason, expiry).
4. Pin role versions in `requirements.yml`.
5. Run the role's audit (or CIS-CAT / InSpec) before and after; keep the delta.

## Verify
Second run reports zero changes (idempotent); audit pass rate rises; applications still pass smoke tests.
