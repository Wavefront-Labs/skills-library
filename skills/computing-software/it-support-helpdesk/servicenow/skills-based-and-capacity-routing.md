---
id: computing-software.it-support-helpdesk.servicenow.skills-based-and-capacity-routing
name: skills-based-and-capacity-routing
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, queue-management, skills-based-routing, advanced-work-assignment, awa, agent-capacity, push-routing, omni-channel, agent-presence]
level: advanced
status: draft
description: "Push work to agents with ServiceNow Advanced Work Assignment: service channels, queues, skills and capacity, presence states, and when push beats agents cherry-picking from lists."
sources:
  - "https://www.servicenow.com/docs/"
  - "https://developer.servicenow.com/dev.do"
  - "https://www.thinkhdi.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# skills-based-and-capacity-routing

Goal: each ticket/chat goes to an available agent who can handle it, in
priority order, instead of agents picking the easy ones from a list.

## Why push routing
List-based queues invite cherry-picking: hard or old tickets age while quick
wins get grabbed. Push routing (ServiceNow **Advanced Work Assignment**,
AWA; similar in Zendesk Omnichannel routing and JSM with plugins) offers the
next item to the next suitable agent.

## AWA building blocks
- **Service channel**: what's routed (Incident, Chat, Case) and how much
  capacity one item uses.
- **Queues**: conditions selecting work items (e.g. priority 1–3 incidents
  for Service Desk L1), with order/priority.
- **Assignment rules**: most capable/least loaded; route to agent vs group.
- **Skills**: attach skills to agents (e.g. "macOS", "French", "SAP") with
  levels; work items get required skills by condition; mandatory vs
  optional skills.
- **Capacity**: max items per channel per agent (e.g. 3 chats, 6
  incidents).
- **Presence**: agents set Available/Away/Offline in Agent Workspace inbox;
  only Available agents receive offers; offers time out to the next agent.

## Rollout
1. Start with one channel (chat or P1–P2 incidents) and one team.
2. Keep skills few and meaningful — 50 micro-skills makes nobody eligible.
3. Set reasonable offer timeouts (e.g. 30–60 s for chat), and decide whether
   rejected offers need a reason.
4. Monitor: wait time, offers rejected, items routed to backup queue.

## Agent etiquette
- Set presence honestly (Away during breaks/meetings) — otherwise offers
  time out and wait time grows.
- Don't hoard: decline only with reason; supervisors review rejections.

## Gotchas
- Work items not matching any queue never get routed — catch-all queue.
- Skill requirements derived from category depend on correct categorisation.
- Mixing pull lists and push for the same work confuses ownership.

## Verify
Oldest-ticket age and P2 wait time drop after rollout; distribution of
items per agent evens out; no items stuck unrouted.
