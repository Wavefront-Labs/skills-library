---
id: computing-software.cloud-infrastructure-engineering.aws.organizations-all-features-and-trusted-access
name: organizations-all-features-and-trusted-access
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, organizations, all-features, trusted-access, enable-aws-service-access, consolidated-billing-only, delegated-administrator-setup]
level: practitioner
status: docs-checked
description: "Move an organization from consolidated billing to all features, then enable trusted access per service (CLI vs service console), audit it, and disable it safely."
sources: ["https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_org_support-all-features.html", "https://docs.aws.amazon.com/organizations/latest/userguide/manage-begin-all-features-standard-migration.html", "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_integrate_services.html", "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_integrate_services_list.html", "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_best-practices_mgmt-acct.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Organizations: all features and trusted access

## 1. Consolidated billing only vs all features
An organization with only the consolidated billing feature set produces a single bill and has no other
management capabilities; SCPs and integration with AWS services need all features. Check:
```bash
aws organizations describe-organization --query 'Organization.FeatureSet'
# "ALL" or "CONSOLIDATED_BILLING"
```

## 2. Enabling all features
1. `aws organizations enable-all-features` from the management account (needs
   `organizations:EnableAllFeatures`). This sends a request to **every invited** (not created)
   member account; an account created in the organization gets a request only if its
   `AWSServiceRoleForOrganizations` role was deleted. Unaccepted older invitations are cancelled.
   The requests expire after 90 days, after which you start over.
2. Each invited account's admin must accept: console, or `aws organizations list-handshakes-for-account`
   then `aws organizations accept-handshake --handshake-id h-...` (action `APPROVE_ALL_FEATURES`; needs
   `organizations:AcceptHandshake`). Track status in the console.
3. When all have accepted, the management account finalises in the console ("Finalize") or by accepting
   the enable-all-features handshake. An account that declines must be removed or sent a new request.
4. The change is one-way: you cannot go back to consolidated billing only.
Effects: once all features are on, the management account can apply policy-based controls to member
accounts. Enabling the SCP policy type attaches the `FullAWSAccess` SCP to every root, OU and account,
so nothing is restricted until you attach other SCPs. AWS recommends an SCP at the root denying
`organizations:LeaveOrganization` and `account:CloseAccount`.

## 3. Trusted access
Trusted access lets a service create service-linked roles in every member account and act
org-wide (e.g. Config aggregator, CloudTrail org trail, GuardDuty auto-enable).

**AWS strongly recommends enabling and disabling trusted access from the service's own console, CLI
or API when that option exists** (e.g. `aws guardduty enable-organization-admin-account`,
`aws securityhub enable-organization-admin-account`, `aws cloudtrail create-trail --is-organization-trail`),
so the service can do any required initialization and clean-up. Enabling via Organizations only
changes the Organizations side:
```bash
aws organizations enable-aws-service-access --service-principal <SERVICE_PRINCIPAL>
aws organizations list-aws-service-access-for-organization
```
Find each service's principal, and whether it supports trusted access and delegated
administration, in the "AWS services that you can use with AWS Organizations" table. For example,
centralized root access uses `iam.amazonaws.com`. A service that is enabled this way creates a
service-linked role only where it needs one, not necessarily in every account.

## 4. Delegated administrators
After trusted access, register a member account (Security Tooling, Log Archive) to run the
service so day-to-day work stays out of the management account:
```bash
aws organizations register-delegated-administrator --account-id 222233334444 \
  --service-principal <SERVICE_PRINCIPAL>
aws organizations list-delegated-administrators
```
Many services expose their own call that does this (`enable-organization-admin-account`).
Organizations also has a delegation resource policy (`put-resource-policy`) for delegating some
Organizations actions to a member account.

## 5. Disabling trusted access
Disable from the **service** first (remove delegated admin, turn off org features) so it can clean up,
then `disable-aws-service-access` if needed. Disabling only in Organizations stops the service creating
service-linked roles in new accounts and removes its permissions from the organization and its
accounts. Disabling trusted access does not stop users with permissions from using the service; use IAM
permissions or SCPs for that. Check the per-service notes before doing it.

## Gotchas
- `enable-all-features` handshake is visible to member admins; brief them, an unknown
  "accept" prompt looks like phishing.
- SCPs never apply to the management account, so do not put workloads there; they do apply to delegated administrator member accounts.
- Trusted access for RAM (`enable-sharing-with-aws-organization`) is separate and needed
  to share resources to OUs without invitations.

## Verify
- [ ] `FeatureSet` is `ALL`.
- [ ] `list-aws-service-access-for-organization` lists exactly the services you intend.
- [ ] Each security service has a delegated admin outside the management account.
- [ ] No pending handshakes remain.

## Checked

Checked 2026-10-27 against the AWS Organizations User Guide pages on enabling all features (overview and standard migration), integrating AWS services (trusted access), the services table and best practices for the management account, the IAM page on centralized root access, and the botocore organizations, guardduty, securityhub and ram models:
- Feature set values `ALL` and `CONSOLIDATED_BILLING`, one-way migration, request to invited accounts only, 90-day expiry, handshake action names and permissions.
- AWS's recommendation to enable and disable trusted access from the service, and what Organizations-side disabling does and does not do.
- Operations used in the examples exist (`enable-organization-admin-account` for GuardDuty and Security Hub, `register-delegated-administrator`, `put-resource-policy`, `enable-sharing-with-aws-organization`).
- The management-account best practice page recommends a root SCP denying `organizations:LeaveOrganization` and `account:CloseAccount`.
Removed: the list of service principals and the per-service CLI remarks, which the pages read do not give. The commands were not run.

Method: documentation only; no commands were run.
