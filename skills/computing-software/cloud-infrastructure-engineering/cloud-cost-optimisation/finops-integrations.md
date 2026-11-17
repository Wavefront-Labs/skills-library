---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.finops-integrations
name: finops-integrations
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-tools, finops-integrations, chatops, jira, slack]
level: practitioner
status: draft
description: "Integrate FinOps tooling with ticketing and chat: routing anomalies and recommendations to owners, Slack/Teams digests, Jira automation and closing the loop."
sources: ["https://www.finops.org/framework/capabilities/finops-tools-services/", "https://docs.aws.amazon.com/cost-management/latest/userguide/manage-ad.html", "https://api.slack.com/messaging/webhooks"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Integrating FinOps tools with ticketing and chat

Engineers live in Jira/ServiceNow and Slack/Teams, not the FinOps portal. Push cost signals there,
addressed to the owning team, with enough context to act.

## Patterns
1. **Anomaly alerts to chat**: AWS Cost Anomaly Detection -> SNS -> AWS Chatbot or a webhook into
   the team channel; Azure cost alerts -> action group -> Logic App/Teams webhook; GCP budget
   notifications -> Pub/Sub -> Cloud Function -> Slack. Route by account/subscription/project
   owner, not to one shared channel.
2. **Recommendations to tickets**: weekly job pulls rightsizing/idle recommendations (Compute
   Optimizer, Azure Advisor, GCP Recommender, or the FinOps platform API), dedupes against open
   tickets by resource ID, creates Jira issues in the owner's project with monthly savings, resource
   link and suggested action.
3. **Weekly digest**: per-team message with last week's spend, change vs prior week, top 3 movers,
   open recommendations value. Short, with a link to the dashboard.
4. **Closing the loop**: when a ticket closes as done, verify the resource change in inventory and
   record realised savings; "won't do" requires a reason (feeds exceptions).

## Steps
1. Build the owner map (account/project/tag -> team -> channel + Jira project).
2. Start with anomalies (high signal), then digests, then recommendation tickets.
3. Set thresholds so each team gets few, valuable messages (e.g. ticket only if > $100/month).
4. Track response metrics: alert acknowledgement time, ticket closure rate, realised savings.

## Gotchas
- One #finops-alerts channel for everyone becomes noise nobody reads.
- Re-creating tickets each week for the same resource; dedupe on resource ID and status.
- Webhook URLs are secrets; keep them in a secrets manager.

## Verify
- [ ] Every alert and ticket lands with the owning team.
- [ ] Realised savings are recorded from closed tickets.
