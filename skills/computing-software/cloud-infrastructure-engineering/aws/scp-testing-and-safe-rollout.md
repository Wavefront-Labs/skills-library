---
id: computing-software.cloud-infrastructure-engineering.aws.scp-testing-and-safe-rollout
name: scp-testing-and-safe-rollout
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, organizations, scp, scp-testing, scp-rollout, scp-denial, cloudtrail, policy-validation]
level: practitioner
status: docs-checked
description: "Roll out SCP changes without outages: Access Analyzer validation, CloudTrail impact analysis, staging through a test OU, and reading SCP denials."
sources: ["https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-validation.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_access-denied.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing SCPs and rolling them out safely

An SCP mistake applies instantly to every account below the target. Treat SCPs like
production code.

## 1. Before attaching
- **Validate**: `aws accessanalyzer validate-policy --policy-type SERVICE_CONTROL_POLICY --policy-document file://scp.json`
  (`SERVICE_CONTROL_POLICY` is a valid `--policy-type`).
- **Impact analysis**: who currently does what you're about to deny?
  - CloudTrail Lake / Athena over the org trail: count events matching the denied
    `eventSource`/`eventName`/region in the last 90 days, grouped by account and principal.
  - Service last accessed data for the OU: `aws iam generate-organizations-access-report --entity-path <path>`
    shows which services are used at all.
- Add exceptions for pipelines/break-glass via `aws:PrincipalArn` conditions before attaching.

## 2. Stage it
1. Attach to a **test OU** with a sandbox account; run smoke tests (deploy pipeline,
   console login via SSO, Security tooling, Backup jobs).
2. Attach to a **non-prod OU**; watch for a few days.
3. Attach to prod OUs. Keep every SCP in git and deploy via IaC/pipeline so you can re-attach
   the previous text.

## 3. Recognising an SCP denial
- Error messages: `... with an explicit deny in a service control policy` (the documented example
  names the policy ARN) for a Deny, and `... because no service control policy allows the <action> action`
  when an Allow is missing at some level.
- CloudTrail: an access denied error whose message mentions a service control policy.
- Athena query for fallout after rollout:
```sql
SELECT useridentity.arn, eventsource, eventname, count(*) n
FROM cloudtrail_logs
WHERE errormessage LIKE '%service control policy%' AND eventtime > '<ROLLOUT_TIME>'
GROUP BY 1,2,3 ORDER BY n DESC;
```

## 4. Rollback
`aws organizations detach-policy --policy-id p-new --target-id ou-...` (and reattach the old
one). Make sure the management account (unaffected by SCPs) has a
role that can run it.

## Gotchas
- AWS recommends not attaching SCPs to the root without thorough testing: create a test OU and move accounts in one at a time or in small groups. Do not remove `FullAWSAccess` unless you replace it.
- Test with real calls in the sandbox. Region-deny SCPs usually need `NotAction` exemptions for global services; confirm each against your own CloudTrail data.

## Verify
- [ ] Impact query run and exceptions documented before attach.
- [ ] Post-rollout Athena query shows no unexpected SCP denials after 24 h.
- [ ] SCP source in git with pipeline-based attach/detach.

## Checked

Checked 2026-10-27 against the AWS Organizations User Guide page "Service control policies (SCPs)", the IAM User Guide pages on policy validation and troubleshooting access denied, and the botocore accessanalyzer, iam and organizations models:
- `validate-policy` accepts policy type `SERVICE_CONTROL_POLICY`.
- `generate-organizations-access-report` takes an entity path for service last accessed data.
- The two SCP denial wordings and the guidance to test in a separate OU and not remove `FullAWSAccess`.
Removed: the "SCPs have no versions" and "takes effect within minutes" statements and the policy simulator remark, which no page confirmed. The commands and SQL were not run.

Method: documentation only; no commands were run.
