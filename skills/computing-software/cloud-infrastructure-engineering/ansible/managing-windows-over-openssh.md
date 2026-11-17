---
id: computing-software.cloud-infrastructure-engineering.ansible.managing-windows-over-openssh
name: managing-windows-over-openssh
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, windows-automation, win-openssh, windows, ssh]
level: practitioner
status: docs-checked
description: "Manage Windows hosts over OpenSSH instead of WinRM: install and configure the OpenSSH server, set the default shell, inventory vars and key-based auth."
sources: ["https://github.com/ansible/ansible-documentation/blob/devel/docs/docsite/rst/os_guide/windows_ssh.rst", "https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Windows over OpenSSH

Ansible has been able to use the ssh connection plugin with Windows since 2.8; official support was added in ansible-core 2.18. Advantages: one transport for Linux and Windows, key auth, no WinRM listener or certificates.

## Install OpenSSH Server (Windows capability since Windows Server 2019)
```powershell
Get-WindowsCapability -Name OpenSSH.Server* -Online | Add-WindowsCapability -Online
Set-Service -Name sshd -StartupType Automatic -Status Running
New-ItemProperty -Path "HKLM:\SOFTWARE\OpenSSH" -Name DefaultShell `
  -Value "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe" -PropertyType String -Force
```
The shell change applies to the next SSH connection without restarting `sshd`; run `meta: reset_connection` after changing it from a playbook. The default shell is `cmd.exe`; PowerShell is recommended as better tested.

## Inventory
```yaml
# group_vars/windows_ssh.yml
ansible_connection: ssh
ansible_shell_type: powershell        # match DefaultShell (cmd if you left the default)
ansible_user: svc-ansible
ansible_ssh_private_key_file: ~/.ssh/win_ed25519
```

## Key auth
- Standard users: `authorized_keys` in the `.ssh` folder of the user profile.
- Administrators: keys go in `%ProgramData%\ssh\administrators_authorized_keys` (see the Windows SSH page for the `Match Group administrators` setting that controls this).

## Become
Key authentication does not delegate credentials (the double-hop problem), so a task that reaches a network resource fails; use `become` with a password to work around it. GSSAPI and password authentication can delegate.

## Gotchas
- `ansible_shell_type` must match the configured DefaultShell.
- Use the Windows modules (`ansible.windows.*`), not the Linux builtin ones.

## Verify
```bash
ansible windows_ssh -m ansible.windows.win_ping
```

## Checked

Checked 2026-10-26 against the Ansible Windows SSH page (documentation repository, devel). Confirmed: official support since ansible-core 2.18 (ssh plugin usable since 2.8); OpenSSH as a Windows capability since Windows Server 2019 and the `Get-WindowsCapability ... | Add-WindowsCapability` install command; the `HKLM:\SOFTWARE\OpenSSH` `DefaultShell` value, default `cmd.exe`, no `sshd` restart needed; `ansible_connection: ssh` with `ansible_shell_type` of `powershell` or `cmd`; administrators' keys in `%ProgramData%\ssh\administrators_authorized_keys`; key authentication cannot delegate credentials. Removed the `icacls` command, event-log remark, pipelining and sftp claims, which the page does not state.

Method: documentation only; no commands were run.
