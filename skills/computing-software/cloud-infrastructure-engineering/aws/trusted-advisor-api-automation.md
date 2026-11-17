---
id: computing-software.cloud-infrastructure-engineering.aws.trusted-advisor-api-automation
name: trusted-advisor-api-automation
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, trusted-advisor, trusted-advisor-api, ta-refresh, support-api, trustedadvisor-api, eventbridge, organizational-view, check-results, cost-optimization-checks, service-limits, automation]
level: practitioner
status: docs-checked
description: "Automate Trusted Advisor: list and refresh checks through the Support and Trusted Advisor APIs, react to check status changes via EventBridge, and aggregate results across an org."
sources: ["https://docs.aws.amazon.com/awssupport/latest/user/trustedadvisor.html", "https://docs.aws.amazon.com/awssupport/latest/user/get-started-with-aws-trusted-advisor-api.html", "https://docs.aws.amazon.com/awssupport/latest/user/cloudwatch-events-ta.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Trusted Advisor automation via API and EventBridge

**Goal:** Trusted Advisor findings (idle resources, open security groups, service limits,
exposed keys) turn into tickets and dashboards automatically, refreshed on a schedule,
across every account — not a console page someone looks at quarterly.

## 1. Access
- The Trusted Advisor API and EventBridge rules for checks require a **Business Support+,
  Enterprise Support or Unified Operations** plan; other plans get an Access Denied exception.
  AWS has announced that Developer and Business Support end on 2027-01-01: read the support plan
  page for the current plan names.
- Two APIs:
  - **AWS Support API** (`aws support ...`) — the classic check/result/refresh calls.
  - **Trusted Advisor API** (`aws trustedadvisor ...`) — recommendation-centric:
    `ListChecks`, `ListRecommendations`, `GetRecommendation`, `ListRecommendationResources`,
    `UpdateRecommendationLifecycle`.

## 2. Support API: list, refresh, read
```bash
aws support describe-trusted-advisor-checks --language en \
  --query 'checks[].[id,name,category]' --output table
aws support refresh-trusted-advisor-check --check-id <CHECK_ID>
aws support describe-trusted-advisor-check-refresh-statuses --check-ids <CHECK_ID>
aws support describe-trusted-advisor-check-result --check-id <CHECK_ID> --language en \
  --query 'result.flaggedResources[?status!=`ok`].[metadata]'
```
- Send one refresh request, then poll the refresh status. Statuses: `none` (never refreshed),
  `enqueued`, `processing`, `success` (refresh data available), `abandoned` (failed).
- Reading a result does not generate updated data; refresh first.
- `metadata` is an array whose column meaning comes from the check's `metadata` list in
  `describe-trusted-advisor-checks`; map by index.

## 3. Trusted Advisor API (recommendations, org view)
```bash
aws trustedadvisor list-recommendations --status warning --pillar cost_optimizing
aws trustedadvisor list-recommendation-resources --recommendation-identifier <ARN>
aws trustedadvisor list-organization-recommendations                      # Trusted Advisor Priority only
aws trustedadvisor update-recommendation-lifecycle --recommendation-identifier <ARN> \
  --lifecycle-stage dismissed --update-reason-code non_critical_account \
  --update-reason "sandbox account, not production"
```
Lifecycle stages `pending_response`, `in_progress`, `dismissed`, `resolved` let teams record
decisions instead of re-seeing the same finding. `--update-reason` must be 10 to 4096 characters.
Reason codes: `non_critical_account`, `temporary_account`, `valid_business_case`,
`other_methods_available`, `low_priority`, `not_applicable`, `other`. Status filter values are
`ok`, `warning`, `error`; pillar values include `cost_optimizing`, `security` and `service_limits`.

## 4. React with EventBridge
Trusted Advisor is a global service, so all its events are emitted to EventBridge in
**US East (N. Virginia)**; create the rule there. In the console choose AWS service
"Trusted Advisor" and event type "Check Item Refresh Status", then pick statuses (`ERROR`, `WARN`,
`INFO`, `OK`), specific checks or any check, and any resource ID or specific ARNs. Delivery is
best effort, not guaranteed. Targets such as Lambda, SNS, Kinesis or a CloudWatch alarm action can
open a ticket or notify. Pair with a scheduled job that calls `refresh-trusted-advisor-check` for
the checks you act on.

## 5. Org-wide reporting
- `ListOrganizationRecommendations` and the other organization calls cover only prioritized
  recommendations (Trusted Advisor Priority) and run from a management or delegated admin account
  with Priority activated; otherwise they return Access Denied.
- Aggregate that output into S3/Athena on a schedule.

## Gotchas
- Events fire when a check changes status; a check that has been red for months
  produces nothing. Seed tickets from a one-off full export.
- Events are best effort, so also poll results on a schedule.

## Verify
- [ ] Scheduled refresh Lambda runs and `describe-trusted-advisor-check-refresh-statuses` shows `success`.
- [ ] Opening an SG to `0.0.0.0/0:22` in a test account produces an EventBridge event in us-east-1 and a ticket.
- [ ] The organization listing returns the prioritized recommendations for member accounts.

## Checked
2026-10-28. Confirmed against the Support User Guide pages "Get started with the Trusted Advisor API" (required plans, Access Denied, operations, Priority-only organization calls), "Monitoring Trusted Advisor with EventBridge" (us-east-1, statuses, best effort, console event type) and "Use the AWS Support API" (refresh statuses, polling), plus botocore trustedadvisor and support models (lifecycle stages, reason codes, updateReason 10-4096 characters, pillar and status enums, check metadata lists). Corrected: updateReason "sandbox" was below the 10-character minimum; plan names updated; organization calls need Priority. Removed unconfirmed claims: Support API endpoint region, refresh rate limit, the detail-type string, check names, organizational view reports, SubscriptionRequiredException, Service Quotas overlap. The Trusted Advisor API reference landing page was unreadable and is no longer cited.
Method: documentation only; no commands were run.
