---
id: computing-software.cloud-infrastructure-engineering.ansible.windows-local-users-groups-and-domain-membership
name: windows-local-users-groups-and-domain-membership
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, windows-automation, win-user, win-domain-membership, win-group-membership, microsoft-ad, domain-join]
level: practitioner
status: docs-checked
description: "Manage Windows local users and group membership with ansible.windows modules and join or leave an AD domain with microsoft.ad.membership, including the required reboot."
sources: ["https://github.com/ansible-collections/ansible.windows/blob/main/plugins/modules/win_user.py", "https://github.com/ansible-collections/ansible.windows/blob/main/plugins/modules/win_group_membership.py", "https://github.com/ansible-collections/microsoft.ad/blob/main/plugins/modules/membership.yml", "https://github.com/ansible-collections/ansible.windows/blob/main/CHANGELOG.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows local users, groups and domain membership

## Local users
```yaml
- name: Ensure local service account
  ansible.windows.win_user:
    name: svc_backup
    password: "{{ vault_svc_backup_pw }}"
    update_password: on_create          # do not reset it every run
    password_never_expires: true
    user_cannot_change_password: true
    groups: [Backup Operators]
    groups_action: add                  # add | remove | replace (the default; replace drops other groups!)
    state: present
  no_log: true
```
Disable rather than delete when auditing matters: `account_disabled: true`.

## Group membership (local groups, incl. domain members)
```yaml
- ansible.windows.win_group_membership:
    name: Administrators
    members: [CORP\srv-admins, svc_backup]
    state: present            # pure = exactly these members, removes others
```
`state: pure` is how you enforce "only these admins" — dangerous: test that it keeps the
account Ansible connects with.

## Join a domain
```yaml
- name: Join corp.example.com
  microsoft.ad.membership:
    dns_domain_name: corp.example.com
    hostname: "{{ inventory_hostname_short | upper }}"
    domain_admin_user: "join-svc@corp.example.com"
    domain_admin_password: "{{ vault_join_pw }}"
    domain_ou_path: "OU=Servers,DC=corp,DC=example,DC=com"
    state: domain
    reboot: true             # handles the reboot and reconnect itself
  no_log: true
```
Leave: `state: workgroup`, `workgroup_name: WORKGROUP`. The older
`ansible.windows.win_domain_membership` was removed in favour of `microsoft.ad.membership`
(install the `microsoft.ad` collection).

Prerequisite: DNS on the host must resolve the domain (`ansible.windows.win_dns_client`
pointing at DCs first).

## After joining: connection credentials
If you switch to domain accounts for WinRM, set `ansible_winrm_transport` (for example `kerberos`) and a user principal name such as `ansible_user: user@CORP.EXAMPLE.COM`.

## Gotchas
- `win_user` manages local accounts; use the `microsoft.ad` collection against a domain controller for domain accounts.
- `update_password: always` (default) sets the password each run and reports changed.
- `hostname` renames the computer as part of the join; it cannot be combined with `offline_join_blob`.
- If you do not use the module's reboot handling, reboot afterwards (`ansible.windows.win_reboot` when the result's `reboot_required` is true).

## Verify
- [ ] `ansible win -m ansible.windows.win_shell -a '(Get-CimInstance Win32_ComputerSystem).Domain'` shows the domain.
- [ ] `net localgroup Administrators` lists exactly the expected members.

## Checked

Checked 2026-10-26 against the ansible.windows, microsoft.ad and community.windows sources (main). Confirmed: `win_user` options `groups_action` (add, replace, remove; default replace), `update_password` (always default, on_create), `password_never_expires`, `user_cannot_change_password`, `account_disabled`; `win_group_membership` `state` present, absent, pure; `microsoft.ad.membership` options `dns_domain_name`, `hostname`, `domain_admin_user`, `domain_admin_password`, `domain_ou_path`, `state` domain or workgroup, `workgroup_name`, `offline_join_blob`, the `reboot` handling and `reboot_required` result; `win_domain_membership` removed from ansible.windows in favour of `microsoft.ad.membership`. Removed the unconfirmed 5-minute clock rule and the NTLM remark.

Method: documentation only; no commands were run.
