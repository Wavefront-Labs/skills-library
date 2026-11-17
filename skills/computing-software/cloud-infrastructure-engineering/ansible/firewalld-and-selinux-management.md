---
id: computing-software.cloud-infrastructure-engineering.ansible.firewalld-and-selinux-management
name: firewalld-and-selinux-management
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, firewalld, firewall, ansible-posix-firewalld, ufw, iptables, nftables, selinux, selinux-module, sefcontext, seboolean, seport, restorecon, enforcing, permissive, rich-rules, zones, services, ports, community-general-ufw, rhel-system-roles-firewall, rhel-system-roles-selinux]
level: practitioner
status: docs-checked
description: "Manage host firewalls and SELinux with Ansible: firewalld zones/services/ports with permanent+immediate, ufw on Debian, selinux state, seboolean, sefcontext, seport."
sources:
  - https://raw.githubusercontent.com/ansible-collections/ansible.posix/main/plugins/modules/firewalld.py
  - https://raw.githubusercontent.com/ansible-collections/ansible.posix/main/plugins/modules/selinux.py
  - https://raw.githubusercontent.com/ansible-collections/ansible.posix/main/plugins/modules/seboolean.py
  - https://raw.githubusercontent.com/ansible-collections/community.general/main/plugins/modules/sefcontext.py
  - https://raw.githubusercontent.com/ansible-collections/community.general/main/plugins/modules/seport.py
  - https://raw.githubusercontent.com/ansible-collections/community.general/main/plugins/modules/ufw.py
  - https://raw.githubusercontent.com/linux-system-roles/firewall/main/README.md
  - https://raw.githubusercontent.com/linux-system-roles/selinux/main/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# firewalld and SELinux management

**Goal:** ports open only where declared, rules survive reboots, and SELinux stays
enforcing because contexts, booleans and ports are declared instead of disabled.

## 1. firewalld (RHEL/Fedora/SUSE)
```yaml
- ansible.posix.firewalld:
    service: https
    zone: public
    permanent: true
    immediate: true
    state: enabled
- ansible.posix.firewalld: {port: 8443/tcp, permanent: true, immediate: true, state: enabled}
- ansible.posix.firewalld: {masquerade: true, zone: public, permanent: true, immediate: true, state: enabled}
```
- The module needs `python-firewall` or `python3-firewall` on the managed node, usually provided
  by the distribution's `firewalld` packaging. It requires firewalld >= 0.9.0.
- `permanent` (default false) writes the permanent configuration; `immediate` (default false)
  applies to the runtime configuration. If `permanent` is false, `immediate` defaults to true.
  To change both, set both.
- Permanent operations can work while firewalld is not running; `offline: true` ignores
  `immediate` when `permanent: true` and firewalld is not running.
- Zone creation/deletion (`zone` plus `state: present`/`absent` only) must be permanent. Reload
  firewalld afterwards if you need to act on the new zone immediately; the module does not.
- Declarative alternative: the `firewall` system role with a `firewall:` list of items such as
  `- service: http` and `- port: "8080/tcp"`; `previous: replaced` must be its own list item.

Debian/Ubuntu: `community.general.ufw` takes `rule`, `port`, `proto`, `state` (`enabled` reloads
the firewall and enables it on boot) and `default` (alias `policy`: `allow`, `deny`, `reject`).

## 2. SELinux
```yaml
- ansible.posix.selinux: {policy: targeted, state: enforcing}
  register: se
- ansible.builtin.reboot:
  when: se.reboot_required
- ansible.posix.seboolean: {name: httpd_can_network_connect_db, state: true, persistent: true}
- community.general.sefcontext:
    target: '/srv/www(/.*)?'
    setype: httpd_sys_content_t
    state: present
  notify: restorecon www
- community.general.seport: {ports: 8443, proto: tcp, setype: http_port_t, state: present}
handlers:
  - name: restorecon www
    ansible.builtin.command: restorecon -Rv /srv/www
```
- `selinux` may need a reboot; it does not issue one but returns `reboot_required`.
- `sefcontext` is similar to `semanage fcontext`; the docs say to create the file contexts before
  creating files, or run `restorecon` manually for existing files. Either `setype` or
  `substitute` is required when `state: present`.
- `seboolean` has a `persistent` option; set it to keep the value across reboots.
- Declarative: the `selinux` system role with `selinux_policy`, `selinux_state`,
  `selinux_booleans`, `selinux_fcontexts` and `selinux_ports`; the `*_purge` variables remove
  entries not listed.
- The SELinux modules need the SELinux and semanage Python bindings on the target (the module
  docs list libselinux, libsemanage and policycoreutils Python packages).

## Gotchas
- `seboolean` without `persistent: true` is lost at reboot.
- `selinux: state: disabled` is available but fixing the label, boolean or port is the alternative this skill prefers.
- `restorecon` on a large tree is slow; scope the handler to the path you changed.

## Verify
- [ ] `firewall-cmd --list-all` shows the declared services/ports.
- [ ] `getenforce` prints `Enforcing`.
- [ ] A second run reports `changed=0`.

## Checked

Method: documentation only; no commands were run. Checked 2026-11-09 against the firewalld, selinux, seboolean, sefcontext, seport and ufw module sources and the linux-system-roles firewall and selinux READMEs. Removed as not confirmed: rich-rule, source, interface and service-disable examples, the Molecule/D-Bus claim, custom service XML advice, `firewall-cmd --get-*` check commands, the RHEL 9 unsupported-disabled claim, audit2allow/semodule advice, the permissive diagnosis flow with `ausearch`, per-file `setype` on file/copy/template, the `ansible_facts.selinux` fact names, `selinux_restore_dirs`, the iptables persistence advice and the RHCE exam objectives source.
