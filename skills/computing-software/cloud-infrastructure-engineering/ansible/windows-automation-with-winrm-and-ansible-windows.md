---
id: computing-software.cloud-infrastructure-engineering.ansible.windows-automation-with-winrm-and-ansible-windows
name: windows-automation-with-winrm-and-ansible-windows
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, windows, winrm, psrp, pywinrm, pypsrp, ansible-windows, community-windows, powershell-modules, win-feature, win-package, win-chocolatey, chocolatey, win-service, win-updates, win-shell, win-powershell, win-reboot, kerberos, ntlm, credssp, openssh-windows, become-runas, dsc]
level: practitioner
status: docs-checked
description: "Manage Windows hosts with Ansible over WinRM or PSRP: authentication options, HTTPS listener, certificate validation, and the WinRM limitations and their workarounds."
sources: ["https://docs.ansible.com/ansible/latest/os_guide/windows_winrm.html", "https://docs.ansible.com/ansible/latest/os_guide/windows_faq.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows automation with WinRM/PSRP and ansible.windows

**Goal:** Windows servers managed by the same playbooks and inventory as Linux, with
authentication that works on a domain.

## 1. Connection plugins and requirements
Ansible reaches Windows over WinRM through the `psrp` or `winrm` connection plugin. Their
Python requirements (`pypsrp`, `pywinrm`) are not included in the Ansible package and must be
installed on the control node separately (for `credssp`, install the `[credssp]` extra of
the library). Use `winrm` or `psrp` on macOS only with the workaround in the Ansible docs
(`OBJC_DISABLE_INITIALIZE_FORK_SAFETY=yes`, `no_proxy=*`, no Kerberos).

```yaml
windows:
  hosts: {win01.corp.example: {}}
  vars:
    ansible_connection: psrp            # or winrm
    ansible_port: 5986
    ansible_psrp_auth: kerberos         # ansible_winrm_transport for winrm
    ansible_user: svc-ansible@CORP.EXAMPLE
```
- `psrp` and `winrm` have separate variable prefixes (`ansible_psrp_*` vs `ansible_winrm_*`).
- Default WinRM ports are 5985 (HTTP) and 5986 (HTTPS). Use an HTTPS listener (it needs a
  `CertificateThumbprint`; self-signed or CA-issued).
- `ansible_psrp_cert_validation: ignore` disables certificate checks (labs only);
  `ansible_psrp_ca_cert` sets a CA bundle, otherwise the `certifi` chain (or the system store,
  depending on the distribution) is used.

## 2. Authentication
- `psrp` values: `basic`, `certificate`, `negotiate`, `kerberos`, `ntlm`, `credssp`.
  `winrm` values (`ansible_winrm_transport`): `basic`, `certificate`, `kerberos`, `ntlm`,
  `credssp`.
- `negotiate` (psrp only) tries Kerberos first and falls back to NTLM; the `winrm` plugin
  must name `kerberos` or `ntlm`.
- Do not use `basic` or `ntlm` over an HTTP listener: no encryption or very weak encryption.
- `ansible_psrp_message_encryption: always` forces message encryption.

## 3. Limitations of WinRM and mitigations
Under WinRM, credentials are not delegated for most authentication types (network resources
fail), many Windows Update API calls are blocked, commands run in a non-interactive session,
and DPAPI-using installers cannot run. Mitigations in the Ansible docs:
- use `credssp`, or `kerberos` with credential delegation enabled;
- use `become` to bypass all WinRM restrictions and run as locally (this also removes the
  non-interactive and API restrictions);
- use a scheduled task (`win_scheduled_task`), which bypasses restrictions but can run only
  a command, not modules.

## 4. Troubleshooting
WinRM errors shown by Ansible can be host setup problems. Test from another Windows host
(`winrs -r:https://server:5986/wsman ... -ssl ipconfig`, or `Invoke-Command -UseSSL
-ComputerName server { ipconfig } -Credential <user>`), and confirm the target hostname resolves
from the control node (`dig +search server`).

## Verify
- [ ] `ansible windows -m ansible.windows.win_ping` returns `pong` with the chosen authentication.
- [ ] A task that must reach a network share works with the chosen delegation mitigation.

## Checked
2026-11-09. Confirmed in the Ansible Windows WinRM guide: plugins and separate installs,
auth value lists for psrp and winrm, negotiate behaviour, ports 5985/5986, cert validation
variables, message encryption, limitations and mitigations, troubleshooting commands. Removed
as unconfirmed (collection and Windows-specific pages not read): the module table and module
parameters, PowerShell and .NET minimums, OpenSSH transport details, Server version claims,
become runas flags, Kerberos SPN/FQDN note, CRLF template note, win_updates/async rules,
Chocolatey, product_id behaviour, performance figures, and Linux-keyword gotchas.
Method: documentation only; no commands were run.
