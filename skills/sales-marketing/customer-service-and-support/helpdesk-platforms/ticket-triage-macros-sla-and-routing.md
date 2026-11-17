---
id: sales-marketing.customer-service-and-support.helpdesk-platforms.ticket-triage-macros-sla-and-routing
name: ticket-triage-macros-sla-and-routing
category: sales-marketing
field: customer-service-and-support
product: helpdesk-platforms
tags: [helpdesk-platforms, helpdesk, help-desk, zendesk, freshdesk, intercom, gorgias, ticketing, ticket-triage, macros, canned-responses, triggers, automations, sla-policies, routing, skills-based-routing, round-robin, omnichannel-routing, views, tags, ticket-fields, knowledge-base, help-centre, deflection, self-service, support-reporting, shopify-support]
level: practitioner
status: draft
description: "Configure and work a support helpdesk (Zendesk, Freshdesk, Intercom, Gorgias): ticket fields and tags, triage views, macros, SLA policies, routing rules, knowledge-base deflection and reporting."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Helpdesk platforms: triage, macros, SLAs and routing

**Goal:** every customer request lands in the right queue, gets the right priority,
is answered consistently and on time, and simple questions are answered by the help
centre before they become tickets.

Feature names differ (Zendesk "triggers/automations/macros", Freshdesk "dispatch'r/
observer/canned responses", Intercom "workflows", Gorgias "rules/macros") and change
with releases. The concepts below map across all four; check each vendor's docs for
exact menus and plan-tier availability.

## 1. Data model first
- **Ticket fields** (structured): contact reason, product, order number, priority,
  channel. Keep contact-reason lists short (15–25 options) and mutually exclusive.
- **Tags** for automation hooks and ad-hoc analysis; don't use tags where a field
  belongs (fields report cleanly).
- **Groups/teams** (tier 1, billing, technical, VIP) and **agent skills** (languages, products).
Set this before automations — every rule depends on it.

## 2. Triage views
Create shared views (queues) agents work from, e.g.:
- Unassigned, sorted by SLA due time (oldest breach risk first).
- My open tickets; Pending customer reply > 3 days; On-hold (waiting on internal team).
- Priority: VIP or urgent keywords ("chargeback", "legal", "safety").
Agents should work the top of a sorted view, not cherry-pick.

## 3. Routing rules
- **Auto-classify** on creation: channel, keywords, form selection, customer
  attributes (plan, VIP, language) → set group, priority, tags.
- Assignment: round-robin or load-based (capacity-aware) for chat/messaging; skills-based
  for languages or specialist products.
- Escalation rules: e.g. reassign to tier 2 if tagged "technical" and unresolved after 24 h.
- Test each rule with sample tickets; order matters — rules generally run top to bottom
  and one rule's action can trigger another.

## 4. Macros (canned responses + actions)
A macro should both reply and update the ticket: insert templated text with
placeholders (customer first name, order number), set fields/tags, change status.
Rules: one macro per common scenario; owner and review date; personalise before
sending; retire unused macros quarterly (check usage stats).

## 5. SLA policies
Define targets by priority and channel, e.g. first reply: urgent 1 h, high 4 h,
normal 24 h; next reply and resolution targets too (business hours vs calendar hours —
set the business-hours schedule and holidays). Put "SLA due" in every view and alert
leads on imminent breaches. Report SLA achievement weekly.

## 6. Knowledge base and deflection
- Write help articles for your top 20 contact reasons first; each with a clear title in
  customer language, steps, screenshots.
- Surface them: search on the contact form, article suggestions in the web widget/bot,
  links in macros.
- Track **deflection** (searches/article views not followed by a ticket) and failed
  searches (no results → write that article).

## 7. Reporting essentials
Ticket volume by contact reason and channel; first reply and resolution time; SLA
achievement; one-touch/first-contact resolution; CSAT by group/agent; backlog age.
Volume by reason is the input to fixing products and writing articles.

## Gotchas
- Too many automations interact unpredictably; document each rule's purpose.
- Merging duplicate tickets late splits customer history; teach agents to merge early.
- Integrations (Shopify for Gorgias, CRM for others) need correct customer matching by email.
- Changing field values breaks historical reports; add new values, retire old ones.

## Verify
- [ ] Contact-reason field and groups defined before automations.
- [ ] Sorted triage views by SLA due time exist and are used.
- [ ] Routing rules tested with sample tickets for each channel.
- [ ] SLA policies with business hours configured; breaches alerted.
- [ ] Top 20 contact reasons covered by help articles; failed searches reviewed monthly.
