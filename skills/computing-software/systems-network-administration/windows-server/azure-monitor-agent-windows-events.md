---
id: computing-software.systems-network-administration.windows-server.azure-monitor-agent-windows-events
name: azure-monitor-agent-windows-events
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, azure-arc, azure-monitor-agent, ama, data-collection-rule, dcr, log-analytics, windows-event-logs, xpath, performance-counters, kql]
level: practitioner
status: gated
description: "Collect Windows events and counters into Log Analytics with Azure Monitor Agent: data collection rules, XPath filters to control cost, association, and KQL checks."
sources:
  - https://learn.microsoft.com/en-us/azure/azure-monitor/agents/azure-monitor-agent-overview
  - https://learn.microsoft.com/en-us/azure/azure-monitor/agents/data-collection-rule-azure-monitor-agent
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Monitor Agent: Windows events and counters

Azure Monitor Agent (AMA) collects data according to **data collection rules (DCRs)** associated with the agent;
configuration lives in the DCR, not on the agent.

## Deploy the agent
- Azure VMs and Arc servers: creating a DCR in the portal and adding the machines installs the agent and creates the
  association (Learn's recommended path); use Azure Policy for scale.
- When resources are added to a DCR, the portal's default is to enable a system-assigned managed identity.

## Create a DCR for Windows events
Portal > Monitor > Data Collection Rules > Create: platform Windows, resources (or use
policy for association), Data sources:
- **Windows Event Logs**: collect only the logs and levels you need (the portal offers basic selection and custom
  XPath; see Learn's DCR creation page for the syntax).
- **Performance counters**: pick the counters and sample rate you need.
- Destination: Log Analytics workspace. Learn notes the Azure Monitor path writes the `Event` table and the Microsoft
  Sentinel path the `SecurityEvent` table; do not collect the same security events twice.

## Check data arrives
```kusto
Heartbeat | where Computer startswith "app01" | summarize max(TimeGenerated) by Computer, Category
Event | where TimeGenerated > ago(1h) | summarize count() by Computer, EventLog
```

## Cost control
Start narrow and widen when a use case needs it. DCR transformations can filter or reshape data before ingestion; see
the DCR pages and the vendor pricing page for cost.

## Verify
- [ ] A recent Heartbeat record for each server (Learn: a healthy agent sends one every minute).
- [ ] Event volume per server per day is within the budget you set.

## Checked
2026-10-28. Confirmed on Learn (AMA overview, DCR creation page): DCRs define what is collected and where it goes, portal DCR creation
installs and associates the agent, default system-assigned managed identity, Heartbeat table every minute,
Event vs SecurityEvent tables, DCR transformations. Removed as unconfirmed: MMA retirement date, extension name, policy
initiative names, XPath examples and Get-WinEvent test, counter list and 60 s interval, Sentinel connector name, billing
statement. The two KQL queries are standard Log Analytics usage on Heartbeat and Event tables (gated: unconfirmed, source is paywalled or blocked).
Method: documentation only; no commands were run.
