---
id: computing-software.cybersecurity-defensive.nessus.nessus-agent-scans-and-scan-windows
name: nessus-agent-scans-and-scan-windows
category: computing-software
field: cybersecurity-defensive
product: nessus
tags: [nessus, nessus-agents, agent-scan-windows, agent-groups, tenable-vulnerability-management, endpoint-scanning, nessus-deployment]
level: practitioner
status: draft
description: "Configure Nessus/Tenable agent scans: agent groups, scan windows, triggered and scheduled agent scans, plugin sets for agents, and gaps caused by offline laptops."
sources: ["https://docs.tenable.com/nessus/Content/AgentScans.htm", "https://docs.tenable.com/vulnerability-management/Content/Scans/AgentScans.htm", "https://docs.tenable.com/nessus-agent/Content/AgentScanWindows.htm"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Agent scans and scan windows

Agents run local checks on hosts that network scans reach poorly (laptops, cloud VMs, hosts without
credential access). They do not do remote network checks.

## Agent groups
Group by purpose and schedule: `laptops-global`, `servers-prod`, `servers-dev`. A host can be in
several groups. Assign via linking key group parameter:
`nessuscli agent link --key=<KEY> --host=<manager> --port=8834 --groups="servers-prod"`.

## Scan window
Agent scans have a **scan window** (e.g. 24 hours): the scan launches, agents that check in during
the window run it and upload results; the scan completes when the window ends. Offline agents miss it.
- Laptops: daily scans with 24 h windows; servers: daily or weekly with 3-6 h windows.
- Tenable VM supports **triggered agent scans** (run on a schedule interval or file-name trigger on
  the agent, results uploaded whenever) instead of fixed windows: best for intermittent laptops.

## Templates
- Basic Agent Scan, Advanced Agent Scan, Policy Compliance Auditing (agent), Malware Scan.
- Choose plugin families to keep runtime low; agents throttle CPU (agent setting
  `process_priority=low`).

## Coverage monitoring
- Agents not scanned in X days: Tenable VM Explore filter "Last Scanned" per agent group; Nessus
  Manager Agents page last-scanned column.
- Agent unlinked/missing: compare against EDR/CMDB inventory.

## Gotchas
- A short scan window with a large group can overload the manager uploads; stagger groups.
- Agents and network scans can create duplicate assets; see asset deduplication rules.
- Agent plugin updates are pushed from the manager; offline agents run stale plugins until they sync.

## Verify
Scan history shows results count close to group size; agents last-scan age under target for 95%
of the group.
