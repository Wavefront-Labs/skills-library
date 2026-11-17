---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.cost-onboarding
name: cost-onboarding
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-education, cost-onboarding, engineer-onboarding, cost-awareness]
level: practitioner
status: draft
description: "Onboard new engineers to cost: a 30-minute module, where to see their team's spend, tagging and policies, tools like Infracost, and a first cost task."
sources: ["https://www.finops.org/framework/capabilities/finops-education-enablement/", "https://www.finops.org/framework/personas/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cost onboarding for new engineers

New engineers copy what they see. Teach cost in week one, alongside security and on-call.

## Onboarding content (30-45 minutes, self-paced plus one live session)
1. **Why it matters here**: cloud spend size, the company's unit metric (cost per customer etc.),
   and one real story of a costly mistake and how it was caught.
2. **Your team's spend**: where the dashboard is, how to filter to your team, amortised vs billed
   cost in one sentence each.
3. **Rules**: mandatory tags and allowed values, non-prod schedules, allowed regions/SKUs, how to
   request an exception.
4. **Tools in the workflow**: cost estimate on pull requests (Infracost), budget alerts in the team
   channel, where recommendations show up.
5. **Pricing basics for your stack**: the 5 most expensive services your team uses, what drives
   their cost (requests, GB-month, data transfer, provisioned capacity).
6. **Who to ask**: team champion, #finops channel, office hours.

## First cost task (week 2-4)
Pick one: review the team's top 5 resources by cost and explain them; fix untagged resources; act
on one rightsizing recommendation. Pair with the champion.

## Steps
1. Add the module to the standard engineering onboarding checklist (owned by engineering
   enablement, content owned by FinOps).
2. Keep examples current (refresh quarterly); stale screenshots lose trust.
3. Measure: completion rate, quiz score, tag compliance of resources created by new joiners.

## Gotchas
- A slide deck on FinOps theory; show their real dashboard instead.
- Fear messaging makes engineers avoid experimenting; emphasise visibility and trade-offs.

## Verify
- [ ] Module in the onboarding checklist with >90% completion.
- [ ] New joiners can find their team's cost within one minute.
