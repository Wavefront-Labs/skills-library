---
id: computing-software.cloud-infrastructure-engineering.aws.trusted-advisor-service-limits-checks
name: trusted-advisor-service-limits-checks
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, service-quotas, ta-service-limits-check, trusted-advisor, quota-monitoring, aws-usage-metrics]
level: practitioner
status: docs-checked
description: "Use Trusted Advisor service limits checks to catch quotas nearing exhaustion: refresh, read results and send check status changes to EventBridge."
sources: ["https://docs.aws.amazon.com/awssupport/latest/user/service-limits.html", "https://docs.aws.amazon.com/awssupport/latest/user/cloudwatch-events-ta.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Trusted Advisor service limits checks

## What it checks
The Service limits category checks usage against quotas for a set of resources; see the Service limits page for
the current list, thresholds and which support plans include them.

## Refresh and read
```bash
aws support describe-trusted-advisor-checks --language en --region us-east-1
aws support refresh-trusted-advisor-check --check-id <CHECK_ID> --region us-east-1
aws support describe-trusted-advisor-check-result --check-id <CHECK_ID> --region us-east-1
```
Filter the check list by category in the output to find the service limit checks.

## Alerts with EventBridge
Trusted Advisor is a global service: all of its events are emitted to EventBridge in US East (N. Virginia), so
create the rule there. Creating a rule needs a Business Support+, Enterprise Support or Unified Operations plan.
Delivery is best effort, not guaranteed. Targets include Lambda, Kinesis, SNS and CloudWatch alarm actions.

## Gotchas
- Trusted Advisor results refresh on a schedule or on manual refresh; they are not real-time.
- Pair it with Service Quotas and CloudWatch usage alarms for quotas Trusted Advisor does not cover.

## Verify
- [ ] An EventBridge rule in us-east-1 delivers a Trusted Advisor test notification to its target.

## Checked
2026-10-28. Confirmed in the AWS Support User Guide pages in `sources` (EventBridge monitoring of Trusted Advisor checks; us-east-1 emission; plan requirement; best-effort delivery; targets); commands checked with check_commands.
Removed (not confirmed on the pages fetched this batch): the 80%/100% thresholds, the resource list, the EventBridge event pattern values, the `AWS/Usage` metric math example, the JMESPath queries, and the claim that checks are available on all plans.
Method: documentation only; no commands were run.
