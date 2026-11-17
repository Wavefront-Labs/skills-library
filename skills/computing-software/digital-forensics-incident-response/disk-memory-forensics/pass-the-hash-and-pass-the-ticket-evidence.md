---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.pass-the-hash-and-pass-the-ticket-evidence
name: pass-the-hash-and-pass-the-ticket-evidence
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [pass-the-hash, pass-the-ticket, overpass-the-hash, credential-theft, 4624, kerberos, dfir]
level: advanced
status: draft
description: "Recognise pass-the-hash, overpass-the-hash and pass-the-ticket in Windows logs: logon type 9 seclogo, NTLM type 3 patterns, Kerberos 4768/4769 anomalies and memory evidence."
sources: ["https://attack.mitre.org/techniques/T1550/002/", "https://attack.mitre.org/techniques/T1550/003/", "https://jpcertcc.github.io/ToolAnalysisResultSheet/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pass-the-hash and pass-the-ticket evidence

**Goal:** identify use of stolen NTLM hashes or Kerberos tickets instead of passwords.

## Pass-the-hash (NTLM)
- **Source host** (Mimikatz `sekurlsa::pth`): Security 4624 **logon type 9**
  (NewCredentials), `LogonProcessName` = `seclogo`, `AuthenticationPackageName` =
  `Negotiate`, with the *original* user in subject and new credentials not shown; Sysmon 10
  on lsass from mimikatz; 4648 is not generated.
- **Destination**: 4624 type 3, `AuthenticationPackageName` = `NTLM`, `LmPackageName`
  NTLM V2, `KeyLength` 0, from a workstation where that account normally uses Kerberos;
  4776 on the DC (NTLM validation) for domain accounts; local admin PtH with RID 500 or
  LocalAccountTokenFilterPolicy.
- Impacket tools (psexec, wmiexec, smbexec with `-hashes`) produce NTLM type 3 logons with
  `WorkstationName` often random or empty.

## Overpass-the-hash / pass-the-key
NTLM hash or AES key used to request a TGT: DC 4768 with `TicketEncryptionType` **0x17
(RC4)** for an account/domain that normally uses AES (0x12), from the attacker's host IP.

## Pass-the-ticket
- Stolen/forged tickets injected (`kerberos::ptt`, Rubeus `ptt`): destination 4624 type 3
  Kerberos from a host IP not matching where the user logged on; 4769 service ticket
  requests without a preceding 4768 from that host for the user.
- Memory: `klist` on live host or Volatility/MemProcFS shows tickets for users not logged on.
- Rubeus `asktgt` artefacts: 4768 from unusual process on source with RC4.

## Hunting tips
Baseline NTLM usage (`4624 | where AuthenticationPackageName == "NTLM"`), alert on NTLM
logons by privileged accounts and logon type 9 with seclogo.

## Verify
For each suspected PtH/PtT logon, show the mismatch (protocol, encryption type, source host)
versus the account's normal pattern, and link to the credential theft event earlier.
