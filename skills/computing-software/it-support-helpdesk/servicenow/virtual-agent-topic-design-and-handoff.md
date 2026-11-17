---
id: computing-software.it-support-helpdesk.servicenow.virtual-agent-topic-design-and-handoff
name: virtual-agent-topic-design-and-handoff
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, self-service-portal, self-service, virtual-agent, chatbot, live-agent-handoff, conversational-design, nlu]
level: practitioner
status: draft
description: "Build virtual agent topics that resolve or hand off cleanly: choosing intents, NLU utterances, slot filling, fallback, live-agent transfer with context, tuning from transcripts."
sources:
  - "https://www.servicenow.com/docs/"
  - "https://learn.microsoft.com/en-us/microsoft-copilot-studio/"
  - "https://www.thinkhdi.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# virtual-agent-topic-design-and-handoff
Goal: a chatbot that fully resolves a handful of high-volume requests and
passes everything else to a human with the context already captured.

## Pick topics from ticket data
Start with 5-10 high-volume, rule-based tasks: password reset/unlock (via
SSPR), check ticket status, MFA re-registration guidance, request common
software, report outage ("is X down?"), find a knowledge article. Avoid
complex troubleshooting early.

## Designing a topic (ServiceNow Virtual Agent Designer or Copilot Studio)
- **Intent**: 15-30 real utterances taken from ticket short descriptions
  and chat logs, varied wording and typos; train NLU (or LLM topic
  discovery) and test with held-back phrases.
- **Slots**: collect the minimum (which application, which device) with
  choice lists; validate against the CMDB/catalog.
- **Action**: call the fulfilment (Flow / Power Automate / API) and
  confirm the result in plain words.
- **Exit**: "Did that fix it?" Yes → close with resolution; No → offer
  live agent or open ticket.

## Handoff that does not annoy users
- Transfer to live agent with the transcript and collected slots, so the
  agent does not ask again. In ServiceNow, use the Live Agent transfer
  node; queue by topic.
- Out of hours: create the incident with transcript attached and tell the
  user the reference number and when someone will respond.
- Always offer an escape ("talk to a person") within 2 turns of failure.

## Tuning
- Weekly: review unrecognised utterances and fallback hits; add to intents
  or create new topics.
- Track per topic: containment (resolved without agent), handoff rate,
  CSAT, and abandonment mid-conversation.

## Gotchas
- Bots that loop "I didn't understand" destroy trust; cap retries at 2.
- Password reset by bot must use the same identity proofing as SSPR;
  never reset based on chat-supplied details alone.
- Generative answers from knowledge need citations and an answer
  confidence threshold, or they invent steps.

## Verify
For each live topic you can show containment and handoff rates, and a
handed-off chat arrives at the agent with the slots filled.
