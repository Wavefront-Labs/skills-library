---
id: creative-arts.design-for-form-and-experience.ux-design.writing-an-event-tracking-plan
name: writing-an-event-tracking-plan
category: creative-arts
field: design-for-form-and-experience
product: ux-design
tags: [tracking-plan, event-tracking, analytics-instrumentation, product-analytics, event-taxonomy, ux-research]
level: practitioner
status: draft
description: "Write an event tracking plan: naming convention, event and property definitions, identity rules, and QA so product analytics answers real questions."
sources:
  - "Segment - Tracking Plan and Naming Conventions (segment.com/academy/collecting-data/naming-conventions-for-clean-data)"
  - "Amplitude Data - Taxonomy Playbook (amplitude.com/docs/data)"
  - "Google Analytics 4 - Events and recommended event names (support.google.com/analytics)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Event tracking plan

**Goal:** a shared, versioned spec of what is tracked, so data is consistent and trustworthy.

## Start from questions
List 5-10 business and UX questions ("Where do new users stall?"). Derive only the events needed to answer them.

## Spec table (one row per event)
| Event | Trigger | Properties | Owner | Platforms | Status |
Example: `checkout_started`, fires when the checkout page first renders, properties `cart_value` (number, currency in a separate `currency` string), `item_count` (int), `source` (enum).

## Conventions
- **Naming:** pick Object-Action in past tense, snake_case (`order_completed`, `search_submitted`) and never mix styles. Do not encode values in event names (`clicked_blue_button`); use properties.
- **Properties:** typed, with allowed values and units. Prefer few events with rich properties over hundreds of events.
- **Identity:** define anonymous ID, user ID, when `identify` merges them, and what happens on logout. Never send emails or other PII as properties unless the privacy review allows it.
- **Consent:** document which events fire without consent and which wait for it.

## QA and governance
- Verify in a debug view (GA4 DebugView, Segment debugger, Amplitude ingestion debugger) on every platform before release; check types and counts against expected.
- Store the plan in version control or a tool with change history; an event not in the plan should fail review or be flagged by schema validation.
- Retire unused events on a schedule.

## Verify
- [ ] Every event traces to a question and has an owner.
- [ ] Naming, typing and identity rules are written down.
- [ ] Events verified on each platform before shipping.
