---
id: computing-software.cloud-infrastructure-engineering.ansible.become-runas-on-windows
name: become-runas-on-windows
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, windows-automation, win-become, runas, become-plugins]
level: advanced
status: docs-checked
description: "Use become with runas on Windows to escape network-logon limits, run as SYSTEM or another user, choose logon types and flags, and fix double-hop credential issues."
sources: ["https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_privilege_escalation.html#become-and-windows", "https://docs.ansible.com/ansible/latest/collections/ansible/builtin/runas_become.html", "https://docs.ansible.com/ansible/latest/os_guide/windows_winrm_kerberos.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# become with runas on Windows

A WinRM session is a restricted logon: constrained network delegation (the double-hop problem) and no access to some system calls such as the Windows Update Agent (WUA) API; many installers also misbehave over WinRM. `become` with runas creates an interactive-style logon.

## Basics
```yaml
- name: Install updates as SYSTEM
  ansible.windows.win_updates:
    category_names: [SecurityUpdates]
  become: true
  become_method: runas
  become_user: SYSTEM

- name: Access a file share as a service account
  ansible.windows.win_copy:
    src: \\fileserver\pkgs\agent.msi
    dest: <DRIVE>:\Temp\agent.msi
    remote_src: true
  become: true
  become_method: runas
  become_user: CORP\svc-deploy
  vars:
    ansible_become_password: "{{ vault_svc_deploy_password }}"
```

## Users
- `SYSTEM`, `NetworkService`, `LocalService`: no password needed.
- `become_user` has no default on Windows and is required. Local and domain users normally need `ansible_become_password`. Becoming an account without a password (since Ansible 2.8) needs the connection user to hold `SeDebugPrivilege` and be in `BUILTIN\Administrators`, and the become user to hold `SeBatchLogonRight` or `SeNetworkLogonRight`; leave the password undefined. Such a logon usually has no network access.
- On Windows you cannot connect as an unprivileged account and use become to elevate: the connection account must already be an Administrator of the target.
- Set `logon_type`/`logon_flags` only when becoming a normal user, not a service account.

## Flags
```yaml
become_flags: logon_type=new_credentials logon_flags=netcredentials_only
```
- `logon_type`: `interactive` (default; bypasses WinRM restrictions), `batch` (like a scheduled task with a password; for users not allowed to log on interactively), `new_credentials` (runs as the calling user, outbound connections use the become user and password, like `runas.exe /netonly`; pair with `logon_flags=netcredentials_only`; for shares), `network` (no cached credentials, same restrictions as a normal WinRM process), `network_cleartext` (like `network` but caches credentials so network resources are reachable). The plugin source also accepts `service` and `unlock`.
- `logon_flags`: `none`, `with_profile` (the default; loads the user profile) and `netcredentials_only` (use the caller's token locally, the become credentials for remote resources). Separate several with commas, for example `logon_flags=with_profile,netcredentials_only`; `logon_flags=` loads no profile. Any other key in `become_flags` is rejected.

## Gotchas
- Elevation: runas tries to get the full token; the user needs `SeDebugPrivilege` (Administrators have it by default), otherwise the task silently runs with a limited token. Check the `label` in `win_whoami` output: `Medium` limited, `High` elevated, `System` the SYSTEM account.
- The runas plugin ignores `become_exe` (it uses an API, not an executable) and needs the Secondary Logon service (seclogon) running on the target. The plugin notes say it is implemented in the PowerShell module handler and can only be used with winrm connections; the Windows SSH guide nevertheless recommends become for the SSH double-hop problem, so test your connection plugin.
- Kerberos delegation is an alternative for double-hop: set `ansible_winrm_kerberos_delegation: true` (winrm) or `ansible_psrp_negotiate_delegate: true` (psrp); it needs a forwardable TGT, and the user must not be marked sensitive or be in Protected Users.

## Verify
```yaml
- ansible.windows.win_whoami:
  become: true
  become_method: runas
  become_user: SYSTEM
  register: who
- ansible.builtin.debug: {var: who.account.account_name}
```

## Checked
Checked 2026-10-25 against the ansible-documentation devel branch (commit of 2026-10-21): playbook_guide/playbooks_privilege_escalation.rst (Windows become sections), os_guide/windows_ssh.rst, os_guide/windows_winrm_kerberos.rst, and the ansible-core `runas` become plugin source. Confirmed: required `become_user`, service accounts and passwordless become requirements, the full `logon_type` and `logon_flags` value lists and defaults, `SeDebugPrivilege` elevation, `win_whoami` labels, seclogon and `become_exe` notes. Removed unconfirmed claims about DPAPI, `win_updates` handling become internally and play-level become sending sudo to Windows.
Method: documentation only; no commands were run.
