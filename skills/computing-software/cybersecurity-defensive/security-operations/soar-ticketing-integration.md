---
id: computing-software.cybersecurity-defensive.security-operations.soar-ticketing-integration
name: soar-ticketing-integration
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [soar, ticketing-integration, servicenow, jira, case-management, bidirectional-sync, itsm]
level: practitioner
status: draft
description: "Integrate SIEM and SOAR with ITSM ticketing: when to create tickets, field mapping, bidirectional status sync, assignment to resolver teams and avoiding duplicates."
sources: ["https://docs.splunk.com/Documentation/SOAR/current/Playbook/Overview", "https://learn.microsoft.com/en-us/azure/sentinel/automation/automation", "https://www.servicenow.com/docs/bundle/xanadu-security-management/page/product/security-incident-response/concept/c_SecurityIncidentResponse.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ticketing and case management integration

**Goal:** security work that needs other teams (rebuild a server, patch, reset, block a
port) flows into their ITSM queue with context, and status flows back, without duplicates
or lost updates.

## Decide the system of record
- SOC investigation lives in the SIEM/SOAR case (Sentinel incident, Splunk ES/SOAR
  container, XSOAR incident) or in a security incident module (ServiceNow SIR).
- Remediation tasks for other teams live in ITSM (ServiceNow, Jira Service Management).
Do not mirror every alert into ITSM; create tickets when another team must act.

## Mapping
| Security case | ITSM ticket |
|---|---|
| case ID, link | correlation ID / external reference |
| severity | priority (map explicitly, e.g. SEV1 to P1) |
| affected host/user | configuration item, caller/affected user |
| summary, required action | short description, description with steps and due date |
| owner team | assignment group (from CMDB CI support group or asset tags) |

Never put raw sensitive evidence (credentials, full PII) in widely visible tickets; link back
to the restricted case instead. Use security-incident ticket types with restricted ACLs where
available.

## Sync
- Create ticket via the SOAR connector or API; store the ticket number in the case.
- Bidirectional: ITSM state changes (resolved, needs info) update the case via webhook or
  polling; case closure resolves open security tickets or flags them.
- Comments: sync work notes in one direction only to avoid loops, or tag synced comments.

## Duplicates
Use a deterministic key (case ID + action type + CI). Before creating, query for an open
ticket with that key and append instead.

## SLAs
Set due dates from the security severity and track them in ITSM reporting; escalate breaches
to the resolver team's manager automatically.

## Gotchas
- Auto-closing tickets when a case closes can hide unfinished remediation; close only
  informational tickets automatically.
- Integration service accounts expiring or losing roles break sync silently; alert on API errors.

## Verify
Create a test case, push a ticket, change its state in ITSM, and confirm the case reflects it;
retry creation and confirm no duplicate is created.
