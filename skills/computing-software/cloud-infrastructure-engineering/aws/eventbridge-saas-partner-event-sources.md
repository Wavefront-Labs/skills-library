---
id: computing-software.cloud-infrastructure-engineering.aws.eventbridge-saas-partner-event-sources
name: eventbridge-saas-partner-event-sources
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, eventbridge, partner-event-source, partner-event-bus, saas-integration, event-sources]
level: practitioner
status: docs-checked
description: "Receive SaaS events (Datadog, Zendesk, Shopify, Auth0 and others) through EventBridge partner event sources: setup in the partner, bus association, rules and lifecycle."
sources: ["https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-saas.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EventBridge SaaS partner event sources

**Goal:** get events from a SaaS provider into your account without webhooks, API Gateway or
polling code, then route them with normal rules.

## Flow
1. In the **partner's** console, configure the AWS EventBridge integration with your account id
   and region. The partner creates a **partner event source** in your account named like
   `aws.partner/<partner>/<name>` style (the docs example is `aws.partner/saas-integration/name`); it appears as `Pending`.
2. In your account, associate it with a **partner event bus** (bus name equals source name):
```bash
aws events list-event-sources --name-prefix aws.partner/
aws events create-event-bus \
  --name aws.partner/saas-integration/name \
  --event-source-name aws.partner/saas-integration/name
```
   The source becomes `Active`.
3. Create rules on that bus (not the default bus):
```bash
aws events put-rule --event-bus-name aws.partner/saas-integration/name \
  --name to-queue --event-pattern file://pattern.json
```
   Build `pattern.json` from the partner's documented event fields.
4. Events published by a partner to a source that is not yet associated with a bus are dropped immediately and not stored by EventBridge.

## Partner list
The supported partners are listed in the EventBridge guide and include Auth0, Datadog, PagerDuty, Shopify, Zendesk, Segment and MongoDB. Salesforce is supported via Amazon AppFlow. The partner event source is created from the partner's own site using your account ID (console flow; the source is available only to your account). For SaaS providers without a partner integration, the guide documents receiving events through Lambda function URLs.

## Gotchas
- The CLI association needs both `--name` and `--event-source-name` set to the partner event source name.
- `put-permission` on a partner event bus returns an error, and a CloudFormation `AWS::Events::EventBusPolicy` for it fails: only the partner account of the source may send events to it.
- To receive partner events on the new Custom Event Bus rather than a Classic bus, the guide says to create an event source that names the partner event source as its origin.

## Verify
- [ ] `describe-event-source` shows `ACTIVE`.
- [ ] A test event triggered in the partner shows up in a CloudWatch Logs target on the bus, and rule `MatchedEvents` increases.

## Checked
2026-10-27. Documentation: Amazon EventBridge User Guide, Receiving events from a SaaS partner, read this date. Confirmed: two-step flow (partner creates source, you associate it with a partner bus whose name equals the source name), Pending to Active, CLI create-event-bus and describe-event-source usage, events dropped before association, put-permission and EventBusPolicy errors, partner list entries named in the skill, Salesforce via Amazon AppFlow (the draft said Event Relay), Lambda function URL webhook option. Removed unconfirmed claims about fan-out, deletion behaviour, schema discovery, region mismatch and replay.
Method: documentation only; no commands were run.
