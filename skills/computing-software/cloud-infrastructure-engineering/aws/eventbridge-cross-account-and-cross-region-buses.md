---
id: computing-software.cloud-infrastructure-engineering.aws.eventbridge-cross-account-and-cross-region-buses
name: eventbridge-cross-account-and-cross-region-buses
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, eventbridge, cross-account-bus, cross-region-events, event-bus-policy, central-event-bus, aws-principalorgid, bus-to-bus, event-forwarding, multi-account-events, hub-and-spoke-events, global-endpoints, event-driven]
level: practitioner
status: docs-checked
description: "Route events across accounts and regions with EventBridge: org-scoped bus policies, bus-to-bus targets with roles, what forwarding rewrites, and global endpoints."
sources: ["https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-cross-account.html", "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-cross-region.html", "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-bus-perms.html", "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-bus-permissions-manage.html", "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-global-endpoints.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EventBridge across accounts and regions

**Goal:** workload accounts publish to a central bus (or the central bus fans out to
workloads), with permissions scoped to the organisation and no surprises about which
account/region an event claims to come from.

## 1. Allow senders onto a bus (receiver side)
```bash
aws events put-permission --event-bus-name central --policy '{"Version":"2012-10-17","Statement":[
 {"Sid":"OrgPublish","Effect":"Allow","Principal":"*","Action":"events:PutEvents",
  "Resource":"arn:aws:events:<REGION>:<HUB_ACCOUNT_ID>:event-bus/central",
  "Condition":{"StringEquals":{"aws:PrincipalOrgID":"o-xxxxxxxx"}}}]}'
```
Variants: grant by account ID (the `put-permission` API takes `--principal` as a 12-digit account ID or `*`, plus `--action` and `--statement-id`), or by organization with the `aws:PrincipalOrgID` condition as above. The docs also describe conditions to filter by rule, account or tag. A rule on the receiver matches events from other accounts unless its pattern has an `account` field; if you accept events from many accounts, add `account` to every rule. Do not use `*` in a rule's `account` field: it never matches, omit the field instead.

## 2. Forward from a bus to another bus (sender side)
A **rule target** can be another event bus (same or different account/region):
```bash
aws events put-targets --event-bus-name default --rule to-central --targets \
 '[{"Id":"central","Arn":"arn:aws:events:<REGION>:<HUB_ACCOUNT_ID>:event-bus/central","RoleArn":"arn:aws:iam::<SPOKE_ACCOUNT_ID>:role/eb-forward"}]'
```
- EventBridge requires an IAM role (`RoleArn`) on every cross-account event bus target created after 2 March 2023; the console creates it, with the CLI you create it. AWS recommends roles for all bus targets so SCPs apply. The role must trust `events.amazonaws.com` and allow `events:PutEvents` on the destination bus ARN.
- The receiving bus resource policy grants the sender account or organization.
- Events a receiver gets from a sender account are not forwarded on to a third account. The same applies to three buses in one account: events forwarded from the second bus are not sent to the third. This is a one-hop limit; design the hub so that each event needs only one forward.
- Cost: events sent between accounts are charged to the sending account as custom events; the receiving account is not charged.

## 3. Cross-region
Cross-Region and cross-account routing both work as long as the destination Region is a supported cross-Region destination Region. Rules on the destination bus evaluate the event as received; confirm the `region` and `account` values on a real forwarded event before writing patterns.

## 4. Hub-and-spoke pattern
- Spoke accounts: rule on `default` bus `{"source":[{"prefix":"com.example."}]}` → central
  bus. Also forward selected `aws.*` events (`aws.guardduty`, `aws.health`, `aws.config`) for
  central security/ops.
- Central: rules route by `account`/`source` to consumers. Do not plan on re-forwarding from the central bus to another bus (see the one-hop rule above).
- Alternatively, spokes publish **directly** to the central bus with `PutEvents` using the bus ARN as `EventBusName`; no forwarding rule is involved, but producers need cross-account permission.

## 5. Global endpoints (multi-region failover for publishers)
A global endpoint uses a Route 53 health check; when it reports unhealthy, custom events are routed within minutes to an event bus in the secondary Region. With event replication enabled and the prescriptive alarm configuration, AWS states an RTO and RPO of 360 seconds, maximum 420 seconds. Replication increases monthly cost and is required for automatic recovery back to the primary; without it you must reset the health check manually. Custom buses need the same name in the same account in each Region. With an SDK you need the AWS CRT library, and must pass `EndpointId` and `EventBusName` in `PutEvents`; requests use Signature Version 4A (credentials from the global STS endpoint do not support it by default).

## Gotchas
- `Principal: "*"` with an organization condition limits senders to the organization.
- Cross-account targets other than event buses are covered on the cross-account services page of the EventBridge guide, not here.
- A rule pattern with `"account":["<HUB_ACCOUNT_ID>"]` matches only events from the hub account, so it will not match events from spokes.

## Verify
- [ ] `aws events put-events` from a spoke credential lands on the central bus and matches a rule there (`MatchedEvents`); from an account outside the org it fails `AccessDeniedException`.
- [ ] A forwarded event in a CloudWatch Logs target on the central bus shows which account and Region it carries; write patterns from that sample.

## Checked
2026-10-27. Documentation: Amazon EventBridge User Guide (cross-account, cross-Region, event bus permissions, managing permissions, global endpoints), read this date. Confirmed: org-scoped PutEvents policy with aws:PrincipalOrgID; role required for cross-account bus targets created after 2 March 2023; events received from another account are not forwarded to a third; sender is charged (the draft said the receiver is charged); account field behaviour in rules; global endpoint health check, RTO/RPO 360 s (max 420 s), same-named custom bus per Region, CRT and SigV4A needs, EndpointId and EventBusName. Confirmed from the API model: PutPermission principal is a 12-digit account ID or *. Removed the unsupported claim that a central bus can forward once more to per-team buses, the 256 KB limit, the put-permission replaces-policy claim, events:source condition keys and the claim about which region field forwarded events keep.
Method: documentation only; no commands were run.
