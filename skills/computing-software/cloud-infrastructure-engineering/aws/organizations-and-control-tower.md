---
id: computing-software.cloud-infrastructure-engineering.aws.organizations-and-control-tower
name: organizations-and-control-tower
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, organizations, aws-organizations, control-tower, landing-zone, multi-account, account-structure, organizational-units, ou, account-factory, aft, account-factory-for-terraform, delegated-administrator, management-account, scp, rcp, controls, guardrails, region-deny, enroll-account, drift, log-archive, audit-account, all-features, ct-controls, proactive-controls, detective-controls, account-closure, close-account, move-account, invite-account]
level: advanced
status: draft
description: "Stand up and run an AWS Organization with Control Tower: all-features org, OU layout, Account Factory vending, delegated admins, controls, enrolling existing accounts and fixing drift."
sources: ["AWS Organizations User Guide - Managing organizational units and accounts", "AWS Organizations User Guide - Delegated administrator for AWS services", "AWS Control Tower User Guide - Getting started and landing zone setup", "AWS Control Tower User Guide - Controls library and region deny", "AWS Control Tower User Guide - Enroll an existing account", "Account Factory for Terraform (AFT) documentation", "AWS whitepaper - Organizing Your AWS Environment Using Multiple Accounts"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS Organizations and Control Tower — operating the account structure

**Goal:** an organisation where every new account arrives pre-baselined (logging, Config,
guardrails, SSO) in minutes, the management account does nothing but govern, and no
account can leave the guardrails without a visible drift alarm. The design rationale
(why many accounts, OU shapes across clouds) is in
`computing-software.cloud-infrastructure-engineering.cloud-architecture.multi-account-landing-zone`;
this skill is the AWS mechanics.

## 1. Organizations first, then Control Tower on top
- Create the org from a clean, dedicated **management account** (no workloads, no IAM
  users except break-glass): `aws organizations create-organization --feature-set ALL`.
  Consolidated-billing-only orgs cannot use SCPs, RCPs or most delegated-admin features;
  converting later needs every member account to approve the handshake.
- Enable trusted access for the services you will delegate:
  `aws organizations enable-aws-service-access --service-principal guardduty.amazonaws.com`
  (also `securityhub`, `config`, `cloudtrail`, `sso`, `ipam`, `backup`, `account`).
- **Delegated administrators** keep the management account out of daily use:
  `aws organizations register-delegated-administrator --account-id <AUDIT_ACCT> --service-principal guardduty.amazonaws.com`.
  Typical: security tooling → Audit account; CloudTrail/Config aggregation → Log Archive
  account; IPAM and Network Manager → Network account; Organizations policy management
  itself can be delegated with a resource-based delegation policy.
- Invite vs create: `create-account --email <unique> --account-name <name>` (one unique
  email per account — plus-addressing works); for existing accounts send an invitation
  and accept it from the member (`accept-handshake`).

## 2. OU layout that survives growth
Keep it shallow (five levels max, two or three in practice):
```
Root
├── Security        (Log Archive, Audit)           ← Control Tower creates these
├── Infrastructure  (Network, Shared Services)
├── Workloads
│   ├── Prod
│   └── NonProd
├── Sandbox         (per-developer, budget-capped, region-restricted)
├── Suspended       (SCP denies everything; accounts parked before closure)
└── Exceptions      (legacy accounts that cannot yet meet the baseline)
```
Policies attach to OUs, not accounts, so moving an account (`move-account`) is how you
change its guardrails. Accounts closed with `close-account` stay visible for 90 days and
count toward the closure quota (10% of member accounts per rolling 30 days).

## 3. Control Tower setup
- Launch from the management account in the **home region**; choose governed regions
  deliberately — the **Region deny** control blocks API calls everywhere else (global
  services such as IAM, Route 53, CloudFront and STS stay reachable).
- It creates the Security OU with **Log Archive** (org CloudTrail + Config delivery
  bucket) and **Audit** (aggregator, SNS notifications, cross-account audit role),
  an org-level CloudTrail and a Config recorder/aggregator per governed region, and
  IAM Identity Center with default permission sets.
- Controls (formerly guardrails) come in three kinds: **preventive** (SCPs),
  **detective** (Config rules) and **proactive** (CloudFormation hooks that reject
  non-compliant templates before creation). Mandatory ones cannot be disabled; apply
  elective ones per OU with `aws controltower enable-control --control-identifier
  arn:aws:controltower:<region>::control/<ID> --target-identifier <OU_ARN>`.
- Bring your own: Control Tower only manages its own SCPs; attach custom SCPs/RCPs with
  Organizations directly (see `...aws.iam-policies-and-roles`) and do not edit the
  `aws-guardrails-*` policies by hand — that registers as drift.

## 4. Account vending
- **Account Factory** (Service Catalog product) creates an account, places it in an OU,
  enrols it and applies the baseline. The requester needs Identity Center access to the
  provisioning product; the account owner email must be unused.
- **Account Factory Customization (AFC)** runs a CloudFormation blueprint from a hub
  account in each new account — enough for VPC deletion, tagging and a bootstrap role.
- **AFT** (Account Factory for Terraform) is the GitOps path: an account request is a
  Terraform resource in a repo; a pipeline in the AFT management account vends the
  account, then runs global and account-specific customisation stages. Use it when
  requests must be reviewable and reproducible; it adds a dedicated AFT account and a
  CodePipeline/Step Functions footprint you own.
- **Enrolling an existing account:** it needs the `AWSControlTowerExecution` role
  trusting the management account, no existing Config recorder/delivery channel in the
  governed regions (delete them or enrolment fails), and it must be in a registered OU.
  Then `Enroll account` from the console or re-register the OU.

## 5. Drift and lifecycle
- Drift = any deviation from what Control Tower deployed: an SCP detached, an account
  moved outside the console, a Config recorder deleted. The dashboard shows it; fix with
  **Re-register OU** (re-applies the baseline to every account in the OU) or **Repair**
  on the landing zone. Repair also upgrades the landing-zone version — read release
  notes first, it can change the Config resource-recording scope and cost.
- Decommissioning: Control Tower's decommission removes its stacks but leaves accounts,
  org CloudTrail bucket and Identity Center in place; it is one-way.
- Quotas worth knowing: a new organisation's default **account quota is 10**; raise it via
  Service Quotas well before vending day — the increase is not instant.

## Gotchas
- A member account created by `create-account` has an `OrganizationAccountAccessRole`
  (Control Tower: `AWSControlTowerExecution`) trusting the management account; that role
  is the only way in until Identity Center is wired. Do not delete it.
- Control Tower's org CloudTrail is one trail: enabling a second org trail in a member
  account duplicates management events and doubles the bill.
- Region deny is an SCP; it also blocks *your* pipelines that call un-governed regions
  (STS `GetCallerIdentity` works, but `ec2:DescribeRegions` scripts fail oddly).
- The management account is exempt from SCPs. Anything that must be constrained must
  live in a member account.
- Billing: consolidated billing shares Reserved Instance and Savings Plan discounts
  across the org by default; turn sharing off per account in Billing preferences if a
  chargeback model needs it isolated.

## Verify
- [ ] `aws organizations describe-organization` shows `FeatureSet: ALL`; management account has no workloads.
- [ ] Every account sits in a registered OU; the Control Tower dashboard shows zero drift.
- [ ] Delegated admins registered for GuardDuty, Security Hub, Config, CloudTrail and Identity Center; management-account logins are break-glass only.
- [ ] A test account vends end to end (request → enrolled → baseline Config rules compliant → SSO login works) in under 30 minutes.
- [ ] Region deny tested: an API call in a non-governed region returns `AccessDenied` citing the SCP.
