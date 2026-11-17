---
id: computing-software.it-support-helpdesk.servicenow.zendesk-ticket-fields-and-forms
name: zendesk-ticket-fields-and-forms
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, zendesk, zendesk-ticket-forms, ticket-fields, conditional-fields, custom-fields, ticket-form-design]
level: practitioner
status: draft
description: "Design Zendesk ticket fields and forms: field types, agent vs end-user visibility, conditional fields, required-on-solve, and keeping field sprawl under control."
sources:
  - "https://support.zendesk.com/hc/en-us/articles/4408883152794-Adding-custom-fields-to-your-tickets-and-support-request-form"
  - "https://support.zendesk.com/hc/en-us/articles/4408846520858-Creating-multiple-ticket-forms-to-support-different-request-types"
  - "https://support.zendesk.com/hc/en-us/articles/4408834848154-Creating-conditional-ticket-fields"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# zendesk-ticket-fields-and-forms

Fields drive triggers, views, SLAs and reports. Forms decide which fields appear for a
request type. Bad field design means agents pick "Other" and reports are useless.

## Fields (Admin Center > Objects and rules > Tickets > Fields)
- Types: drop-down, multi-select, text, multi-line, checkbox, date, numeric, decimal,
  regex, lookup relationship (to users, orgs, tickets, custom objects).
- Drop-down **tag values** (e.g. `category_hardware_laptop`) are what triggers and views
  test; choose a stable naming scheme before go-live.
- Nested drop-downs with `::` in values (Hardware::Laptop::Battery) give a tree without
  extra fields.
- Permissions: "Editable for end users" and "Visible" control the Help Center form;
  agent-only fields stay hidden.
- "Required to solve" for agents: category/resolution code. Don't make many fields
  required to submit; it slows capture.

## Forms (Admin Center > Objects and rules > Tickets > Forms)
- One form per request family: Incident/fault, Access request, Hardware request, HR-IT.
  Forms available on Enterprise/Professional per plan.
- End-user form selector in Help Center; agent can switch form on the ticket.
- **Conditional fields** (form > Conditions): show "Which printer?" only when Category =
  Printer; separate conditions for agents and end users; conditions can make a field
  required when shown.

## Design rules
- Start from reporting questions: what do you need to count? Fields that never appear in
  a report or rule are clutter.
- Keep drop-downs under about 30 values per level; review "Other" usage monthly and add
  the real values.
- Use ticket type (question/incident/problem/task) and priority system fields before
  inventing custom ones.

## Gotchas
- Renaming a drop-down value's tag breaks triggers and views silently; change titles,
  not tags.
- Deactivating a field hides history in reports; prefer removing from forms.
- Field values set by API/triggers bypass form conditions.

## Verify
Submit through Help Center with each form; conditional fields appear correctly, agents
can't solve without required fields, and views/triggers using the tags still fire.
