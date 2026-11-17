---
id: computing-software.cloud-infrastructure-engineering.ansible.windows-firewall-rules
name: windows-firewall-rules
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, windows-automation, win-firewall, win-firewall-rule, windows-defender-firewall, winrm]
level: practitioner
status: docs-checked
description: "Manage Windows Defender Firewall profiles and inbound/outbound rules from Ansible with ansible.windows win_firewall and win_firewall_rule without locking out WinRM."
sources: ["https://github.com/ansible-collections/ansible.windows/blob/main/plugins/modules/win_firewall_rule.py", "https://github.com/ansible-collections/ansible.windows/blob/main/plugins/modules/win_firewall.py", "https://github.com/ansible-collections/community.windows/blob/main/CHANGELOG.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows firewall rules

## Keep WinRM open first
Before tightening anything, make sure the rule Ansible depends on exists:
```yaml
- ansible.windows.win_firewall_rule:
    name: WinRM HTTPS (Ansible)
    localport: 5986
    protocol: tcp
    direction: in
    action: allow
    remoteip: 10.20.0.0/24          # the controller / execution node subnet
    profiles: [domain, private, public]
    state: present
    enabled: true
```

## Application rules
```yaml
- name: Allow HTTPS to IIS
  ansible.windows.win_firewall_rule:
    name: Shop HTTPS
    localport: 443
    protocol: tcp
    direction: in
    action: allow
    profiles: [domain]
    description: Managed by Ansible
    state: present
    enabled: true

- name: Allow app binary outbound to the DB
  ansible.windows.win_firewall_rule:
    name: Shop to SQL
    program: <DRIVE>:\Apps\Shop\Shop.exe
    remoteport: 1433
    remoteip: 10.30.0.10
    protocol: tcp
    direction: out
    action: allow
```
Rules are matched by `name`, so renaming creates a new rule and leaves the old one. Remove old
ones explicitly with `state: absent`.

## Profiles
```yaml
- ansible.windows.win_firewall:
    state: enabled
    profiles: [Domain, Private, Public]
    inbound_action: block
    outbound_action: allow
```

## Group rules
`win_firewall_rule` takes a `group` option; with `name` omitted, it sets the given options on every rule in that group. PowerShell also works:
```yaml
- ansible.windows.win_powershell:
    script: |
      $r = Get-NetFirewallRule -DisplayGroup 'Remote Desktop'
      if (($r | Where-Object Enabled -eq 'False').Count) { $r | Enable-NetFirewallRule; $Ansible.Changed = $true } else { $Ansible.Changed = $false }
```

## Gotchas
- `localport` and `remoteport` need `protocol` set; the defaults on creation are `any` for addresses, ports and service, and all three profiles.
- Several rules can share one `name`: the module then applies the options to each matching rule, so keep names unique.
- `win_firewall_rule` and `win_firewall` live in `ansible.windows`; the `community.windows` names are deprecated redirects, so use the `ansible.windows` names.

## Verify
- [ ] `Get-NetFirewallRule -DisplayName 'Shop HTTPS' | Get-NetFirewallPortFilter` shows port 443/TCP.
- [ ] `Test-NetConnection host -Port 443` from a client succeeds; WinRM still reachable from the controller.

## Checked

Checked 2026-10-26 against the ansible.windows module sources and the community.windows changelog (main). Confirmed: `win_firewall_rule` and `win_firewall` now live in `ansible.windows` (the community.windows modules are deprecated redirects to be removed in 4.0.0); rule options `name`, `group`, `direction` (in, out), `action` (allow, block), `localport`, `remoteport`, `remoteip`, `program`, `protocol`, `profiles`, `enabled`, `state` (present, absent), `description`; `localport` requires `protocol`; rules sharing a name are all updated; `win_firewall` `state` (enabled, disabled), `profiles` (Domain, Private, Public), `inbound_action` and `outbound_action` (allow, block, not_configured). Removed the `ActiveStore` and version-difference remarks.

Method: documentation only; no commands were run.
