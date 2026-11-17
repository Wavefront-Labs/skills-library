---
id: computing-software.cloud-infrastructure-engineering.aws.aws-support-cases-severity-and-escalation
name: aws-support-cases-severity-and-escalation
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, support-case, case-severity, aws-support-api, escalation, technical-account-manager, incident-response]
level: practitioner
status: docs-checked
description: "Open AWS Support cases that get fast answers: severity by plan, what to include (IDs, UTC times, request IDs), CLI/API case creation, and chat/phone escalation."
sources: ["https://docs.aws.amazon.com/awssupport/latest/user/case-management.html", "https://docs.aws.amazon.com/cli/latest/reference/support/create-case.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS Support cases: severity and escalation

## 1. Severity levels (availability depends on plan)
| Severity | API code | Meaning | First response target (case-management page) |
|---|---|---|---|
| General guidance | `low` | development question or feature request | 24 hours |
| System impaired | `normal` | non-critical functions abnormal | 12 hours |
| Production system impaired | `high` | important functions impaired or degraded | 4 hours (Business Support+, Enterprise, Unified Operations) |
| Production system down | `urgent` | business significantly impacted | 1 hour (same plans) |
| Business-critical system down | `critical` | business at risk, critical functions unavailable | Business Support+ under 30 minutes; Enterprise 15 minutes; Unified Operations 5 minutes |

Plan names and eligibility per severity change; check the case-management page for the
current list. With Basic Support you cannot create a technical case (account/billing cases
and service quota increase requests are open to all customers) and cannot change the severity
after creation. Choose honestly: under-severity delays help.

## 2. What to include (gets a faster first useful answer)
- Account ID, region, resource IDs/ARNs (instance IDs, DB identifiers, load balancer ARN).
- Exact timestamps in **UTC** with start/end of impact.
- Request IDs from error responses (`x-amz-request-id`, `x-amzn-RequestId`, S3 `HostId`),
  CloudTrail event IDs, error messages verbatim.
- What changed recently, what you tried, business impact, and the outcome you need.
- Attach logs/screenshots (each attachment in an API attachment set must be 5 MB or smaller; use upload IDs for larger files).
- Do not include secrets or customer PII.

## 3. Open via CLI/API (needs Business Support+, Enterprise or Unified Operations; otherwise `SubscriptionRequiredException`)
```bash
aws support describe-services --region us-east-1 --query 'services[?contains(name,`Relational`)].{code:code,cats:categories[].code}'
aws support create-case --region us-east-1 \
  --subject "Prod RDS orders failover loop since 09:12 UTC" \
  --service-code amazon-rds --category-code performance --severity-code urgent \
  --communication-body file://case.txt --cc-email-addresses oncall@example.com \
  --language en --issue-type technical
aws support add-communication-to-case --case-id <id> --communication-body "New: failover again 09:40 UTC"
aws support describe-cases --include-resolved-cases false
```
Severity codes: `low`, `normal`, `high`, `urgent`, `critical`.

## 4. Escalation
- When raising a case to Production system down or Business-critical system down, use one of the
  live contact methods (chat or phone) listed on the case-management page; after raising to either level
  you must wait 60 minutes before changing the severity again.

## Verify
- [ ] Support plan level matches the response times your SLAs require.
- [ ] Case template (resource IDs, UTC times, request IDs, impact) exists in the runbook.
- [ ] On-call knows how to open a phone/chat case and who can approve severity.

## Checked

2026-10-28. Confirmed against the AWS Support case-management page and the support create-case CLI reference: severity names, codes and response targets, Basic Support limits, Support API plan requirement and SubscriptionRequiredException, 5 MB attachment limit, live-contact guidance and the 60-minute severity change wait. Removed (unconfirmed): Developer-plan eligibility and "business hours" wording, the us-east-1 endpoint statement, Enterprise IDR/TAM escalation, Health Dashboard, EventBridge automation and Slack app bullets. Read end to end.

Method: documentation only; no commands were run.
