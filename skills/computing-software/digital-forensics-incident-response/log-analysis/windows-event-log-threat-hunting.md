---
id: computing-software.digital-forensics-incident-response.log-analysis.windows-event-log-threat-hunting
name: windows-event-log-threat-hunting
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [log-analysis, threat-hunting, windows-event-logs, evtx, event-id, 4624, 4625, 4688, 4698, 4720, 7045, 1102, sysmon, powershell-logging, 4104, logon-types, lateral-movement, siem, splunk, kql, sentinel, elastic, chainsaw, hayabusa, sigma, mitre-attack, hypothesis-driven-hunting, detection-gaps]
level: practitioner
status: draft
description: "Hypothesis-driven hunting in Windows event logs: the event IDs and logon types that matter, Sysmon and PowerShell logging, fast EVTX triage with Hayabusa/Chainsaw, SIEM queries."
sources: ["https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/", "https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon", "https://github.com/SigmaHQ/sigma", "https://attack.mitre.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Windows event log threat hunting

**Goal:** find intrusion activity in Windows logs by testing specific hypotheses
("someone is moving laterally with stolen admin creds"), knowing which events would
prove or disprove each one, and recording where logging is missing.

## The events that carry most hunts
| ID (log) | Meaning | Hunt use |
|---|---|---|
| 4624 / 4625 (Security) | Logon success / failure | Logon type is the key field (below). Bursts of 4625 = brute force / spraying. |
| 4648 | Logon with explicit credentials (`runas`, some lateral tools) | Source of lateral movement. |
| 4672 | Special privileges assigned | Admin-equivalent logon; pair with 4624 by Logon ID. |
| 4688 | Process creation | Only useful with **"Include command line in process creation events"** policy enabled. |
| 4698 / 4702 | Scheduled task created / updated | Persistence, remote execution. |
| 4720, 4728/4732/4756 | Account created; added to security groups | Persistence, privilege escalation. |
| 4768 / 4769 (DC) | Kerberos TGT / service ticket | 4769 with RC4 (`0x17`) encryption for many SPNs = Kerberoasting. |
| 7045 (System) | Service installed | PsExec-style execution, persistence. |
| 1102 (Security) / 104 (System) | Log cleared | Almost always worth an explanation. |
| 4104 (PowerShell/Operational) | Script block logging | Decoded script contents — gold for `-enc` payloads. |
| Sysmon 1 / 3 / 11 / 13 / 22 | Process (with hashes, parent), network connection, file create, registry set, DNS query | Far richer than native auditing; deploy with a maintained config. |

**Logon types (4624):** 2 interactive, 3 network (SMB, many lateral tools), 4 batch
(scheduled tasks), 5 service, 7 unlock, 9 new credentials (`runas /netonly`), 10
RemoteInteractive (RDP), 11 cached. A workstation receiving type 3/10 logons from
another workstation is a classic lateral-movement signal — workstations rarely
administer each other.

## Hunting loop
1. **Hypothesis** tied to a technique, e.g. ATT&CK T1021.002 (SMB/admin shares):
   "an account is authenticating to many hosts with type 3 in a short window."
2. **Data check:** is the needed log collected from those hosts, with the right audit
   policy? If not, that is a *detection gap* finding — write it down.
3. **Query**, baseline, and look at the outliers (rare = interesting).
4. **Conclude:** confirmed activity → open an incident; benign → document and,
   if it's a good pattern, turn the query into a detection rule (Sigma for portability).

## Example queries
Splunk (field names depend on your add-on):
```spl
index=wineventlog EventCode=4624 Logon_Type=3 NOT user="*$"
| bin _time span=1h
| stats dc(dest) as hosts values(dest) as targets by _time, user, src
| where hosts > 5
```
KQL (Microsoft Sentinel / Defender):
```kql
SecurityEvent
| where EventID == 4688
| where ParentProcessName endswith @"\winword.exe" or ParentProcessName endswith @"\excel.exe"
| where NewProcessName has_any ("powershell.exe","cmd.exe","wscript.exe","mshta.exe","rundll32.exe")
| project TimeGenerated, Computer, Account, ParentProcessName, CommandLine
```

## Offline EVTX triage (no SIEM)
```bash
hayabusa csv-timeline -d ./evtx/ -o hayabusa.csv     # Sigma-based detections + timeline (check `hayabusa help` for current flags)
chainsaw hunt ./evtx/ -s sigma/ --mapping mappings/sigma-event-logs-all.yml
```
Collect logs from `%SystemRoot%\System32\winevt\Logs\` (copy, don't export via the GUI on
the suspect box if you can avoid it). Both tools produce leads, not verdicts: verify
each hit in the raw event.

## Gotchas
- Default Windows audit policy misses a lot (no command lines, no 4698 on some
  builds). Default Security log size (~20 MB) can roll over in hours on a DC — check the
  oldest event date before saying "no evidence".
- Times in EVTX are UTC; SIEM display often converts to local — confirm.
- Machine accounts (`HOST$`) generate huge volumes of type 3 logons; filter them.
- An absent event is not proof of absence unless you showed the log covers that time.

## Verify
- [ ] Each hunt states its hypothesis and ATT&CK technique.
- [ ] Log coverage and retention for the hunt window confirmed (oldest event checked).
- [ ] Hits verified in raw events, with host, account, time (UTC) and logon ID.
- [ ] Gaps recorded as findings; useful queries promoted to detections.
