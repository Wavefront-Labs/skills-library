---
id: computing-software.cloud-infrastructure-engineering.aws.aws-health-and-trusted-advisor
name: aws-health-and-trusted-advisor
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, trusted-advisor, aws-health, health-dashboard, personal-health-dashboard, health-api, scheduled-changes, planned-lifecycle-events, eventbridge-health-events, organizational-view, trusted-advisor-checks, service-limits-check, support-plan, deprecation-notices, aws-support-api]
level: practitioner
status: draft
description: "Turn AWS Health events (outages, maintenance, deprecations) and Trusted Advisor checks into tickets and pages instead of unread emails: EventBridge routing, organizational view, check refresh."
sources: ["AWS Health User Guide - Monitoring AWS Health events with Amazon EventBridge", "AWS Health User Guide - Aggregating AWS Health events across accounts (organizational view)", "AWS Support User Guide - Trusted Advisor check reference", "AWS Trusted Advisor - Organizational view and Trusted Advisor Priority"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AWS Health and Trusted Advisor — hear about AWS-side problems before your customers do

**Goal:** every Health event that affects *your* resources (an EC2 host retirement, an RDS
maintenance, a Lambda runtime deprecation, a regional degradation) reaches the right
on-call channel, and Trusted Advisor findings become tracked work, not a dashboard nobody opens.

## 1. AWS Health
- Three event scopes: **public** (region/service issues; also on the public status page),
  **account-specific** (affects your resources: `AWS_EC2_INSTANCE_RETIREMENT_SCHEDULED`,
  `AWS_RDS_MAINTENANCE_SCHEDULED`, `AWS_LAMBDA_RUNTIME_DEPRECATION…`), and
  **planned lifecycle events** (deprecations with deadlines, e.g. EKS version end of support)
  with an *affected resources* list.
- Console: Health Dashboard → *Your account health*; API (`aws health describe-events
  --filter eventStatusCodes=open,upcoming`) **requires Business/Enterprise support**;
  EventBridge events do not.
- **Organizational view**: enable in the management account (`enable-health-service-access-for-organization`)
  to see/aggregate all member-account events; delegated administrator supported.

## 2. Route events with EventBridge (every account, every region)
```json
{"source":["aws.health"],"detail-type":["AWS Health Event"],
 "detail":{"eventTypeCategory":["issue","scheduledChange"],"service":["EC2","RDS","LAMBDA","EKS"]}}
```
- Targets: SNS (→ chat/pager), Lambda (→ Jira/ServiceNow), Incident Manager, SSM Automation
  (e.g. stop/start an instance on `AWS_EC2_INSTANCE_RETIREMENT_SCHEDULED` to move hosts).
- Health events for **global services** (IAM, Route 53, CloudFront) are emitted in `us-east-1`;
  keep a rule there regardless of your home region.
- `eventTypeCategory`: `issue` (outage), `accountNotification` (billing/security notices),
  `scheduledChange` (maintenance, retirements), `investigation`. Page on `issue`; ticket the rest.
- Deploy the **AWS Health Aware** (AHA) sample for a ready-made Slack/Teams/ServiceNow pipeline.
- Health events include `affectedEntities` (ARNs/instance ids); enrich tickets with the
  owner tag of the entity via the Tagging API.

## 3. Trusted Advisor
- Checks in categories: **cost optimization** (idle LBs, low-utilisation EC2, unassociated
  EIPs, RI/SP recommendations), **performance**, **security** (S3 public, security groups
  open on 0.0.0.0/0, MFA on root, IAM key rotation), **fault tolerance** (single-AZ RDS,
  ASG health, EBS snapshot age), **service limits**, **operational excellence**.
- Free tier: a handful of security + all service-limit checks; Business/Enterprise: all checks,
  API (`aws support describe-trusted-advisor-checks --language en`,
  `refresh-trusted-advisor-check`, `describe-trusted-advisor-check-result`) and
  **organizational view** reports (aggregate across accounts, CSV/JSON to S3).
- Checks refresh automatically ~weekly; force with `refresh-trusted-advisor-check` (rate-limited, some checks cannot be refreshed).
- **EventBridge**: `source: aws.trustedadvisor`, `detail-type: Trusted Advisor Check Item Refresh Notification`
  with `status` (`ERROR`/`WARN`/`OK`) and `check-name`; route `ERROR` on security checks to the
  security channel, cost checks to FinOps.
- **Trusted Advisor Priority** (Enterprise): AWS account team curates the top recommendations.
- Overlaps: Security Hub (security checks, richer), Compute Optimizer (rightsizing), Cost
  Optimization Hub (savings), Service Quotas (limits). Use Trusted Advisor as the cross-cutting
  summary, those services for depth; suppress/exclude items you consciously accept.

## 4. Operating cadence
- Daily: pager on Health `issue` events; weekly: review `scheduledChange` with deadlines
  (host retirements need an instance stop/start before the date; RDS maintenance windows
  can be deferred once).
- Monthly: Trusted Advisor org report → tickets by owner tag; track the count of `ERROR`
  items over time.
- Quarterly: planned lifecycle events (runtime/engine deprecations) into the roadmap.

## Gotchas
- Email notifications go to the root/alternate contacts — set **alternate contacts**
  (operations, security, billing) per account or via Organizations, or nobody reads them.
- EventBridge Health rules must exist in **each region** where you have resources plus `us-east-1`.
- Health API calls fail with `SubscriptionRequiredException` on Basic/Developer support; use the dashboard/EventBridge.
- Trusted Advisor's "low utilisation EC2" uses 14-day CPU/network averages — batch hosts
  that run nightly show as idle; exclude them.
- Scheduled changes can be rescheduled by AWS; re-read the event's `lastUpdatedTime`.
- Unconfirmed: current free-tier check list and whether the Health API still requires paid support — verify.

## Verify
- [ ] An EventBridge rule for `aws.health` exists in every active region and `us-east-1`, targeting the on-call channel.
- [ ] Alternate contacts set on all accounts (`aws account get-alternate-contact --alternate-contact-type OPERATIONS`).
- [ ] Organizational view enabled; the management account dashboard lists member-account events.
- [ ] A Trusted Advisor `ERROR` on "Security Groups - Unrestricted Access" creates a ticket automatically.
- [ ] Last quarter's planned lifecycle events are all either actioned or on the roadmap with an owner.
