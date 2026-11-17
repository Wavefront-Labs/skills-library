---
id: computing-software.cloud-infrastructure-engineering.ansible.firewalld-permanent-runtime-masquerade-and-forwarding
name: firewalld-permanent-runtime-masquerade-and-forwarding
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, firewall-selinux, firewalld-permanent, masquerade, port-forward, firewalld]
level: practitioner
status: docs-checked
description: "Apply firewalld changes both permanently and immediately, avoid reload surprises, and configure masquerading and port forwarding with ansible.posix.firewalld."
sources: ["https://github.com/ansible-collections/ansible.posix/blob/main/plugins/modules/firewalld.py", "https://firewalld.org/documentation/configuration/runtime-versus-permanent.html", "https://github.com/firewalld/firewalld/blob/main/doc/xml/firewalld.policies.xml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# firewalld: permanent vs runtime, masquerade, forwarding

## Always set both
```yaml
- name: Allow HTTPS
  ansible.posix.firewalld:
    service: https
    zone: public
    permanent: true       # survives reload/reboot
    immediate: true       # also applies to the running config now
    state: enabled
```
| permanent | immediate | Result |
|---|---|---|
| true | false (the default) | saved, not active until reload |
| false | true (implied) | active now, lost on reload/reboot |
| true | true | both: what you almost always want |

A reload restores the permanent configuration, so runtime-only rules added without `permanent: true` are lost when a later handler reloads.

## Masquerade
```yaml
- ansible.posix.firewalld:
    masquerade: true          # a bool since ansible.posix 2.0.0
    zone: external
    permanent: true
    immediate: true
    state: enabled
```

## Port forwarding
```yaml
- ansible.posix.firewalld:
    port_forward:
      - port: 443
        proto: tcp
        toport: 8443
        toaddr: 10.0.0.20     # omit for local redirect
    zone: external
    permanent: true
    immediate: true
    state: enabled
```
Forwarding to another host needs masquerade (or routing back) and `net.ipv4.ip_forward=1` (`ansible.posix.sysctl`). Rich rules (the module's `rich_rule` option) are the alternative for source-restricted forwards.

## Policies and zone forwarding
The module has no `policy` option. `forward: true` (firewalld 0.9.0 or later) turns on intra-zone forwarding for a zone. For policies between zones use `firewall-cmd --permanent --new-policy <name>` in command tasks or the firewall system role.

## Gotchas
- `offline: true` ignores `immediate` when `permanent` is true and firewalld is not running, so permanent config can be edited in images.
- Interfaces not assigned to a zone use the default zone.

## Verify
```bash
ansible gw -b -m ansible.builtin.command -a 'firewall-cmd --zone=external --list-all'
ansible gw -b -m ansible.builtin.command -a 'firewall-cmd --permanent --zone=external --list-all'
```

## Checked

Checked 2026-10-26 against the ansible.posix `firewalld` module source (main) and the firewalld manual sources. Confirmed: `permanent` and `immediate` semantics and defaults; `masquerade` and `forward` as bool options (`forward` needs firewalld 0.9.0 or later); `port_forward` entries with `port`, `proto`, `toport`, `toaddr`; `rich_rule`; `offline`; no `policy` option; `firewall-cmd --permanent --new-policy` exists. Removed the string-`yes` remark and the unconfirmed statement that firewalld must be running.

Method: documentation only; no commands were run.
