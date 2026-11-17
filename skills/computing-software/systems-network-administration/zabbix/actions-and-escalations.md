---
id: computing-software.systems-network-administration.zabbix.actions-and-escalations
name: actions-and-escalations
category: computing-software
field: systems-network-administration
product: zabbix
tags: [actions, escalations, operations, steps, remote-commands, action, escalation, operation]
level: practitioner
status: docs-checked
description: "Configure action operations with escalation steps, step duration and behaviour during maintenance or cancellation."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/notifications/action
  - https://www.zabbix.com/documentation/current/en/manual/config/notifications/action/escalations
  - https://www.zabbix.com/documentation/current/en/manual/config/notifications/action/operation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Actions combine conditions and operations. Escalations let operations run at later steps: notify immediately, repeat until resolved, delay a notification, escalate to a higher user group, or run remote commands after a long unresolved problem.

Rules:
- Step 1 is immediate. Each step has a duration; the minimum is 60 seconds, set as a default plus optional custom values per operation. Steps are unlimited and several operations can share a step.
- Escalation is supported for problem operations only, not for recovery operations.
- Recipients need at least read permission to the host to be notified.

Behaviour table highlights from the docs:
- Host enters maintenance after the first notification: the Pause operations for suppressed problems setting decides whether remaining steps are delayed or not. Maintenance never cancels operations.
- A Time period condition ending after the first message does not stop later steps. It only affects when actions start.
- Problem starting in maintenance and persisting after it: steps run from maintenance end or immediately, per the same setting.
- Overlapping escalations from every-evaluation events: a new escalation supersedes the previous one, but at least one step of the previous still runs.
- If the action, trigger, host or item is disabled mid-escalation, the message in progress is sent plus one more beginning with NOTE: Escalation canceled and the reason, sent to all earlier recipients.

Pause operations for symptom problems affects only problem escalations and is available for trigger actions.

## Checked

2026-11-03. Confirmed against the Zabbix manual pages (config/notifications/action; config/notifications/action/escalations; config/notifications/action/operation): the figures, defaults, ranges, parameter and key names and behaviours stated above. Removed: nothing needed removing.

Method: documentation only; no commands were run.
