---
id: computing-software.cybersecurity-defensive.splunk.es-mission-control-analyst-queue
name: es-mission-control-analyst-queue
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, enterprise-security, mission-control, findings, analyst-queue, response-plans, splunk-soar, es8]
level: practitioner
status: draft
description: "Work the Splunk Enterprise Security 8 Mission Control analyst queue: findings vs investigations, queue filters, SLAs, response plans, and SOAR actions from the queue."
sources: ["https://docs.splunk.com/Documentation/ES/8.0.0/User/AnalystQueue", "https://docs.splunk.com/Documentation/ES/8.0.0/User/ResponsePlans", "https://docs.splunk.com/Documentation/ES/8.0.0/RN/WhatsNew"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Mission Control analyst queue (ES 8)

ES 8 unifies ES, Mission Control and SOAR: notables become **findings** (from finding-based
detections) and grouped work becomes **investigations**, worked in one analyst queue.

## Object model
- **Finding**: output of an event-based detection (old notable).
- **Intermediate finding**: low-fidelity output that only contributes risk; not in the queue by default.
- **Finding group**: produced by a finding-based detection (e.g. risk threshold over 24 h).
- **Investigation**: created from a finding or group; owner, status, disposition, SLA, response plan.

## Queue setup
- Saved views per tier: filter by urgency, detection type, owner `unassigned`, MITRE tactic.
- Columns: urgency, SLA remaining, entity, risk score, detection name. Sort by SLA, not time.
- Configure statuses and dispositions under Configure > Incident management; keep dispositions
  aligned with your metrics taxonomy (true positive, benign true positive, false positive).

## Response plans
Templates of phases and tasks (Triage, Containment, Eradication) attached to investigations.
Tasks can carry searches and SOAR playbooks/actions; completion is timestamped, which gives
MTTA/MTTR without manual logging. Build one per incident category (phishing, malware, account
compromise) mirroring your runbooks.

## SOAR from the queue
With SOAR paired, analysts run playbooks or single actions (e.g. isolate host, disable user) on an
investigation; results attach to the investigation record. Restrict destructive actions with SOAR
role permissions and require approval prompts.

## Migration notes
- Existing correlation searches convert to event-based detections; notables' history stays in
  the `notable` index.
- RBA risk notables become finding-based detections; review thresholds after migration.

## Gotchas
- Findings and investigations live in different stores; dashboards built on `notable` need updating.
- Without pairing SOAR and ES on the same tenant/version, action buttons are hidden.

## Verify
Create a test finding, start an investigation, apply a response plan, complete one task with a
SOAR action, and confirm timestamps and results appear on the investigation.
