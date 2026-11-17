---
id: computing-software.cloud-infrastructure-engineering.ansible.notification-events-and-schedule-auditing
name: notification-events-and-schedule-auditing
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, schedules-notifications, notification-events, schedule-audit, notifications]
level: practitioner
status: docs-checked
description: "Attach notifications to the right events (started, success, error, approval) on organizations, projects and templates, and review schedules before cleanup."
sources: ["https://raw.githubusercontent.com/ansible/aap-docs/main/downstream/modules/platform/con-controller-enable-notifications.adoc", "https://raw.githubusercontent.com/ansible/awx/devel/awx_collection/plugins/modules/job_template.py", "https://raw.githubusercontent.com/ansible/awx/devel/awx_collection/plugins/modules/workflow_job_template.py", "https://raw.githubusercontent.com/ansible/awx/devel/awx_collection/plugins/modules/organization.py", "https://raw.githubusercontent.com/ansible/awx/devel/awx_collection/plugins/modules/schedule.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Notification events and schedule auditing

## Events
Notifications can be enabled on job start, job success and job failure (or a combination) from the
Notifications tab of job templates, workflow templates and projects. Workflow templates with approval
nodes also get approval-related events.

| Event | Typical use |
|---|---|
| started | long jobs, change-window visibility |
| success | release announcements, ticket closure |
| error (failure) | paging, chat alerts |
| approval (workflow) | tell approvers a node is waiting |

```yaml
- ansible.controller.job_template:
    name: Deploy app
    notification_templates_started: [chat-releases]
    notification_templates_success: [chat-releases]
    notification_templates_error: [pagerduty-oncall]
- ansible.controller.workflow_job_template:
    name: Release app
    notification_templates_approvals: [approvers-email]
```
The same `notification_templates_*` parameters exist on the organization, project and inventory source modules.

## Behaviours documented
- A start notification on a workflow template and on a job template inside it both fire.
- A start notification on a sliced job template fires once per slice.
- If a notification template is deleted while still attached to a job start event, the job still runs but reports an error message.

## Schedule audit
List schedules through the API or the Schedules page and review them. Look for:
- Disabled schedules nobody remembers (delete or document).
- Schedules on templates whose owners left.
- Overlapping schedules that hit the same hosts.
- Schedules whose prompted values (extra vars, limit) differ from the template defaults.
The `schedule` module has an `enabled` parameter: `ansible.controller.schedule: {name: X, unified_job_template: T, enabled: false}` disables without deleting. Export schedules to your config-as-code repository before deleting.

## Verify
- [ ] Every production template has an error notification, directly or through its organization.

## Checked

- Date: 2026-11-09. Sources: ansible/aap-docs main (enable and disable notifications), ansible/awx devel modules job_template, workflow_job_template, organization, schedule.
- Confirmed: events and resources that support notifications, the three documented behaviours, `notification_templates_started/success/error/approvals` parameters, schedule `enabled` parameter.
- Removed unconfirmed claims: per-level firing rules (user-guide inventory source notifications are unconfirmed upstream, only module parameters back them), organization notifications firing for every template in it, the `awx schedules list` jq pipeline and `awx schedules modify` command, duplicate-notification advice, custom message requirement for approvals, schedules deleted with their template.

Method: documentation and collection source read from cloned repositories; no commands were run against a controller.
