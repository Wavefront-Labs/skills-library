---
id: computing-software.it-support-helpdesk.servicenow.jsm-approvals-in-workflows
name: jsm-approvals-in-workflows
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, jira-service-management, jsm, jsm-approvals, approval-step, workflow, service-request, approver-field]
level: practitioner
status: draft
description: "Configure Jira Service Management approvals: approval steps on workflow statuses, approver user/group fields, number of approvals, automation-set approvers and stuck approvals."
sources:
  - "https://support.atlassian.com/jira-service-management-cloud/docs/set-up-approvals/"
  - "https://support.atlassian.com/jira-service-management-cloud/docs/approve-or-decline-requests/"
  - "https://support.atlassian.com/cloud-automation/docs/jira-automation-triggers/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# jsm-approvals-in-workflows

JSM approvals live on a workflow *status*: while the request sits in that status, the
named approvers see Approve/Decline in the portal, email and the agent view.

## Setup (company-managed project)
1. Project settings > Workflows > edit the request type's workflow.
2. Select the status that should wait (e.g. "Waiting for approval") > **Add approval**.
3. Choose the approver field: a user picker (multiple users) such as the built-in
   **Approvers** field, or a group picker (Approver groups).
4. Number of approvals needed: 1, all, or N; for group fields, at least N members of
   the group.
5. Map transitions: **Approve** -> next status (e.g. In progress), **Decline** -> Declined.
6. Publish the workflow. Team-managed projects: Project settings > Request types > the
   type > Workflow > add approval on a status with the same options.

## Setting approvers
- Customer chooses on the portal form (add the Approvers field to the request type).
- Automatically: Automation rule "When: Work item created" (request type = X) > Edit field
  Approvers = `{{reporter.manager}}` style lookups require the manager attribute from
  your directory or Assets; common pattern: Lookup the user's Assets object to get the
  manager, then set Approvers.
- Group approvals for change requests: Approver groups = CAB group.

## Approver experience
Approvers don't need an agent licence; customers (portal users) can approve. They get an
email with Approve/Decline links and see pending items under Approvals in the portal.

## Troubleshooting
- Stuck in "Waiting for approval" with empty approver field: the request had no approver
  set (automation failed). Add approvers manually; the approval re-evaluates.
- Approver left the company: edit the field to a new approver; or decline and reopen.
- Agents can't approve on someone's behalf by default (audit); record verbal approvals
  only if policy allows, as an internal comment.
- Decline transitions with required fields (resolution) fail silently in older configs;
  check the transition screen.

## Gotchas
- Approval steps are per status; two sequential approvals (manager then finance) need two
  statuses, each with its own approval.
- Approvers must have "Browse projects"/portal access to the service project.

## Verify
Raise a test request; approver receives the email, approving moves the status, declining
lands in Declined with a comment visible to the requester.
