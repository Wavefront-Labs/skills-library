---
id: computing-software.it-support-helpdesk.servicenow.live-agent-chat-handoff-and-staffing
name: live-agent-chat-handoff-and-staffing
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, live-chat, live-agent, virtual-agent-handoff, chat-queue, awa, chat-concurrency]
level: practitioner
status: gated
description: "Run live agent chat in ServiceNow: Virtual Agent handoff, chat queues and AWA capacity, concurrency limits, business-hours fallback, and turning chats into tickets."
sources:
  - "https://www.servicenow.com/docs/bundle/zurich-servicenow-platform/page/administer/virtual-agent/concept/live-agent-chat.html"
  - "https://www.servicenow.com/docs/bundle/zurich-servicenow-platform/page/administer/advanced-work-assignment/concept/awa-overview.html"
  - "https://www.servicenow.com/docs/bundle/zurich-servicenow-platform/page/administer/virtual-agent/task/setup-live-agent-transfer.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# live-agent-chat-handoff-and-staffing

Chat is cheaper than phone only if agents run 2-3 chats at once and the bot passes
context. Done badly it is a slower phone line.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Handoff from Virtual Agent
- In Virtual Agent Designer, use the **Live agent transfer** (or "Transfer to live agent")
  topic/utility. Pass context: user, topic, what the bot already tried, any device chosen.
- Queue routing: chat queues in Advanced Work Assignment (`awa_queue`) with conditions on
  `interaction` fields (language, topic, VIP flag). Agents need the right AWA channel
  (Chat) and to be Available in their inbox.
- Outside business hours: the queue's schedule makes the transfer topic offer "Create a
  ticket" or callback instead of leaving the user waiting.

## Capacity and staffing
- AWA channel capacity per agent: start at 2 concurrent chats, 3 for experienced agents
  on simple topics. Phone + chat at once is a poor experience; use separate states.
- Watch queue wait time (target under 60 s) and abandonment; staff with the same Erlang
  logic as phones but adjust for concurrency.
- Wrap-up: allow a short after-chat work time before the next one is pushed.

## In the chat
- Greet with name within 30 s of accept; read the bot transcript, don't re-ask.
- Use quick actions/shortcuts (`/`) and response templates for repeats.
- Set expectations if you need to investigate ("give me 3 minutes to check your
  account"); come back before then.
- Before ending: summarise outcome and next step.

## Records
- Each chat is an `interaction` record. Create or link an incident/request from the
  interaction (Create incident related link); the transcript copies into the ticket.
- Resolve trivial chats on the interaction only if your reporting counts them; many desks
  require a ticket for anything needing action.

## Gotchas
- Agents set to Available on phone and chat at once get pushed both; use presence states.
- Long silent chats: configure inactivity timeouts and a warning message, otherwise chats
  occupy capacity forever.
- Sensitive data typed into chat lands in the transcript; mask with sensitive data
  handling rules (e.g. card numbers).

## Verify
Test transfer from the bot in and out of hours; transcript and context appear to the
agent; a ticket created from the chat contains the transcript; AWA reports show waits.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
