---
id: computing-software.cybersecurity-defensive.splunk.elastic-security-cases-and-connectors
name: elastic-security-cases-and-connectors
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [elastic-security, elastic-cases, kibana-connectors, servicenow, jira, case-management, incident-management]
level: practitioner
status: docs-checked
description: "Use Elastic Security cases: create from alerts or Timeline, custom fields and templates, and push to ServiceNow, Jira or webhook connectors with field mapping."
sources: ["https://www.elastic.co/guide/en/security/current/cases-overview.html", "https://www.elastic.co/guide/en/kibana/current/action-types.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Elastic Security cases and connectors

## Cases
- Create from Alerts (bulk "Add to new case"), from Timeline ("Attach to case"), or Cases page.
- Case activity is the audit trail: comments, alerts attached, status changes.

## Connectors
Stack Management > Connectors (or Cases > Settings > External incident management system):
- Cases integrate with ServiceNow, Jira and IBM Resilient; Swimlane and TheHive connectors are also available.
- Configure the connector, then push the case to the external system from the case; check the cases page for current behaviour.

## Alert status
With Sync alert status on, closing a case opens a prompt to choose how the attached detection alerts are closed (without a reason, or with a close reason).

## Verify
Create a test case from an alert, push it to the ticketing sandbox, add a comment and push again;
ticket shows both; closing the case with sync on prompts for the alert close reason.

## Checked

Date: 2026-10-28

- Confirmed (cases overview, Kibana connectors list): cases integrate with Jira, ServiceNow and IBM Resilient; Swimlane and TheHive connectors exist; with Sync alert status on, closing a case prompts for a close reason for attached alerts.
- Removed (not found): custom field/template version gate, Markdown embedding, closure setting, ServiceNow/Jira field-level setup, push labels and one-way sync claim, rule action and API sample, gotchas. Dropped dead source cases-ui-integrations.html (404).
Method: documentation only; no commands were run.
