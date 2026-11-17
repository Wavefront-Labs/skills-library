---
id: computing-software.digital-forensics-incident-response.log-analysis.sysmon-wmi-events-19-21
name: sysmon-wmi-events-19-21
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [sysmon-wmi-events, sysmon, wmi-persistence, windows-event-logs, dfir]
level: practitioner
status: docs-checked
description: "Detect WMI event subscription persistence with Sysmon events 19, 20 and 21: what each logs, the WmiEvent filter tag and what to corroborate."
sources: ["https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon", "https://attack.mitre.org/techniques/T1546/003/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sysmon WMI events 19-21

MITRE ATT&CK T1546.003: adversaries use WMI event filters, providers, consumers and bindings
to run code when a defined event occurs (examples given: wall clock time, user login, computer
uptime), for persistence and privilege escalation. They may also compile WMI scripts into MOF
files with `mofcomp.exe`. Subscription execution is proxied by the WMI Provider Host process
(`WmiPrvSe.exe`) and so may run as SYSTEM.

Sysmon logs each stage:

| Event | Name | What the Sysmon docs say it logs |
|---|---|---|
| 19 | WmiEvent (WmiEventFilter activity detected) | WMI namespace, filter name and filter expression when a filter is registered |
| 20 | WmiEvent (WmiEventConsumer activity detected) | Consumer name, log and destination when a consumer is registered |
| 21 | WmiEvent (WmiEventConsumerToFilter activity detected) | Consumer name and filter path when a consumer binds to a filter |

All three are filtered through the `WmiEvent` tag under `EventFiltering`. Events go to
Applications and Services Logs/Microsoft/Windows/Sysmon/Operational with UTC timestamps. Run
`sysmon -s` to print the schema with the exact field names for your Sysmon version.

## Config
```xml
<RuleGroup name="" groupRelation="or">
  <WmiEvent onmatch="exclude"/>
</RuleGroup>
```
With `onmatch="exclude"` events are included except those matching a rule, so an empty exclude
set logs everything. Add exclusions only after you have allowlisted known-good subscriptions.

## Hunting
- Consumer destinations that launch shells, scripting hosts or encoded commands.
- Filter expressions that fire at startup or on a timer, matching the trigger types MITRE lists.
- `mofcomp.exe` command lines, Register-WmiEvent usage in PowerShell, and unusual child
  processes of `WmiPrvSe.exe` (the MITRE detection strategy for this technique).
- Subscriptions you cannot match to an approved management tool.

## Mitigations named by MITRE
Attack Surface Reduction rules on Windows 10; restrict who may connect remotely using WMI (by
default only administrators can).

## Verify
Every 19/20/21 cluster is classified as allowlisted or malicious, with the filter, consumer and
binding matched together by name.

## Checked
2026-11-09. Confirmed on the Sysmon page (read in full) and the MITRE T1546.003 page (read in full): event 19/20/21 descriptions, WmiEvent tag, log location, UTC, `-s` schema switch, exclude semantics, MITRE description, WmiPrvSe.exe, mofcomp.exe, detection strategy and mitigations. Removed: per-event field lists (Operation, User, EventNamespace, Type), WMI-Activity 5861 and 4624 correlation, example WQL query, trigger-word list, the `Get-CimInstance` confirm commands, OBJECTS.DATA tools, Velociraptor artifact, legitimate-software examples.
Method: documentation only; no commands were run.
