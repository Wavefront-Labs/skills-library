---
id: computing-software.cloud-infrastructure-engineering.ansible.rhel-system-roles
name: rhel-system-roles
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, rhel-system-roles, system-roles, linux-system-roles, redhat-rhel-system-roles, fedora-linux-system-roles, timesync, chrony, selinux-role, network-role, storage-role, firewall-role, ssh-role, sshd-role, logging-role, metrics-role, kernel-settings, podman-role, ha-cluster, postfix, certificate-role, rhel]
level: practitioner
status: draft
description: "Use RHEL/Linux System Roles (timesync, network, storage, selinux, firewall, sshd, logging, kernel_settings, podman) as the supported declarative layer for RHEL: install, FQCN, variables, limits."
sources: ["Red Hat documentation - Automating system administration by using RHEL system roles (https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/automating_system_administration_by_using_rhel_system_roles/)", "linux-system-roles project documentation (https://linux-system-roles.github.io/)", "RHCE EX294 exam objectives - Use roles and Ansible Content Collections (RHEL system roles)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RHEL System Roles

**Goal:** configure the standard RHEL subsystems (time, network, storage, SELinux,
firewall, sshd, logging, kernel tuning) with a Red Hat-supported, upgrade-safe data
interface instead of hand-written tasks.

## 1. Install and address them
```bash
# RHEL control node (supported): the rpm ships both the legacy role names and the collection
sudo dnf install rhel-system-roles        # /usr/share/ansible/collections/ansible_collections/redhat/rhel_system_roles
# Anywhere else: Automation Hub (redhat.rhel_system_roles) or Galaxy upstream
ansible-galaxy collection install fedora.linux_system_roles
```
Reference by FQCN: `redhat.rhel_system_roles.timesync` (RHEL) or
`fedora.linux_system_roles.timesync` (upstream, identical code, newer). Legacy names
(`rhel-system-roles.timesync`) still resolve via `roles_path` on RHEL. Docs and example
playbooks: `/usr/share/doc/rhel-system-roles/<role>/` and each role's `README.md`.

## 2. The roles you will use most
| Role | Key variables | Replaces |
|---|---|---|
| `timesync` | `timesync_ntp_servers: [{hostname: ntp.example, iburst: true}]` | chrony config + service |
| `network` | `network_connections: [{name: eth0, type: ethernet, ip: {address: [10.0.0.5/24], gateway4: 10.0.0.1, dns: [10.0.0.2]}, state: up}]` | nmcli/ifcfg |
| `storage` | `storage_pools` / `storage_volumes` (see storage skill) | parted/lvg/lvol/mount |
| `selinux` | `selinux_state: enforcing`, `selinux_booleans`, `selinux_fcontexts`, `selinux_ports`, `selinux_restore_dirs` | selinux/seboolean/sefcontext |
| `firewall` | `firewall: [{service: https, state: enabled}, {port: 8443/tcp, state: enabled}]`, `firewall: [{previous: replaced}]` | firewalld tasks |
| `ssh` / `sshd` | `sshd_config: {PasswordAuthentication: false, PermitRootLogin: false}`, drop-in on RHEL 9 (`sshd_config_file`) | lineinfile on sshd_config |
| `logging` | `logging_inputs`/`logging_outputs`/`logging_flows` (rsyslog to remote/Elastic) | rsyslog templates |
| `kernel_settings` | `kernel_settings_sysctl: [{name: vm.swappiness, value: 10}]`, transparent hugepages, sysfs | sysctl module + tuned |
| `metrics` | `metrics_graph_service: true` (PCP + Grafana) | pcp setup |
| `certificate` | `certificate_requests: [{name: web, dns: host.example, ca: ipa}]` | certmonger |
| `podman` | `podman_kube_specs`, `podman_quadlet_specs` | quadlet files + systemd |
| `cockpit`, `postfix`, `nbde_client/server`, `ha_cluster`, `vpn`, `crypto_policies`, `ad_integration`, `journald`, `bootloader` | | |

Example play:
```yaml
- hosts: all
  become: true
  vars:
    timesync_ntp_servers: [{hostname: ntp1.example, iburst: true}, {hostname: ntp2.example, iburst: true}]
    selinux_state: enforcing
    selinux_booleans: [{name: httpd_can_network_connect, state: true, persistent: true}]
    firewall: [{service: https, state: enabled}, {zone: public, service: cockpit, state: disabled}]
  roles:
    - redhat.rhel_system_roles.timesync
    - redhat.rhel_system_roles.selinux
    - redhat.rhel_system_roles.firewall
```
Every role honours `--check` where the subsystem allows it and reports `changed` truthfully.

## 3. Conventions
- Variables are prefixed with the role name; most roles have a `<role>_provider` (e.g. `timesync_ntp_provider: chrony`, `network_provider: nm`) auto-detected from the OS.
- Roles manage their own packages and services (`firewalld`, `chrony`, `NetworkManager`).
- Many roles support a "replace everything" mode (`firewall: previous: replaced`, `selinux_booleans_purge`, `network_connections` with `state: absent` by name).
- Reboot-requiring changes (SELinux disabled→enforcing, `kernel_settings_reboot_ok`) are exposed as a variable/result instead of silently rebooting.
- Run with `ansible-navigator` and a RHEL EE on Automation Platform: the supported EE already contains `redhat.rhel_system_roles`.

## 4. When not to
- Non-RHEL-family targets (Debian/Ubuntu/SUSE): the roles support Fedora/CentOS/RHEL (some add Ubuntu); use the module-level skills instead.
- A subsystem the role models only partly (complex nftables, bonded VLAN trunks with exotic options): mixing role-managed and hand-managed config in one file causes fights. Choose one owner per subsystem.
- Containers/Molecule: `network`, `storage`, `firewall` need real hosts; test these with a VM driver.

## Gotchas
- Role variable names changed across versions (`sshd` moved from `sshd_config` list to dict forms, `network` dropped `initscripts`); pin the collection version in `requirements.yml` and read the role's CHANGELOG on bump.
- The RHEL rpm version lags the upstream collection; mixing both on one control node leads to two different behaviours under the same short role name — use FQCN.
- `storage` with `storage_safe_mode: false` *will* reformat; keep the default `true`.
- `network` applying a bad gateway drops your SSH session mid-play; set `network_connections` with `state: up` and test with `persistent_state: present` (write only) first, or `wait_for_connection`.

## Verify
- [ ] `ansible-galaxy collection list | grep system_roles` shows one pinned version.
- [ ] `chronyc sources`, `getenforce`, `firewall-cmd --list-all`, `nmcli con show` on a host match the declared data.
- [ ] Second run of the play reports `changed=0` for all role tasks.
