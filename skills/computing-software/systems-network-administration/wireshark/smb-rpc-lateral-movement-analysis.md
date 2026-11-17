---
id: computing-software.systems-network-administration.wireshark.smb-rpc-lateral-movement-analysis
name: smb-rpc-lateral-movement-analysis
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, smb-lateral-movement, smb2, dcerpc, psexec, network-forensics]
level: practitioner
status: draft
description: "Detect lateral movement over SMB and RPC in captures: admin share access, PsExec-style service creation, remote WMI/DCOM, scheduled tasks and DCSync."
sources:
  - https://attack.mitre.org/tactics/TA0008/
  - https://www.wireshark.org/docs/dfref/s/smb2.html
  - https://www.wireshark.org/docs/dfref/d/dcerpc.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SMB/RPC lateral movement

## Admin shares and file drops
```
smb2.tree contains "ADMIN$" || smb2.tree contains "C$" || smb2.tree contains "IPC$"
smb2.cmd == 5 && smb2.filename matches "\\.(exe|dll|ps1|bat)$"     # Create of executables
```
SMB 3 encryption hides filenames; then rely on Tree Connect paths (still visible pre-encryption in
some cases) and RPC timing, or decrypt with session keys.

## PsExec-style service creation (svcctl)
Over IPC$ named pipe `\svcctl`: `dcerpc.cn_bind_to_uuid == 367abb81-9844-35f1-ad32-98f038001003`
then `svcctl.opnum == 12` (CreateServiceW) and 19 (StartServiceW). PsExec also uses pipe
`PSEXESVC`.

## Other remote execution
| Technique | Indicator |
|-----------|-----------|
| Scheduled task (atsvc/ITaskSchedulerService) | pipe `\atsvc`, `dcerpc` bind to 86d35949-83c9-4044-b424-db363231fd0c |
| WMI/DCOM | TCP 135 then dynamic high port, IWbemServices calls (`dcom`) |
| WinRM | TCP 5985/5986 HTTP to `/wsman` |
| Remote registry | pipe `\winreg` |
| DCSync | `drsuapi` DRSGetNCChanges from a non-DC source |
```
dcerpc.cn_bind_to_uuid == e3514235-4b06-11d1-ab04-00c04fc2dcd2 && drsuapi.opnum == 3
```

## Workflow
1. Statistics > Conversations, TCP 445/135 from workstations to workstations (unusual).
2. Follow each to identify tree, pipe and operations.
3. Correlate with Windows event logs (4624 type 3, 7045 service install, 4698 task creation).

## Verify
- [ ] Each candidate has source host, account (from NTLMSSP/Kerberos), target and operation documented.
