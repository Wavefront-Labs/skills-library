---
id: computing-software.it-support-helpdesk.servicenow.jsm-automation-rules
name: jsm-automation-rules
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, jira-service-management, jsm, jsm-automation, automation-for-jira, smart-values, auto-assign, auto-close, atlassian]
level: practitioner
status: draft
description: "Write Jira Service Management automation rules: triggers, conditions, actions, smart values, auto-triage and auto-close, rule actor and loop pitfalls, audit log."
sources:
  - "https://support.atlassian.com/cloud-automation/docs/jira-automation-triggers/"
  - "https://support.atlassian.com/cloud-automation/docs/what-are-smart-values/"
  - "https://support.atlassian.com/cloud-automation/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# jsm-automation-rules

Rules are **trigger -> conditions -> actions** (Project settings > Automation). Build the
handful of rules that remove manual toil; resist building a hidden workflow nobody can debug.

## Rules worth having
| Rule | Trigger | Condition | Action |
|---|---|---|---|
| Auto-triage | Work item created | Request type = X, or summary contains "VPN" | Edit Component / Team; assign (round-robin or balanced) |
| Reopen on reply | Comment added | Public comment by reporter, status = Resolved | Transition to In progress; notify assignee |
| Chase | Scheduled daily, JQL `status = "Waiting for customer" AND updated <= -3d` | none | Public reminder comment |
| Auto-close | Scheduled, JQL `status = "Waiting for customer" AND updated <= -7d` | none | Transition to Resolved, resolution "No response" |
| Major incident alert | Work item created | priority = Highest | Send Slack/Teams message to on-call channel |
| Approval nudge | Scheduled | status = "Waiting for approval" AND created <= -2d | Email the approvers |

## Smart values you will use
```text
{{issue.key}}  {{issue.summary}}  {{issue.reporter.displayName}}
{{issue.status.name}}  {{issue.priority.name}}
{{comment.body}}  {{comment.internal}}         on comment triggers
{{now.plusBusinessDays(2)}}                    date maths
{{#issue.labels}}{{.}} {{/}}                   iterate a list
```
Test smart values with a "Log action" step before using them in real actions.

## Building safely
1. Scope rules to a single project unless they really are global.
2. Leave "Allow rule trigger" (rules triggering other rules) off unless you deliberately
   chain; it is the usual cause of loops.
3. Scheduled rules: always include `resolution = EMPTY` or a status clause in the JQL so
   they never sweep closed tickets.
4. Add "Re-fetch work item data" after an edit when a later action reads the changed field.
5. Name rules "WHEN x IF y THEN z" so the rule list explains itself.

## Gotchas
- Rules run as the rule actor ("Automation for Jira" by default); it needs permission for
  the transitions and fields you touch.
- Cloud plans cap monthly rule executions; multi-project and global rules count against
  the limit. Watch Usage in automation settings.
- "Comment on work item" can make a note public; set comment visibility explicitly.
- A failed transition (usually a required field on the transition screen) shows only in the
  rule **Audit log**, with the reason.

## Verify
Trigger each rule on a test ticket, then read the rule's audit log: SUCCESS, the expected
actions, and no "no actions performed" entries for tickets that should have matched.
