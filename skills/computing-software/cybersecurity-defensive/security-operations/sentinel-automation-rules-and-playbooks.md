---
id: computing-software.cybersecurity-defensive.security-operations.sentinel-automation-rules-and-playbooks
name: sentinel-automation-rules-and-playbooks
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [microsoft-sentinel, logic-apps-playbooks, automation-rules, soar, incident-automation, managed-identity, playbook-permissions]
level: advanced
status: docs-checked
description: "Automate Microsoft Sentinel with automation rules and Logic Apps playbooks: triggers, managed identity permissions, enrichment and safe response actions."
sources: ["https://learn.microsoft.com/en-us/azure/sentinel/automate-incident-handling-with-automation-rules", "https://learn.microsoft.com/en-us/azure/sentinel/automation/automate-responses-with-playbooks", "https://github.com/Azure/Azure-Sentinel/tree/master/Solutions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sentinel automation rules and Logic Apps playbooks

**Goal:** remove repetitive analyst work (tagging, assignment, enrichment, known-benign
closure) and run approved containment, with an audit trail.

## Automation rules (no code, run first)
Trigger on incident created/updated or alert created. Conditions on analytic rule name,
entities, tags, severity, custom details. Actions: assign owner, change status/severity,
add tag, add task list, run playbook, set expiry.
Typical set, ordered by `order` number:
1. Tag and assign by rule family (identity incidents to the IAM queue).
2. Add a task checklist for the analyst (Sentinel incident tasks).
3. Run enrichment playbook.
4. Auto-close known benign test accounts with a classification and comment, with an
   expiration date so suppression does not live forever.

## Playbooks (Logic Apps)
- Use the **Microsoft Sentinel incident** trigger (not the legacy alert trigger) so the
  playbook gets all alerts and entities.
- Authenticate with a **system-assigned managed identity**; grant it only what it needs:
  *Microsoft Sentinel Responder* on the workspace to comment/update, Graph application
  permissions for user actions, Defender for Endpoint API permissions for isolation.
- Grant the Sentinel service account *Microsoft Sentinel Automation Contributor* on the
  playbook's resource group, otherwise automation rules cannot run it.

## Enrichment pattern
For each IP/URL/hash entity: query reputation (VirusTotal, internal TI), sign-in history
for the account, device owner from CMDB; write a single formatted incident comment.
Use `For each` with concurrency control to avoid API rate limits.

## Response pattern with guardrails
- Containment (disable user, revoke sessions, isolate device) via a playbook triggered
  manually from the incident, or automatically only for high-confidence rules.
- Add an approval step (Teams adaptive card or email) for actions on privileged accounts
  or servers; exclude break-glass and service accounts by group membership check.
- Always comment on the incident what was done and by which playbook run.

## Gotchas
- Logic Apps Standard vs Consumption: Consumption is simplest; Standard for VNet integration.
- Connector API connections created with a user's credentials break when that user leaves;
  use managed identity.
- Playbook failures are silent unless you monitor run history (send to Log Analytics via
  diagnostic settings and alert on failed runs).

## Checked
2026-10-28. Confirmed in the automation rules and playbooks pages: roles Microsoft Sentinel Responder, Microsoft Sentinel Automation Contributor (lets automation rules run playbooks) and Playbook Operator; incident trigger. Nothing removed.
Method: documentation only; no commands were run.

## Verify
Create a test incident with a lab entity, confirm the automation rule ran (incident
activity log), the playbook succeeded, and the comment and actions appear.
