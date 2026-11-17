---
id: computing-software.cybersecurity-defensive.cloud-security.iam-identity-center-permission-sets
name: iam-identity-center-permission-sets
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [iam-least-privilege, iam-identity-center, permission-sets, aws-sso, multi-account, abac, session-duration]
level: practitioner
status: docs-checked
description: "Run human access to AWS through IAM Identity Center: organisation instance, permission set design, session duration, delegated admin and ABAC."
sources: ["https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsetsconcept.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/delegated-admin.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/howtosessionduration.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/abac.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IAM Identity Center permission sets

Goal: no IAM users for humans. Everyone signs in through the AWS access portal and gets short-lived
role credentials per account via Identity Center.

## Setup
- Use an **organization instance** (the best practice for production). It is deployed in the AWS Organizations management account and is the only instance type that manages access to AWS accounts; permission sets exist only for organization instances and need multi-account permissions enabled (on by default for new instances).
- **Delegated administrator**: register a member account (AWS Organizations must have at least one member account) so day-to-day administration does not need the management account. A permission set provisioned in the management account can be modified only by an Identity Center administrator in the management account; the delegated administrator cannot alter it. Use dedicated permission sets for the management account.
- If the identity source is external (SCIM), docs describe SCPs that block assigning users to groups through the Identity Store API and console, and that stop the delegated admin creating SCIM bearer tokens (allow temporarily for setup or token rotation). Keep identity source, SCIM token and session timeout administration in separate admin permission sets from those that create and assign permission sets.

## Permission set design
- A permission set can include AWS managed policies, customer managed policies, inline policies and AWS managed policies for job functions, and can use a managed or customer managed policy as a **permissions boundary**. Predefined permission sets (one AWS managed policy) are the quick way to a restrictive set.
- Give administrators additional, more restrictive permission sets and have them pick the most restrictive role in the access portal rather than AdministratorAccess. Each assigned permission set appears as a role in the portal.
- **Session duration** per permission set: default 1 hour, minimum 1 hour, maximum 12 hours; do not set it longer than the task needs. Changing it reprovisions the accounts that use the set. The access portal session is separate: default 8 hours, maximum 90 days.
- **ABAC** (attributes for access control) passes identity attributes as session tags so policies can use conditions, which needs fewer permission sets.
- Relay state can send users to a specific console page (see the session duration page).

## Assignments
Assign **groups** to accounts with a permission set; assign individual users only for exceptions. Review assignments periodically per account and group.

## Gotchas
- Editing a permission set reprovisions it to the accounts that use it.
- Keep access to the management account to as few people as possible; consider temporary elevated access.

## Verify
- No standing IAM users with console passwords except a documented break-glass path.
- Human activity comes from federated role sessions, and assignments match what is intended.

## Checked
Checked 2026-11-09 against the IAM Identity Center User Guide pages in `sources` (instance types, permission set contents and boundary, session duration limits, delegated administrator guidance and SCP examples, ABAC). Removed unconfirmed claims: example permission set names, home Region advice, specific SCP protection of `AWSReservedSSO` roles, Terraform and TEAM tooling, CloudTrail event names, the credential report command and IdP-specific behaviour.
Method: documentation only; no commands were run.
