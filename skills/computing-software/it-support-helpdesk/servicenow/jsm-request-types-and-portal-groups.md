---
id: computing-software.it-support-helpdesk.servicenow.jsm-request-types-and-portal-groups
name: jsm-request-types-and-portal-groups
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, jira-service-management, jsm, jsm-request-types, portal-groups, work-categories, request-forms, help-center, atlassian, service-request, jsm-help-center]
level: practitioner
status: draft
description: "Design Jira Service Management request types and portal groups: work categories, issue-type mapping, form fields, hidden preset fields, and a short portal."
sources:
  - "https://support.atlassian.com/jira-service-management-cloud/docs/what-are-request-types/"
  - "https://support.atlassian.com/jira-service-management-cloud/docs/organize-request-types-into-portal-groups/"
  - "https://support.atlassian.com/jira-service-management-cloud/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# jsm-request-types-and-portal-groups

A JSM **request type** is what the customer picks on the portal; under the hood every
request type maps to one Jira **issue type** (and so one workflow). Portal groups are the
headings that request types sit under on the help centre.

## Model
| Layer | What it controls | Who sees it |
|---|---|---|
| Work category (Service requests, Incidents, Problems, Changes, Post-incident reviews) | Default queues, reports, ITSM features | Agents |
| Issue type | Workflow, screens, field configuration | Agents/admins |
| Request type | Portal name, icon, description, which fields show and their customer-facing labels | Customers |
| Portal group | Grouping on the portal home | Customers |

One issue type can back many request types ("Get a laptop", "Get a monitor", "Get a
headset" all on *Service request with approvals*). That is the normal pattern: few
workflows, many customer-facing doors.

## Build a request type (Project settings > Request types)
1. Create, choose the **work category** and the backing **issue type**.
2. Name it in the user's words ("My laptop won't turn on", not "Hardware incident").
   Add a one-line description; it shows under the name in portal search.
3. **Request form** tab: add only fields the fulfiller needs. Rename fields for the portal
   (field "Component" shown as "Which system?"). Mark required only where the agent cannot
   act without it.
4. Use **hidden fields with preset values** to set component, labels or priority
   automatically, so routing does not depend on the customer.
5. **Issue view** tab: arrange what agents see (request participants, SLAs, linked alerts).
6. **Workflow statuses** tab: map internal statuses to customer-friendly names
   ("Waiting for support" can show as "We're on it").
7. Assign to one or more **portal groups**. A request type in no group is hidden from the
   portal but still usable by the email channel or by agents ("Raise a request").

## Portal design rules
- Fewer than about 8 groups and 8-10 request types per group; customers scan, they don't read.
- Group by the customer's intent (Get something / Something is broken / Ask a question /
  Access), not by your team structure.
- Keep a catch-all ("Get IT help") so nobody abandons the portal; review what lands in it
  monthly and create request types for the top repeats.
- Set the email channel's request type deliberately; all email requests land there.
- Use **Forms** for conditional sections instead of creating near-duplicate request types.

## Gotchas
- Changing the backing issue type of a request type does not move existing tickets.
- Email-created requests skip portal-only required fields, so the workflow must cope with
  them being empty.
- A central help centre shows every project the customer can access, so names must be
  distinct across projects.
- Deleting a request type leaves its tickets with no request type in reports; hide it
  (remove from groups) instead.

## Verify
Open the portal as a test customer account (not an agent), raise one of each new type,
confirm hidden fields set component/priority, the correct queue picks it up, and the
customer-facing status names read correctly.
