---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.detecting-lsass-memory-dumping
name: detecting-lsass-memory-dumping
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [lsass-dumping, credential-theft, lsass, procdump, comsvcs, sysmon, dfir]
level: practitioner
status: docs-checked
description: "Detect LSASS memory dumping (Mimikatz, procdump, comsvcs MiniDump, Task Manager, silent process exit) from command lines and dump files; assess exposure and harden."
sources: ["https://attack.mitre.org/techniques/T1003/001/", "https://www.microsoft.com/en-us/security/blog/2022/10/05/detecting-and-preventing-lsass-credential-dumping-attacks/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Detecting LSASS memory dumping

**Goal:** find whether credentials were dumped from LSASS, by which tool, and which accounts were exposed. After a user logs on, credential material is held in LSASS process memory and can be harvested by an administrative user or SYSTEM (ATT&CK T1003.001).

## Methods and what to look for
| Method (documented) | Where to look |
|---|---|
| `procdump -ma lsass.exe lsass_dump` | process creation command line (`procdump` with `-ma` against lsass); dump file creation |
| `rundll32.exe comsvcs.dll MiniDump <PID> lsass.dmp full` | command line containing `comsvcs.dll` and `MiniDump` |
| Task Manager (`Taskmgr.exe`) | listed by Microsoft among the most common LOLBin routes; look for a dump file written by Task Manager |
| Mimikatz (`sekurlsa::logonPasswords`, or `sekurlsa::Minidump` on a dump moved offline) | process access to lsass from an unexpected process; offline analysis leaves the dump file |
| Silent process exit abuse | a dump created through Windows Error Reporting (`WerFault.exe`); check IFEO / SilentProcessExit registry configuration (see the IFEO skill in this product) |

Microsoft's October 2022 blog (March-August 2022 data) names comsvcs.dll via rundll32, Mimikatz and variants, `procdump.exe -ma` and `taskmgr.exe` as the popular routes, all of them signed, legitimate binaries or common tools.

## Telemetry
- Process creation with command lines for the tools above.
- ATT&CK's analytic: an abnormal process opens a handle to `lsass.exe` with full access (0x1F0FFF), then a memory dump, file creation or registry modification follows. Use your EDR or Sysmon process-access telemetry to find that chain, filtering known security-product callers.
- Dump files: search for new dump files written near the incident window.
- Microsoft Defender for Endpoint offers an attack surface reduction rule that blocks credential stealing from LSASS; Microsoft says it alone prevented all 15 tested dumping techniques in its in-house test.
- Attackers also tamper with settings: enabling `UseLogonCredential` in the WDigest registry settings brings plaintext passwords into memory (Defender flags this as Behavior:Win32/WDigestNegMod.B).

## Exposure assessment
Assume credentials of accounts that have logged on to the host and still have material in LSASS are exposed (ATT&CK lists the MSV, WDigest, Kerberos and CredSSP packages as sources). Use logon records to list accounts, then drive resets. Check hardening state:
- Protected Process Light for LSA (ATT&CK: Windows 8.1 / Server 2012 R2 and later; Microsoft: on by default for new enterprise-joined Windows 11 22H2 installs).
- Credential Guard (ATT&CK: not configured by default, with hardware and firmware requirements, and no protection against every dumping form; Microsoft: default on for Windows 11 Enterprise).
- WDigest `UseLogonCredential` disabled; restricted admin mode for RDP; consider restricting NTLM; unique local administrator passwords.

## Verify
Tool execution time, the lsass access event and dump file creation align; the exposed account list is handed to the credential reset plan.

## Checked
2026-11-08. Confirmed against ATT&CK T1003.001 and the Microsoft Threat Intelligence blog of 2022-10-05: dump commands, silent process exit route, popular LOLBins, access 0x1F0FFF analytic, ASR rule, WDigest tampering, PPL and Credential Guard statements and mitigations. Removed as unconfirmed: Prefetch names, Sysmon event 10 access mask lists, DLL-load indicators, ASR event IDs, Defender table query, the 30 MB size heuristic and the RunAsPPL registry path.
Method: documentation only; no commands were run.
