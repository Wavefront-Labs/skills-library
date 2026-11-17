---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.smb2-and-smb3-traffic-analysis
name: smb2-and-smb3-traffic-analysis
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [smb-traffic-analysis, smb2, smb3, lateral-movement, named-pipes, dcerpc, psexec, wireshark, dfir]
level: advanced
status: gated
description: "Analyse SMB2/3 traffic for lateral movement: tree connects to admin shares, named pipes and DCE/RPC (svcctl, atsvc, samr), file operations and auth context."
sources: ["https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-smb2/5606ad47-5ee0-437a-817e-70c366052962", "https://wiki.wireshark.org/SMB2", "https://attack.mitre.org/techniques/T1021/002/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SMB2/3 traffic analysis

**Goal:** read what a host did over SMB: which shares it connected to, which files it touched,
and which remote procedures it invoked (service creation, scheduled tasks, account
enumeration).

## Session flow and filters
1. `NEGOTIATE` (dialect: 0x0202, 0x0210, 0x0300, 0x0302, 0x0311): `smb2.cmd == 0`
2. `SESSION_SETUP` with NTLMSSP or Kerberos: `smb2.cmd == 1` (user and domain in
   `ntlmssp.auth.username` / `ntlmssp.auth.domain`)
3. `TREE_CONNECT` to a share: `smb2.cmd == 3`, `smb2.tree`
4. `CREATE` file or pipe: `smb2.cmd == 5`, `smb2.filename`
5. `READ`/`WRITE`/`IOCTL`/`CLOSE`: `smb2.cmd == 8 / 9 / 11 / 6`
Status codes: `smb2.nt_status != 0` (e.g. `STATUS_ACCESS_DENIED` = failed attempts,
`STATUS_LOGON_FAILURE` in SESSION_SETUP = password spraying).

## Lateral movement patterns
| Pattern | What you see |
|---|---|
| PsExec-style | TREE_CONNECT `\\host\ADMIN$`, CREATE/WRITE `PSEXESVC.exe` (or random name), then `\\host\IPC$` pipe `svcctl` with DCE/RPC `CreateServiceW`/`StartServiceW` (`svcctl.opnum == 12` / `19`), then pipes `PSEXESVC-<host>-<pid>-stdin/stdout/stderr` (gated: unconfirmed, source is paywalled or blocked) |
| Impacket smbexec | `svcctl` service whose command line starts with `%COMSPEC% /Q /c` and writes to an output file named `__output_<8 random letters>` on a share, which is then read over SMB (impacket `smbexec.py` source) |
| Impacket wmiexec | DCOM over TCP 135 + dynamic ports, output file named `__<epoch time>` on the share (ADMIN$ by default), read via SMB (impacket `wmiexec.py` source) |
| Remote scheduled task | pipe `atsvc` (`ITaskSchedulerService`; Wireshark decodes it as `taskschedulerservice`, `SchRpcRegisterTask` is opnum 1) |
| Remote registry | pipe `winreg` |
| Recon | pipes `samr` (users/groups), `lsarpc` (SIDs), `srvsvc` (`NetShareEnumAll`, `NetSessEnum`), `drsuapi` over TCP for DCSync (`DsGetNCChanges`) |
Filter pipes: `smb2.filename in {"svcctl", "atsvc", "samr", "lsarpc", "srvsvc", "winreg"}` and
`dcerpc.cn_bind_to_uuid`.

## Encryption
SMB 3.x encryption (transform header) hides commands after session setup; you still see the
negotiate, session setup (user), and volumes. Decrypt with the session key
(Preferences > Protocols > SMB2 > Secret session keys) when obtainable from memory or a test
setup.

## Report
Source host, destination, account, share, files written/read, RPC operations with times; map
to host artefacts (4697 service install in the Security log, 5140/5145 share access, 4624 type 3 logons).

## Self-check
For each SMB session you can state who authenticated, to which share, which files moved and
which RPC actions executed, with frame numbers.

## Checked
The comma set filter and every field in this skill (`smb2.cmd`, `smb2.tree`, `smb2.filename`, `smb2.nt_status`,
`svcctl.opnum`, `dcerpc.cn_bind_to_uuid`; the old `dcerpc.cn_bind_to_str` does not exist) were compiled in tshark
4.4.1. Command numbers 0 to 13, the dialect values 0x0202, 0x0210, 0x0300, 0x0302, 0x0311, `STATUS_ACCESS_DENIED`,
`STATUS_LOGON_FAILURE`, svcctl opnums 12 (CreateServiceW) and 19 (StartServiceW), srvsvc `NetShareEnumAll` and
`NetSessEnum` and drsuapi `DsGetNCChanges` come from `tshark -G values`. The smbexec and wmiexec output-file names come
from the impacket sources; event IDs 4624, 5140, 5145 and 4697 from Microsoft Learn. No SMB capture was built, so the
lateral-movement rows are not shown to produce these frames here. The PsExec pipe names could not be confirmed from a
primary source.
