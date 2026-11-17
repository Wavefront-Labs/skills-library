---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.dcerpc-traffic-analysis-drsuapi-svcctl-atsvc
name: dcerpc-traffic-analysis-drsuapi-svcctl-atsvc
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [dcerpc-drsuapi, dcerpc, msrpc, dcsync, lateral-movement, wireshark, dfir]
level: advanced
status: draft
description: "Analyse DCE/RPC traffic in captures: endpoint mapper, DRSUAPI DsGetNCChanges (DCSync), SVCCTL service creation, ATSVC/ITaskSchedulerService task creation and decrypting with keys."
sources: ["https://wiki.wireshark.org/DCE/RPC", "https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-drsr/f977faaa-673e-4f66-b9bf-48c640241d47", "https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-scmr/705b624a-13de-43cc-b8a2-99573da3635f", "https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-tsch/d1058a28-7e02-4948-8b8d-4a347fa64931", "https://attack.mitre.org/techniques/T1003/006/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DCE/RPC traffic analysis (DRSUAPI, SVCCTL, ATSVC)

Much Windows lateral movement and credential theft runs over MS-RPC: either over SMB named pipes (`\svcctl`, `\atsvc`, `\lsarpc`) or directly over TCP via the endpoint mapper (135) and dynamic ports. Wireshark dissects the interfaces when it can see bind requests.

## Find the interfaces
- `dcerpc.cn_bind_to_uuid` / Wireshark shows interface names in bind/bind_ack. Statistics > Service Response Time > DCE-RPC lists interfaces and opnums seen.
- `epm` filter shows endpoint-mapper lookups (client asks 135 which port serves an interface UUID).
- Key UUIDs: DRSUAPI `e3514235-4b06-11d1-ab04-00c04fc2dcd2`; SVCCTL `367abb81-9844-35f1-ad32-98f038001003`; ATSVC `1ff70682-0a51-30e8-076d-740be8cee98b`; ITaskSchedulerService `86d35949-83c9-4044-b424-db363231fd0c`.

## DRSUAPI: DCSync
```text
drsuapi.opnum == 3      # DsGetNCChanges
```
Replication requests from a host that is not a domain controller indicate DCSync (T1003.006: Mimikatz `lsadump::dcsync`, Impacket `secretsdump -just-dc`). Note source IP, time, and the bind authentication (NTLM user or Kerberos ticket).

## SVCCTL: remote service creation (PsExec style)
```text
svcctl.opnum == 12 || svcctl.opnum == 24   # CreateServiceW / CreateServiceA (check dissector names)
svcctl.opnum == 19                          # StartServiceW
```
Payload often shows service name and binary path (`%COMSPEC% /C ...`, `\\ADMIN$\abcd.exe`) if not encrypted.

## ATSVC / Task Scheduler
`atsvc` (`NetrJobAdd`) and `ITaskSchedulerService` `SchRpcRegisterTask` carry task XML with the command (Impacket `atexec`).

## Encryption
Most modern RPC uses packet privacy (`dcerpc.auth_level == 6`), so stubs are encrypted. Wireshark decrypts NTLMSSP-protected RPC if given the user's NT hash or password (Preferences > Protocols > NTLMSSP) and Kerberos-protected traffic with a keytab (KRB5 preferences, "Try to decrypt Kerberos blobs"). Even encrypted, interface UUID, opnum, timing and sizes remain visible, which is often enough.

## Gotchas
- Without the bind (capture started mid-session), Wireshark cannot label the interface; use Decode As or the RPC context from an earlier capture.
- Legitimate DC-to-DC replication and management tools use the same opnums; baseline by source host role.

## Verify
Each suspicious RPC call is confirmed by host logs (DC 4662 with replication GUIDs for DCSync, 7045 for services, 4698 for tasks) at matching times.
