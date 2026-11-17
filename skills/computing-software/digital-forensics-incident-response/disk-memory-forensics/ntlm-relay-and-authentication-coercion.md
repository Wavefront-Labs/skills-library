---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.ntlm-relay-and-authentication-coercion
name: ntlm-relay-and-authentication-coercion
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [ntlm-relay, credential-theft, lateral-movement, petitpotam, dfir]
level: advanced
status: draft
description: "Detect NTLM relay and forced authentication (PetitPotam, PrinterBug, DFSCoerce, Responder poisoning): event patterns, network traces and hardening checks."
sources: ["https://attack.mitre.org/techniques/T1557/001/", "https://attack.mitre.org/techniques/T1187/", "https://support.microsoft.com/en-us/topic/kb5005413-mitigating-ntlm-relay-attacks-on-active-directory-certificate-services-ad-cs-3612b773-4043-4aa9-b23d-b87910cd3429"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NTLM relay and authentication coercion

**Goal:** attackers trick a host (often a DC) into authenticating to them, then relay that NTLM
authentication to another service (AD CS web enrollment, LDAP, SMB) to gain its privileges.

## Coercion methods
| Method | RPC interface | Artefacts on victim |
|---|---|---|
| PetitPotam | MS-EFSRPC (`\pipe\efsrpc`, `\pipe\lsarpc`) | 5145 named pipe access to `lsarpc`/`efsrpc` from attacker IP; EFS events |
| PrinterBug / SpoolSample | MS-RPRN (`\pipe\spoolss`) | Print Spooler connection from attacker; `RpcRemoteFindFirstPrinterChangeNotificationEx` |
| DFSCoerce | MS-DFSNM (`\pipe\netdfs`) | 5145 to `netdfs` |
| ShadowCoerce | MS-FSRVP | File Server VSS Agent |
| LLMNR/NBT-NS/mDNS poisoning (Responder) | name resolution spoofing | Victims send auth to attacker for mistyped names |

## Relay evidence
- On the relay **target**: 4624 logon type 3 with **NTLM** for the *victim machine account*
  (e.g. `DC01$`) but `IpAddress` = attacker's host, not DC01's IP. This mismatch is the key signal.
- AD CS ESC8: IIS logs on the CA web enrollment (`/certsrv/certfnsh.asp`) with requests from the attacker IP, CA 4886/4887 issuing a DC template certificate to `DC01$`.
- LDAP relay: 5136 directory changes (RBCD `msDS-AllowedToActOnBehalfOfOtherIdentity`, shadow credentials) by the relayed account.
- Network: SMB/HTTP NTLMSSP sessions where the NTLM `Workstation` field does not match the source IP's hostname (Zeek `ntlm.log`).

## Hardening checks (report as contributing factors)
- SMB signing required, LDAP signing and channel binding, EPA on AD CS HTTP / disable HTTP enrollment.
- Print Spooler disabled on DCs; LLMNR/NBT-NS disabled; patch coercion CVEs; restrict NTLM (audit with 8001-8004 NTLM operational events).

## Gotchas
- Machine-account NTLM logons are normal from the machine's own IP; always compare IP to the account's host.
- Responder activity may be visible only in network data, not host logs.

## Verify
Each relayed authentication is paired with the coercion event and the action it was used for.
