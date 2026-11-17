---
id: computing-software.cloud-infrastructure-engineering.aws.scp-allow-list-strategy
name: scp-allow-list-strategy
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, scp, allow-list-scp, scp-allow-strategy, approved-services, organizations, fullawsaccess]
level: advanced
status: docs-checked
description: "Run an SCP allow-list: replace FullAWSAccess with approved-service allows at every OU level, onboard new services, and avoid locking out landing-zone tooling."
sources: ["https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps_evaluation.html", "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps_syntax.html", "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_reference_limits.html", "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_access-denied.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SCP allow-list strategy

**When:** regulated environments where every AWS service must be approved before use.
The default deny-list strategy (FullAWSAccess plus targeted denies) is simpler; choose
allow-list only if you can staff the service-approval process.

## 1. How allow-lists evaluate
For an action to be allowed by SCPs it must be allowed at **every level** from the root
down to the account: root, each parent OU, and the account itself. Removing
`FullAWSAccess` at a level and attaching an allow-list there means only those services
pass through that level. Explicit denies anywhere still win.

## 2. Structure
- Root: keep `FullAWSAccess` (simplifies; the management account is unaffected anyway). The
  documentation also describes the alternative of attaching the allow-list SCPs at the root only
  and leaving `FullAWSAccess` below it: allows intersect, so the root-level allow-list sets the
  effective list for the whole organization. Per-OU allow-lists give finer control.
- Top-level OUs (Workloads, Sandbox, Security, Infrastructure): detach
  `FullAWSAccess`, attach `Allow-Baseline` (services every account needs) and
  `Allow-<OU>` (OU-specific).
- Child OUs and accounts: must also have an allow; most teams attach `FullAWSAccess`
  below the filtering level so only one level filters. Forgetting this is the classic
  outage: the account still has FullAWSAccess but the OU in between has nothing.

Baseline example (SCP limit is 10,240 characters; service prefixes, not actions):
```json
{"Version": "2012-10-17",
 "Statement": [{"Sid": "ApprovedServices", "Effect": "Allow",
   "Action": ["access-analyzer:*", "acm:*", "autoscaling:*", "backup:*", "cloudformation:*",
              "cloudtrail:*", "cloudwatch:*", "config:*", "dynamodb:*", "ec2:*", "ecr:*",
              "ecs:*", "elasticloadbalancing:*", "events:*", "guardduty:*", "health:*",
              "iam:*", "kms:*", "lambda:*", "logs:*", "rds:*", "route53:*", "s3:*",
              "secretsmanager:*", "securityhub:*", "sns:*", "sqs:*", "ssm:*", "sso:*",
              "sts:*", "support:*", "tag:*", "xray:*"],
   "Resource": "*"}]}
```
Limits (Organizations quotas page): at most 10 SCPs directly attached to the root, an OU or an
account, 10,240 characters each. The console strips extra whitespace; the CLI and SDKs store the
text exactly as sent. Use `service:*` granularity.

## 3. Services you will forget
Landing-zone tooling and consoles call more than their headline service. Build the list from
service last accessed data and your CloudTrail history, and expect to need entries such as these
(confirm each against your own usage):
- Control Tower / AFT: `controltower:*`, `servicecatalog:*`, `organizations:Describe*`,
  `organizations:List*`, `sso:*`, `sso-directory:*`, `identitystore:*`.
- Console experience: `ce:*` (if billing views wanted), `resource-explorer-2:*`,
  `resource-groups:*`, `notifications:*`, `account:Get*`.
- Encryption/keys used indirectly: `kms:*` for any encrypted service.
- Service-linked role creation (`iam:CreateServiceLinkedRole`) is IAM, covered by `iam:*`.
Calls made **by** AWS services through service-linked roles are not affected by SCPs.

## 4. Approving a new service
1. Request with use case, data classification, and the service's security docs
   (compliance validation, encryption, VPC endpoint support).
2. Add deny guardrails for the service if needed (e.g. require encryption keys).
3. Add the prefix to `Allow-<OU>` for the target OU first (Sandbox), then promote.
4. Record in the service catalogue; announce.

## 5. Diagnosing
- Error: `... because no service control policy allows the <action> action`. This
  wording (as opposed to "explicit deny") means an allow is missing at some level.
- `aws organizations list-policies-for-target --target-id <ou-or-account> --filter
  SERVICE_CONTROL_POLICY` up the parent chain (`list-parents`) to find the level lacking it.
- Service last accessed data for an Organizations entity (`aws iam generate-organizations-access-report
  --entity-path <path>`) shows which services accounts actually use; use it to build the initial list.

## Gotchas
- Detaching `FullAWSAccess` before attaching the replacement allow blocks every call in that
  OU, and an entity must always keep at least one SCP. Attach first, then detach.
- Older guidance says SCP Allow statements accept only `Action` with `Resource: "*"`. The current
  SCP syntax page lists `Condition`, `Resource` and `NotResource` as usable with Allow as well as
  Deny, but keep allow-lists to plain service prefixes: conditional allows across several levels
  are very hard to reason about. Put conditions in Deny statements.
- The documentation warns that relying only on Allow statements and implicit deny can give
  unintended access when broad or overlapping allows exist; pair allow-lists with explicit denies.
- Region lock still needs a deny statement; allow-lists cannot express it.

## Verify
- [ ] Every OU level and account in the path has an allow for each baseline service (script the parent-chain check).
- [ ] A non-approved service call (e.g. `aws gamelift list-fleets`) fails with "no service control policy allows".
- [ ] Control Tower landing zone update, AFT account vending and security automation succeed in the filtered OU.
- [ ] Service-approval runbook exists and the last approval was promoted Sandbox to Workloads.

## Checked

Checked 2026-10-27 against the AWS Organizations User Guide pages on SCP evaluation, SCP syntax, quotas and service limits, and Service control policies, the IAM User Guide page on troubleshooting access denied, and the botocore organizations and iam models:
- An allow must exist at every level from root to account; `FullAWSAccess` is attached by default and removing it without a replacement blocks everything; an allow-list at the root alone is documented.
- Quotas read on the Organizations quotas page: SCP size 10,240 characters, 10 SCPs attached per root, OU or account, at least 1 per entity, 5 OU levels. The older figures of 5,120 characters and 5 SCPs were wrong.
- SCP syntax lists Condition, Resource and NotResource for Allow and Deny.
- The two denial message wordings ("no service control policy allows the ... action" and "explicit deny in a service control policy") are in the troubleshooting page.
- Service last accessed data for an Organizations entity is `generate-organizations-access-report` (`EntityPath`) in the IAM model; service-linked roles and the management account are not restricted by SCPs.
The service lists in the Services-you-will-forget section are presented as examples to confirm, not as documented requirements. Commands were not run.

Method: documentation only; no commands were run.
