---
id: computing-software.cybersecurity-defensive.security-operations.lateral-movement-hunting
name: lateral-movement-hunting
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [threat-hunting, lateral-movement-hunting, psexec, wmi, winrm, rdp, remote-services, t1021, logon-type-3]
level: advanced
status: docs-checked
description: "Hunt for lateral movement on Windows estates: remote service creation, WMI/WinRM execution, RDP pivots, admin share use, logon types in 4624, and baselining who administers what."
sources: ["https://attack.mitre.org/tactics/TA0008/", "https://attack.mitre.org/techniques/T1569/002/", "https://attack.mitre.org/techniques/T1021/002/", "https://attack.mitre.org/techniques/T1021/006/", "https://attack.mitre.org/techniques/T1047/", "https://www.jpcert.or.jp/english/pub/sr/ir_research.html", "https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4624", "https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-devicelogonevents-table", "https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-deviceprocessevents-table"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lateral movement hunting

ATT&CK describes Lateral Movement (TA0008) as techniques to enter and control remote systems:
adversaries may install their own remote access tools or use legitimate credentials with
native tools, which may be stealthier. The latter looks like administration.

## Baseline first
Build a list of who legitimately administers what: jump hosts, management servers, IT admin
accounts. The hunt is for remote execution that does not fit that graph. ATT&CK T1072
(Software Deployment Tools) is a reminder that central deployment suites are themselves a
route: watch who can use them.

## Techniques and their traces
**Service execution (T1569.002)**: abuses the service control manager (`services.exe`,
driven by `sc.exe`, `net` or PsExec-style tools).
- Target: Security 4697 "A service was installed in the system" (Audit Security System
  Extension subcategory); System log 7045 (ATT&CK cites a ransomware case run through
  Service Control Manager event 7045); `services.exe` with an unusual child process.
- Source: 4648 "A logon was attempted using explicit credentials".

**WMI (T1047)**: remote WMI over DCOM uses port 135; WMI over WinRM uses 5985 (HTTP) and
5986 (HTTPS). WMI event-subscription execution is proxied by `WmiPrvSe.exe` (T1546.003).

**WinRM (T1021.006)**: WinRM is both a Windows service and a protocol; it can be called with the
`winrm` command or from programs such as PowerShell, and can be used to reach WMI.

**RDP (T1021.001)**: Security 4624 with Logon Type 10 (RemoteInteractive, Terminal Services
or Remote Desktop). Type 12 is CachedRemoteInteractive. Type 7 is Unlock (not a reconnect).
In Windows 10 and later 4624 also records `Restricted Admin Mode` for RemoteInteractive logons.

**SMB and admin shares (T1021.002)**: ATT&CK examples include copying files to `ADMIN$` and
using `C$` and `ADMIN$`. Audit with 5140 (network share object accessed) and 5145 (network
share object checked for desired access).

**Remote scheduled tasks (T1053.005)**: Security 4698 "A scheduled task was created" (Audit Other
Object Access Events subcategory).

**Alternate authentication material (T1550)**: pass-the-hash (.002), pass-the-ticket (.003),
application access tokens (.001) and web session cookies (.004).

## Reading 4624
Logon types: 2 Interactive, 3 Network, 4 Batch, 5 Service, 7 Unlock, 8 NetworkCleartext,
9 NewCredentials, 10 RemoteInteractive, 11 CachedInteractive. Useful fields: `Logon Process`,
`Authentication Package` (NTLM, Kerberos, Negotiate), `Workstation Name`, `Source Network
Address`, `Process Name`, `Logon ID` (correlates with 4672, 4648), `Elevated Token`.
Microsoft's monitoring guidance: alert on accounts that should never log on from a given
computer, address or workstation; on service or batch logon types used by administrative
group members; on NTLM where it should not be used; on `Key Length` other than 128 for NTLM
(`Key Length` is 0 for Kerberos, and also 0 when Kerberos was negotiated). Source address and
port, and workstation name, depend on protocol: Kerberos network logons likely have no
workstation name, NTLM logons have no TCP/IP details.

## Hunt queries (Defender advanced hunting)
```kql
DeviceProcessEvents
| where InitiatingProcessFileName in~ ("wmiprvse.exe","services.exe")
| where FileName in~ ("cmd.exe","powershell.exe","rundll32.exe","mshta.exe")
| summarize count(), hosts=dcount(DeviceName) by InitiatingProcessFileName, FileName, ProcessCommandLine
| order by hosts asc
```
```kql
DeviceLogonEvents
| where LogonType == "Network" or LogonType has "Remote"
| summarize targets=dcount(DeviceName) by AccountName, RemoteIP
| where targets > 10
```
`LogonType` in this table has Interactive, Remote interactive (RDP), Network (including access
via PsExec or to shared resources), Batch and Service. A workstation authenticating to many
workstations is rarely normal; tune the threshold to your estate and check the `ActionType`
values in your own schema before filtering on success.

## Graph view
Plot source-to-target edges for admin logons over a representative window; new edges
(first-seen pairs) and workstation-to-workstation or workstation-to-DC edges are leads.

## Gotchas
- 4624 type 3 is very common (file shares, GPO); filter by privileged accounts and by process
  context.
- JPCERT/CC's "Detecting Lateral Movement through Tracking Event Logs" and its Tool Analysis
  Result Sheet (https://jpcertcc.github.io/ToolAnalysisResultSheet/) document which logs
  common attacker tools leave and which settings produce them; use them to confirm your
  audit policy is capturing the evidence before trusting negatives.

## Verify
Run a sanctioned PsExec or WMI test between two lab hosts and confirm each query catches it.

## Checked
2026-11-08. Confirmed against ATT&CK TA0008 and the T1569.002, T1047, T1021.001, T1021.002
and T1021.006 pages; Microsoft Learn event 4624 (logon types, Key Length, Restricted Admin
Mode, monitoring recommendations), 4697, 4698, 4648, 5140 and 5145 pages; the Defender
`DeviceLogonEvents` and `DeviceProcessEvents` table pages (column names, LogonType meanings);
the JPCERT/CC research page. Corrected: Logon Type 7 is Unlock, not reconnect. Removed:
`PSEXESVC` and `RemCom` pipes, Impacket wmiexec `ADMIN$\__` output, `wsmprovhost.exe`, WinRM
Operational event 91, TerminalServices events 21/22/25 and 1149, `mstsc`/`Default.rdp`
artefacts, the pass-the-hash "key length 0 / NtLmSsp" rule (4624 says Key Length is 0 for
Kerberos), and `wmiprvse`-spawning-cmd as a WMI remote-execution signature (only the proxied
subscription statement is on the ATT&CK page).
Method: documentation only; no commands were run.
