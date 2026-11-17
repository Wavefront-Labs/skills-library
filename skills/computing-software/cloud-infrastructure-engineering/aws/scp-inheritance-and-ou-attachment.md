---
id: computing-software.cloud-infrastructure-engineering.aws.scp-inheritance-and-ou-attachment
name: scp-inheritance-and-ou-attachment
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, organizations, scp, scp-inheritance, fullawsaccess, ou-attachment, deny-list, allow-list]
level: practitioner
status: docs-checked
description: "Reason about SCP inheritance: intersection of allows down the OU tree, the FullAWSAccess default, deny-list vs allow-list strategies, what SCPs never affect, and quotas."
sources: ["https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps_evaluation.html", "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html", "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_reference_limits.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SCP inheritance and OU attachment

## 1. Evaluation model
For an action in an account to be possible, **every level** from root → each OU → account
must have an SCP that allows it, and **no level** may deny it.
- Allows **intersect** down the tree (a child cannot widen what a parent allows).
- Denies anywhere apply everywhere below.
- SCPs grant nothing; IAM policies in the account still must allow.

## 2. FullAWSAccess
Every root/OU/account starts with the AWS-managed `FullAWSAccess` SCP attached. Detaching it
from an OU without attaching another allow = **everything denied** in that OU.
- **Deny-list strategy** (the default setup): keep `FullAWSAccess` at all levels; add deny SCPs
  (region restriction, protect security tooling, deny leaving the org).
- **Allow-list strategy**: replace `FullAWSAccess` with explicit allow SCPs, either at the root
  only or at each level; where you replace it at several levels every level must allow each
  service, which is high maintenance and easy to get wrong. Allows alone can also give
  unintended access when they overlap, so combine with explicit denies.

## 3. Attach and inspect
```bash
aws organizations attach-policy --policy-id p-denyregions --target-id ou-abcd-11111111
aws organizations list-policies-for-target --target-id 222222222222 --filter SERVICE_CONTROL_POLICY
aws organizations list-parents --child-id 222222222222
```
Effective SCPs for an account = walk `list-parents` to root and collect each level's policies
(console "Policies" tab per account shows inherited ones).

## 4. What SCPs don't affect
- The **management account** (SCPs never apply to it — keep workloads out of it). SCPs do
  apply to member accounts that are delegated administrators.
- **Service-linked roles**.
- A short list of tasks, including registering for the Enterprise support plan as the root
  user and CloudFront trusted signer functionality (see "Tasks and entities not restricted by SCPs").
- (Note the opposite: SCPs **do** apply to the root user of member accounts — that's how you
  restrict member-account root.)
- Users and roles from accounts outside the organization that reach a resource through a
  resource-based policy (resource control policies are the organization-level tool for that).

## 5. Quotas
Per the Organizations quotas page: up to 10 SCPs directly attached to each root, OU or account
(inherited policies do not count; every entity must keep at least 1), 10,240 characters per SCP
(the console strips extra whitespace, the CLI and SDKs store text as sent), OU nesting depth 5.
Combine statements; use `NotAction` patterns carefully.

## Gotchas
- Moving an account between OUs changes its effective SCPs immediately — review before `move-account`.
- An allow-list SCP missing a dependency (e.g. `sts:*` for SSO, `kms:*` for encrypted services) breaks things subtly.
- Deny statements with conditions on `aws:PrincipalArn` exceptions should reference role ARNs with wildcards for `AWSReservedSSO_*` paths.

## Verify
- [ ] Every OU and account has `FullAWSAccess` (deny-list strategy) or a documented allow chain.
- [ ] Policy simulator / a test action in a sandbox account confirms intended denies.
- [ ] SCP sizes checked in CI under 10,240 characters (as saved through the CLI or SDK).

## Checked

Checked 2026-10-27 against the AWS Organizations User Guide pages on SCP evaluation, Service control policies and quotas and service limits:
- Allow needed at every level, deny anywhere wins, intersection of allows, `FullAWSAccess` default and the allow-list at root-only option.
- Exclusions: management account, service-linked roles, listed tasks; SCPs apply to member root users and delegated administrator accounts.
- Quotas: 10 SCPs per root, OU or account (minimum 1), 10,240 characters, 5 OU levels. The older 5 SCPs and 5,120 characters were wrong.
The commands were not run.

Method: documentation only; no commands were run.
