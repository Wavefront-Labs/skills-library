---
id: computing-software.it-support-helpdesk.servicenow.zendesk-omnichannel-routing-and-skills
name: zendesk-omnichannel-routing-and-skills
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, zendesk, zendesk-omnichannel-routing, skills-based-routing, agent-capacity, unified-agent-status, routing-queues]
level: practitioner
status: draft
description: "Set up Zendesk omnichannel routing: routing queues, skills, capacity rules per channel, unified agent status, reassignment of unanswered work, and diagnosing tickets not routed."
sources:
  - "https://support.zendesk.com/hc/en-us/articles/4409149119514-About-omnichannel-routing"
  - "https://support.zendesk.com/hc/en-us/articles/4408838892698-Using-skills-based-routing"
  - "https://support.zendesk.com/hc/en-us/articles/6712268543258-Managing-queues-for-omnichannel-routing"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# zendesk-omnichannel-routing-and-skills

Omnichannel routing pushes email/web tickets, messaging conversations and calls to agents
based on status, capacity, priority and skills, replacing "agents cherry-pick from views".

## Building blocks (Admin Center > Objects and rules > Omnichannel routing)
- **Routing configuration**: turn on routing for email/web forms; set the trigger tag
  (tickets tagged e.g. `route` are routed) or route all.
- **Queues** (custom queues, Professional+): conditions (form, priority, language,
  organization) and primary/secondary groups. Order matters; first matching queue wins.
- **Skills** (Admin Center > Objects and rules > Skills): skill types (Language, Product,
  Tier) and skills; assign to agents; attach to tickets by routing rules (conditions ->
  skills) or triggers. Option to drop skills after a timeout so tickets don't wait forever
  for one specialist.
- **Capacity rules**: per channel concurrency, e.g. email 5, messaging 3, calls 1;
  different rules for different agent groups.
- **Unified agent status**: Online, Away, Transfers only, Offline (plus custom statuses);
  only Online agents receive work.

## Behaviour to configure
- Reassign unanswered tickets back to the queue after N minutes when agents go away.
- Priority ordering: urgent before high, then oldest first; SLA-based ordering where
  available.
- Focus mode / auto-accept for messaging so agents don't ignore offers.

## Diagnosing "ticket not routed"
1. Ticket lacks the routing tag or doesn't match any queue condition.
2. Required skills: no Online agent has all of them (check the ticket's skills in the
   context panel); enable skill timeout.
3. All eligible agents at capacity (check the queue/agents in Live/routing dashboards).
4. Ticket already assigned (routing only picks unassigned tickets in eligible groups).
5. Group not included in any queue.

## Gotchas
- Mixing manual view-based work with routing confuses capacity counts; agents
  self-assigning bypasses routing logic.
- Too many skills fragment the pool; 2-3 skill types is usually enough.
- Capacity counts *open* assigned tickets, including pending ones, unless configured;
  check your account's capacity setting.

## Verify
Create test tickets with different languages/products; each routes to an Online agent
with the matching skills within the expected time, and reassignment works when the agent
goes Away.
