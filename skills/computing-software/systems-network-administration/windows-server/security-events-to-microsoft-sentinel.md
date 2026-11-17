---
id: computing-software.systems-network-administration.windows-server.security-events-to-microsoft-sentinel
name: security-events-to-microsoft-sentinel
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, security-auditing, microsoft-sentinel, azure-monitor-agent, windows-security-events, data-collection-rule, log-analytics, securityevent, kql]
level: practitioner
status: docs-checked
description: "Ship Windows Server security events to Microsoft Sentinel via the Windows Security Events AMA connector: event sets, DCRs, Arc onboarding and KQL checks."
sources:
  - https://learn.microsoft.com/en-us/azure/sentinel/data-connectors/windows-security-events-via-ama
  - https://learn.microsoft.com/en-us/azure/sentinel/windows-security-event-id-reference
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ship Windows security events to Microsoft Sentinel

## Path
Server (Azure VM or Azure Arc-enabled on-prem) > Azure Monitor Agent (AMA) > Data
Collection Rule (DCR) > Log Analytics workspace with Sentinel > `SecurityEvent` table.

## Steps
1. Use the "Windows Security Events via AMA" connector and create a data collection rule.
2. Choose the event set:
| Set | Contents |
|---|---|
| Minimal | a small set of events that might indicate potential threats |
| Common | the standard audit-trail set |
| All | the full, unfiltered set of security events |
| Custom | XPath, e.g. `Security!*[System[(EventID=4624 or EventID=4625)]]` |

## Prerequisite: generate the events
The connector only ships events that Windows records, so the audit policy must generate them first.

## Verify in KQL
```kusto
SecurityEvent
| where TimeGenerated > ago(1h)
| summarize count() by Computer, EventID
| order by count_ desc
```

## Verify
- [ ] Each server has recent SecurityEvent rows.

## Checked
2026-10-28: Confirmed on Learn pages windows-security-events-via-ama and windows-security-event-id-reference: AMA connector writes to the SecurityEvent table; event sets Minimal, Common, All and Custom (Custom uses XPath in a data collection rule). Removed: legacy agent retirement claim, Arc onboarding command, Content hub steps, cost wording, automatic AMA install claim, Heartbeat query, cost-control section (noisy ID claims, WEF suggestion).
Method: documentation only; no commands were run.
