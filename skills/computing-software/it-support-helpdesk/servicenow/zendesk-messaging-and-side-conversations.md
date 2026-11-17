---
id: computing-software.it-support-helpdesk.servicenow.zendesk-messaging-and-side-conversations
name: zendesk-messaging-and-side-conversations
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, zendesk-messaging, zendesk-side-conversations, zendesk, web-widget, collaboration]
level: practitioner
status: draft
description: "Set up Zendesk messaging and the Web Widget for live chat and bots, and use side conversations to work with other teams and vendors without leaving the ticket."
sources:
  - "https://support.zendesk.com/hc/en-us/articles/4408836323738-About-messaging"
  - "https://support.zendesk.com/hc/en-us/articles/4408833930906-Setting-up-the-Web-Widget-for-messaging"
  - "https://support.zendesk.com/hc/en-us/articles/4408843711898-Using-side-conversations-in-tickets"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# zendesk-messaging-and-side-conversations

## Messaging and the Web Widget
- Admin Center > Channels > Messaging: create a Web Widget (or mobile SDK channel), set
  brand, colours, and where it shows (embed snippet on the portal/help center).
- Messaging is asynchronous: conversations persist, customers can leave and come back.
  Agents see them as tickets in the workspace with channel = messaging.
- Configure **operating hours** and the out-of-hours response (set expectations, offer
  help center articles).
- **Bots**: a flow builder answer bot greets, suggests articles, collects details
  (name, device, issue type) and hands off to an agent; keep the handoff obvious
  ("Talk to a person").
- Routing: omnichannel routing assigns messaging conversations by capacity and skills;
  set messaging capacity per agent lower than email (2-3 concurrent).

## Side conversations
- From a ticket, open a **side conversation** (email, Slack, Microsoft Teams, or child
  ticket) to ask another team or vendor something. The requester doesn't see it.
- Child tickets create a separate ticket for another group with its own SLA, linked back.
- The side conversation thread stays on the ticket; status shows open/closed.
- Use for: asking networking whether a port is blocked, vendor RMA emails, approvals
  from a manager.

## Pitfalls
- Widget on every page with no staffing, leading to unanswered chats.
- Side conversations left open; close them when answered so the ticket status is clear.
- Pasting customer PII into a Slack side conversation that goes to a wide channel.

## Verify
A test chat from the widget reaches an agent within target, bot handoff passes collected
details, and side conversations show on the ticket with replies captured.
