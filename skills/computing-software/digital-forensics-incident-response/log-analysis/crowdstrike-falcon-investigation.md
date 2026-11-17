---
id: computing-software.digital-forensics-incident-response.log-analysis.crowdstrike-falcon-investigation
name: crowdstrike-falcon-investigation
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [crowdstrike-falcon, edr, event-search, logscale, real-time-response, dfir]
level: practitioner
status: draft
description: "Investigate with CrowdStrike Falcon: detection process trees, key event types (ProcessRollup2, NetworkConnectIP4, DnsRequest), advanced event search queries, and RTR collection."
sources: ["https://www.crowdstrike.com/en-us/platform/endpoint-security/falcon-insight-xdr/", "https://library.humio.com/data-analysis/syntax.html", "https://www.crowdstrike.com/blog/tech-center/", "https://github.com/CrowdStrike/falconpy"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CrowdStrike Falcon investigation

Falcon records endpoint telemetry centrally, so you can investigate hosts that are offline or reimaged within retention. Console names change between releases (Investigate, Event Search, Advanced Event Search on LogScale/Next-Gen SIEM); concepts below are stable.

## Starting from a detection
The detection page shows the process tree with the triggering process, parent/child chain, command lines, hashes, network and file activity, and associated ATT&CK tactic/technique. Pivot from any process to its full event history. Note `aid` (agent ID, host), `TargetProcessId` (Falcon's unique process ID, not the OS PID) and timestamps.

## Event types to know
| Event (`#event_simpleName`) | Content |
|---|---|
| `ProcessRollup2` / `SyntheticProcessRollup2` | Process start: `ImageFileName`, `CommandLine`, `SHA256HashData`, `ParentProcessId`, `UserSid` |
| `NetworkConnectIP4` / `IP6`, `NetworkListenIP4` | Connections: `RemoteAddressIP4`, `RemotePort`, `ContextProcessId` |
| `DnsRequest` | `DomainName`, `ContextProcessId` |
| `UserLogon`, `UserLogonFailed2` | Logons with type and source |
| `PeFileWritten`, `NewExecutableWritten`, `*FileWritten` | File creation |
| `AsepValueUpdate`, `ScheduledTaskRegistered` | Persistence |
`ContextProcessId` / `TargetProcessId` join events to processes.

## Advanced event search (LogScale query language)
```text
#event_simpleName=ProcessRollup2 ImageFileName=/\\rundll32\.exe$/i CommandLine=/comsvcs/i
| table([@timestamp, ComputerName, UserName, CommandLine, ParentBaseFileName])
```
```text
#event_simpleName=DnsRequest DomainName=/bad-update\.example$/i
| groupBy([ComputerName, DomainName], function=count())
```
Join process to network: search `NetworkConnectIP4` for the remote IP, then search `ProcessRollup2` with `TargetProcessId` equal to the connection's `ContextProcessId` and the same `aid`.
Legacy Splunk-based Event Search used SPL syntax (`event_simpleName=ProcessRollup2 ...`); saved queries may need translation.

## Real Time Response (RTR)
Remote shell for collection and remediation: `ls`, `ps`, `netstat`, `get <file>` (retrieves to the console, size-limited), `memdump <pid>`, `reg query`, `runscript` (custom PowerShell), `put`/`run` (deploy and run tools like KAPE or WinPmem). RTR sessions are audited; record commands in the collection log. Network containment is a host action in the console.

## Automation
FalconPy (official Python SDK) wraps the APIs: detections, hosts, RTR sessions, event streams; use least-privilege API clients.

## Gotchas
- Telemetry retention depends on subscription (often 7 to 90 days); export what you need early.
- Falcon process IDs differ from OS PIDs; do not mix them across tools.
- Absence of an event can mean sensor not installed, offline, or filtered event type; check sensor coverage.

## Verify
Key events in the timeline are cited with `aid`, event type, timestamp and Falcon process ID, and RTR-collected files have hashes recorded.
