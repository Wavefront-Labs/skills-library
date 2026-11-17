---
id: computing-software.cloud-infrastructure-engineering.aws.new-account-quotas-and-quota-request-templates
name: new-account-quotas-and-quota-request-templates
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, service-quotas, new-account-quotas, quota-request-template, account-vending, organizations, control-tower]
level: practitioner
status: docs-checked
description: "Avoid launch-day quota failures in new AWS accounts: low starting quotas, Service Quotas request templates applied automatically at account creation, and vending checklists."
sources: ["https://docs.aws.amazon.com/servicequotas/latest/userguide/organization-templates.html", "https://docs.aws.amazon.com/servicequotas/latest/userguide/gs-request-quota.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# New account quotas and pre-requests during account vending

## Why new accounts fail
An account's applied quota can be lower than the AWS default if it is new or used minimally
(Service Quotas guide); other services also start new accounts in sandboxes (for example SES and SNS SMS).
A production cut-over into a fresh account can hit these on day one, so check applied values.

## Quota request templates (Organizations)
From the management account (or delegated admin):
```bash
aws service-quotas associate-service-quota-template
aws service-quotas put-service-quota-increase-request-into-template \
  --service-code lambda --quota-code <QUOTA_CODE> --aws-region eu-west-1 --desired-value <VALUE>
aws service-quotas put-service-quota-increase-request-into-template \
  --service-code ec2 --quota-code <QUOTA_CODE> --aws-region eu-west-1 --desired-value <VALUE>
aws service-quotas list-service-quota-increase-requests-in-template
```
- When the template is associated, new accounts created in the organization automatically get these requests submitted; if you disable the association, new accounts receive the AWS default values.
- The template holds up to 10 quotas; pick the ones that always bite.
- Requires AWS Organizations with all features enabled; supported only in commercial Regions (not China or opt-in Regions).
- Updating the template does not change quotas of existing accounts: script requests for them.
- Find quota codes with `aws service-quotas list-service-quotas --service-code ec2 --query 'Quotas[].[QuotaCode,QuotaName]'`.

## Account vending checklist (Control Tower Account Factory / AFT customisations)
- Quota template associated (covers new accounts); requests tracked to approval.
- Sandboxes: SES production access request, SNS SMS production and spend limit, where the workload needs them.
- Support plan and alternate contacts set.
- Opt-in Regions enabled, and quota requests made directly there (templates do not cover opt-in Regions).
- Budget and cost anomaly monitor created.

## Request strategy
- Ask for realistic peak + headroom with a short justification.
- Track requests: `aws service-quotas list-requested-service-quota-change-history --status PENDING`.
- Template entries name a Region each: add one per Region you deploy to (including the DR Region).

## Verify
- [ ] Newly vended test account shows template requests in its quota request history.
- [ ] Production launch checklist confirms applied values (`get-service-quota`) in each region.

## Checked

2026-10-28. Confirmed against the Service Quotas user guide (request templates page and request-quota page) and the service-quotas botocore model: template purpose, association behaviour for new accounts, disabling gives default values, 10-quota maximum, Organizations all-features requirement, commercial-Region-only support, template updates not affecting existing accounts, applied value possibly lower for new accounts, put-service-quota-increase-request-into-template required fields. Removed (unconfirmed): hard-coded quota codes, the Lambda 1,000 figure, Pinpoint sandbox, support-case follow-up claim. Read end to end.

Method: documentation only; no commands were run.
