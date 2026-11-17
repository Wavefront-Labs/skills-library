---
id: computing-software.systems-network-administration.zabbix.recovery-and-update-operations
name: recovery-and-update-operations
category: computing-software
field: systems-network-administration
product: zabbix
tags: [recovery-operations, notify-all-involved, update-operations, acknowledgement, helpdesk-ticket, recovery, update, operation]
level: practitioner
status: docs-checked
description: "Send recovery messages, notify everyone involved, and run remote commands when problems resolve or are updated."
sources:
  - https://www.zabbix.com/documentation/current/en/manual/config/notifications/action/recovery_operations
  - https://www.zabbix.com/documentation/current/en/manual/config/notifications/action/update_operations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Recovery operations tell people when a problem is resolved. Several can be added, but escalation is not supported: all run in a single step simultaneously.

Operation types for recovery events:
- Send message to chosen user groups or users, who need at least read permission on the host.
- Notify all involved: a recovery message to every user who was notified of the problem.
- A remote command, available if defined in global scripts with scope Action operation.

If the same recipient appears in several operations without a custom message, duplicate notifications are not sent.

Use cases from the docs: notify everyone previously notified; send a message and run a remote command together; open a ticket in an external helpdesk through an external script on the problem operation, then close it with the same script and different parameters on recovery. Use the {EVENT.ID} macro to reference the original problem.

Update operations are available for trigger actions when problems are updated by other users (commented upon, acknowledged, severity changed, closed manually) and for service actions when a service severity changes but the service has not recovered. Users do not receive notifications about their own updates. They also run in one step with no escalation, and offer the same parameters as recovery operations.

Both lists sit on the Operations tab of the action form, in their own Recovery operations and Update operations sections, each with its own Add button.

## Checked

2026-11-09. Confirmed against the Recovery operations and Update operations pages: single step with no escalation, three operation types, read permission requirement, duplicate suppression, use cases and {EVENT.ID}, update triggers and own-update rule, Operations tab layout. Recovery page read through the send message parameters; the remote command parameter table was not read.
Method: documentation only; no commands were run.
