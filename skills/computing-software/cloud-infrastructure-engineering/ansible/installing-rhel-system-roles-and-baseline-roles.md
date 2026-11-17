---
id: computing-software.cloud-infrastructure-engineering.ansible.installing-rhel-system-roles-and-baseline-roles
name: installing-rhel-system-roles-and-baseline-roles
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, rhel-system-roles, system-roles-install, redhat-collection-install, crypto-policies, cockpit-role, journald-role]
level: practitioner
status: docs-checked
description: "Install RHEL system roles from the rpm or the redhat.rhel_system_roles collection, then apply crypto_policies, journald and cockpit roles as a host baseline."
sources:
  - https://raw.githubusercontent.com/linux-system-roles/crypto_policies/main/README.md
  - https://raw.githubusercontent.com/linux-system-roles/journald/main/README.md
  - https://raw.githubusercontent.com/linux-system-roles/cockpit/main/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing RHEL system roles and baseline roles

## Install
The roles are published upstream as linux-system-roles; the RHEL builds use the
`redhat.rhel_system_roles` collection namespace and the Fedora/upstream builds use
`fedora.linux_system_roles` (the cockpit README refers to the latter). Use FQCN role names
(for example `redhat.rhel_system_roles.timesync`) consistently in a play.

## crypto_policies
```yaml
- hosts: rhel
  vars:
    crypto_policies_policy: "DEFAULT:NO-SHA1"
    crypto_policies_reboot_ok: true
  roles:
    - redhat.rhel_system_roles.crypto_policies
```
`crypto_policies_policy` takes a base policy or base plus subpolicies as accepted by
`update-crypto-policies` (for example `FUTURE` or `DEFAULT:NO-SHA1:GOST`); they must exist on the
target. The default `null` changes nothing and the role only reports facts:
`crypto_policies_active`, `crypto_policies_available_policies`,
`crypto_policies_available_subpolicies` and `crypto_policies_reboot_required`. A reboot is
recommended after a change; by default the role only sets the `reboot_required` fact, and
`crypto_policies_reboot_ok: true` lets it reboot. `crypto_policies_reload` (default true)
reloads affected daemons; `crypto_policies_force_regenerate` forces regeneration after you
edit policy files.

## journald
```yaml
- hosts: rhel
  vars:
    journald_persistent: true
    journald_max_disk_size: 2048          # MB
    journald_per_user: true
    journald_sync_interval: 1             # minutes, persistent only
  roles:
    - redhat.rhel_system_roles.journald
```
`journald_persistent: true` stores logs in `/var/log/journal/`; default false is volatile.
Per-user journals (`journald_per_user`, `SplitMode`) need persistence. Other variables:
`journald_max_files`, `journald_max_file_size`, `journald_keep_free`, `journald_max_retention`,
`journald_forward_to_syslog`, `journald_compression`, rate-limit settings.

## cockpit
```yaml
- hosts: rhel
  vars:
    cockpit_packages: default             # minimal | default | full | list
    cockpit_manage_firewall: true
    cockpit_manage_selinux: true
    cockpit_port: 9090
    cockpit_config:
      WebService: {LoginTitle: "{{ inventory_hostname }}"}
  roles:
    - redhat.rhel_system_roles.cockpit
```
`cockpit_config` replaces `/etc/cockpit/cockpit.conf` entirely. By default Cockpit creates a
self-signed certificate; set `cockpit_certificates` (passed to the `certificate` role) or
`cockpit_cert` plus `cockpit_private_key` (needs Cockpit 257 or newer) to use a proper one, but
not both.

## Gotchas
- `cockpit_manage_firewall` and `cockpit_manage_selinux` only add ports/policy (RedHat and Suse
  `os_family`), default false, and use the firewall and selinux roles; removal needs those roles directly.
- The default SELinux policy lets Cockpit listen only on 9090; enable `cockpit_manage_selinux` if you change `cockpit_port`.
- `journald_sync_interval` warns when not persistent.

## Verify
- [ ] `crypto_policies_active` matches the policy you set.
- [ ] `/var/log/journal/` exists after enabling persistence.
- [ ] Cockpit is reachable on the configured port.

## Checked

Method: documentation only; no commands were run. Checked 2026-11-09 against the linux-system-roles crypto_policies, journald and cockpit READMEs (each read in full). Removed as not in those pages: the install table (rpm and Automation Hub commands, `/usr/share/ansible` paths, search order claims), `update-crypto-policies --set` and FIPS advice, the journald drop-in path and restart claim, the `ansible-doc -t role` and `rolespec_validate` gotcha, the "typos silently ignored" and collection precedence claims, and the verify commands. The Red Hat RHEL 9 guide was not read (403) and is no longer cited.
