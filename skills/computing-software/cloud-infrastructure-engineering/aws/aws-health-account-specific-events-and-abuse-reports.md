---
id: computing-software.cloud-infrastructure-engineering.aws.aws-health-account-specific-events-and-abuse-reports
name: aws-health-account-specific-events-and-abuse-reports
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, aws-health, account-specific-events, abuse-report, aws-trust-and-safety, risk-credentials-exposed, scheduled-changes]
level: practitioner
status: docs-checked
description: "Triage account-specific AWS Health events by category, query them with the Health API, route them through EventBridge and use the organizational view."
sources: ["https://docs.aws.amazon.com/health/latest/ug/health-api.html", "https://docs.aws.amazon.com/health/latest/ug/cloudwatch-events-health.html", "https://docs.aws.amazon.com/health/latest/ug/aws-health-account-views.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS Health account-specific events

## Event categories
The Health API's event type categories are `issue`, `accountNotification`, `scheduledChange` and `investigation`.
Use them to triage: follow `issue` updates, plan around `scheduledChange` before its date, read
`accountNotification` for account-level notices, and watch `investigation`.

## Query
```bash
aws health describe-events --region us-east-1 --filter \
  eventTypeCategories=scheduledChange,accountNotification eventStatusCodes=open,upcoming
aws health describe-affected-entities --region us-east-1 --filter eventArns=<EVENT_ARN>
aws health describe-events-for-organization --region us-east-1   # org view, management/delegated admin
```
- The Health API needs a Business Support+, Enterprise Support or Unified Operations plan (or the Business, Enterprise On-Ramp or Enterprise Support plans); the console dashboard works for all.
- The API has two regional endpoints in active-passive mode: `us-east-1` (active) and `us-east-2` (passive), plus the global endpoint `global.health.amazonaws.com`. Sign for the Region of the active endpoint; the latest data is only on the active one.
- Rules in EventBridge receive Health events for your own account only; use the organizational view for other accounts.

## Abuse reports and exposed credentials
This skill does not verify AWS Trust and Safety notice formats or deadlines. Read the notice itself and the AWS
abuse-report guidance, treat a compromised resource as an incident (isolate, snapshot, rotate credentials), and
reply by the deadline in the notice.

## Keep contacts right
Set alternate contacts (security, operations, billing) on every account, ideally team distribution lists.

## Verify
- [ ] An EventBridge rule routes your chosen Health event categories to a queue the team watches.
- [ ] Alternate security contact is set on all accounts (`aws account get-alternate-contact`).

## Checked
2026-10-28. Confirmed in the AWS Health User Guide pages in `sources` (Health API plan requirement and endpoints, EventBridge monitoring, account views) and the botocore model (`DescribeEvents` categories); commands checked with check_commands.
Removed (not confirmed on fetched pages): example event type codes, the `aws.health` source and detail-type values, abuse-report types and deadlines, the quarantine-policy name for exposed keys, and the Organizations `put-alternate-contact` wording.
Method: documentation only; no commands were run.
