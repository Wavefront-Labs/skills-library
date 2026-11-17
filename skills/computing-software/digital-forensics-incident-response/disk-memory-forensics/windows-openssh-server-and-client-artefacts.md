---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.windows-openssh-server-and-client-artefacts
name: windows-openssh-server-and-client-artefacts
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [windows-openssh, lateral-movement, sshd, ssh-artefacts, windows-forensics, dfir]
level: practitioner
status: docs-checked
description: "Investigate OpenSSH on Windows as a lateral movement and persistence path: install and enable evidence, sshd logging, authorized_keys, host keys and client usage."
sources: ["https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse", "https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_keymanagement", "https://github.com/PowerShell/Win32-OpenSSH/wiki/Logging-Facilities", "https://attack.mitre.org/techniques/T1021/004/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows OpenSSH server and client artefacts

Windows OpenSSH is an in-box Feature on Demand (Windows 10 build 1809 / Server 2019 or later; installed by default on Server 2025). MITRE lists SSH as a lateral movement sub-technique (T1021.004): adversaries log in with valid accounts and may use password or public-key authentication. Enabling sshd gives an attacker a persistent remote path.

## Was the server installed or enabled?
- Install is done with `Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0` (client: `OpenSSH.Client~~~~0.0.1.0`). Hunt for that command in PowerShell logging and command-line telemetry.
- Service: `sshd` (display name "OpenSSH SSH Server"). Microsoft's setup sets it to Automatic and starts it with `Start-Service sshd` / `Set-Service -Name sshd -StartupType 'Automatic'`; by default it is started manually. Look for service start-type changes and starts.
- Firewall: installing the server creates and enables an inbound rule named `OpenSSH-Server-In-TCP` for TCP port 22. An attacker may create the same rule by hand with `New-NetFirewallRule`.
- Group: on Server 2025, users and groups allowed or restricted for SSH can be placed in the `OpenSSH Users` group.

## Server-side logs and config
- Since Win32-OpenSSH v7.6.1.0 the server logs to ETW by default, viewable in Event Viewer: the Admin channel holds critical and error events, Operational holds INFO, and Debug holds DEBUG variants (hidden unless "Analytic and Debug Logs" is shown and the channel is enabled). Payloads mimic syslog entries.
- File logging is switched on by `SyslogFacility LOCAL0` (and a `LogLevel`, for example `Debug3`) in `sshd_config`; logs then go to `%programdata%\ssh\logs` (`sshd.log`; `sftp-server.log` for sftp). A `LOCAL0` setting in `sshd_config` is therefore itself a finding.
- Host keys are generated on first use of sshd and stored under `%ProgramData%\ssh`, because no user is associated with the service. Their creation time bounds the first sshd start.
- Keys: a standard user's public keys go in `authorized_keys` in `.ssh` under their profile. For members of the local Administrators group, the file is `administrators_authorized_keys` in `%ProgramData%\ssh`, with an ACL restricted to Administrators and SYSTEM. A new entry there grants access as any administrator account.
- Windows OpenSSH does not support `AuthorizedKeysCommand` / `AuthorizedKeysCommandUser`. Key-based authentication works for local and Active Directory accounts, not Microsoft Entra ID accounts.

## Client-side usage
- `known_hosts` (hosts contacted, added when a user answers "yes" to the host-key prompt), `config` and private keys (default type if unspecified in `ssh-keygen`: Ed25519) live in `.ssh` under the user profile.
- The `ssh-agent` service is disabled by default; if it is enabled and holding keys, that is a sign of deliberate key use.
- Execution evidence for `ssh.exe` (for example Prefetch, Amcache, process-creation logs) comes from the general execution-artefact skills; check the command line for tunnel options.

## Gotchas
- Sessions opened with key-based authentication carry no user credentials, so they cannot authenticate outbound as the user. A pivot from such a session needs another credential.
- Correlate by time between the OpenSSH channel, Security logon events and network telemetry; do not assume a fixed event ID or logon type.

## Verify
For each SSH session claimed, you have an OpenSSH log entry (Operational channel or `sshd.log`) or a Security logon event, the source IP, the account, and whether a key or password was used.

## Checked
Date: 2026-11-08.
Read in full: Microsoft Learn "Get started with OpenSSH for Windows" and "Key-based authentication in OpenSSH for Windows"; Win32-OpenSSH wiki "Logging Facilities"; MITRE ATT&CK T1021.004 (technique description).
Confirmed: version prerequisites and Server 2025 default install, capability names, service names and startup behaviour, `OpenSSH-Server-In-TCP` rule on port 22, `OpenSSH Users` group, host key location and generation, `authorized_keys` and `administrators_authorized_keys` locations and ACL, unsupported `AuthorizedKeysCommand`, Entra ID limitation, Ed25519 default, `known_hosts` behaviour, ssh-agent disabled by default, no outbound credentials for key sessions, ETW default since v7.6.1.0 with Admin/Operational/Debug channels, `SyslogFacility LOCAL0` file logging path, MITRE T1021.004 description.
Removed: "OpenSSH.Client installed by default on 1809+", T1572, the exact Operational log name and event ID 4 text, CBS/DISM log paths, System 7045/7040 and firewall 2004/2097 event IDs, SYSTEM hive service path, `sshd.exe` path, 4624 logon-type mapping, `DefaultShell` registry key, Sysmon event numbers and port-443 remark (none are on the pages).
Method: documentation only; no commands were run.
