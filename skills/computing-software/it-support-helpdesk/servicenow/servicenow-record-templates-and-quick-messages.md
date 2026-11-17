---
id: computing-software.it-support-helpdesk.servicenow.servicenow-record-templates-and-quick-messages
name: servicenow-record-templates-and-quick-messages
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, servicenow-templates, record-templates, quick-messages, response-templates, sys-template, canned-responses]
level: practitioner
status: gated
description: "Use ServiceNow record templates (sys_template) to prefill incidents and quick messages / response templates for consistent replies, with scope, sharing and upkeep."
sources:
  - "https://www.servicenow.com/docs/bundle/xanadu-platform-user-interface/page/use/using-forms/concept/c_Templates.html"
  - "https://www.servicenow.com/docs/bundle/xanadu-it-service-management/page/product/service-operations-workspace/concept/response-templates.html"
  - "https://www.servicenow.com/docs/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# servicenow-record-templates-and-quick-messages

Two different things:
- **Record templates** (`sys_template`): prefill fields on a record (category, CI,
  assignment group, short description, work notes) for common ticket types.
- **Quick messages / response templates**: canned text inserted into comments or emails,
  with variables, in the workspace compose box.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Record templates
Create: open a form, fill fields, right-click header > Templates > Save as template, or
System Definition > Templates.
```text
Name:        Outlook - profile rebuild
Table:       incident
Template:    category=software^subcategory=email^assignment_group=<Service Desk>
             ^short_description=Outlook profile corrupt - rebuild^u_resolution_kb=KB0012345
Global/Group: Group = Service Desk
```
- Apply from the form's template bar or the workspace "Apply template" action.
- Templates can create **child records** (next related template) for multi-task requests.
- Share with a group, not global, so each team's list stays short.

## Quick messages and response templates
Workspace compose box > template icon; admin in the response templates module.
```text
Hi ${caller_id.first_name},
I've reset your MFA registration. Next time you sign in you'll be asked to set up the
Authenticator app again. Your ticket is ${number}.
```
`${field}` variables resolve against the record; dot-walk works for reference fields.

## Rules
- One template per frequent ticket type identified from top-category reports.
- Never store passwords, phone numbers of individuals or expiring links in templates.
- Templates set values but do not trigger client-side onChange logic the way typing does;
  test assignment and SLA results after applying.
- Owner per template; review quarterly with the KB owners so text matches the article.

## Gotchas
- Applying a template overwrites fields that already hold values.
- A template referencing a retired group or CI sys_id fails quietly (field left empty).
- Templates are table-specific; an incident template cannot be applied to a request item.

## Verify
Apply each template to a new test record, confirm every field and the assignment
routing, insert a response template and check variables render with real values.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
