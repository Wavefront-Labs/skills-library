---
id: computing-software.cloud-infrastructure-engineering.aws.identity-center-delegated-admin-and-region
name: identity-center-delegated-admin-and-region
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, iam-identity-center, identity-center, sso, identity-center-delegated-admin, delegated-administrator, identity-center-region, home-region, organization-instance, account-instance, management-account, break-glass]
level: advanced
status: docs-checked
description: "Run IAM Identity Center from a delegated admin account, choose and live with its home Region, and plan for Regional outage and break-glass access to the management account."
sources: ["https://docs.aws.amazon.com/singlesignon/latest/userguide/delegated-admin.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/regions.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/identity-center-instances.html", "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_integrate_services.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Identity Center delegated administration and Region

**Goal:** the identity team administers Identity Center without logging into the
management account, the instance lives in a deliberately chosen Region, and nobody is locked
out when that Region or the IdP is down.

## 1. Delegate administration
From the management account, in the Region where Identity Center is enabled: Settings, Management tab,
Delegated administrator, Register account (this runs the Organizations `RegisterDelegatedAdministrator` API;
use the Identity Center service principal listed for it in the Organizations documentation).
Only one member account can be registered at a time, and registering or deregistering needs
management account credentials.
What the delegated admin can and cannot do: it can perform all Identity Center administrative tasks
(users and groups, permission sets, assignments, applications) except:
- enabling Identity Center or deleting its configuration,
- managing permission sets provisioned in the **management account**,
- registering or deregistering delegated administrators,
- enabling or disabling user access in the management account.
The delegated admin can edit group membership, so assign users directly (not groups) to permission
sets that grant management-account access.
- Name permission sets so the boundary is obvious (e.g. prefix `Mgmt-` for the ones only
  the management account may touch).

## 2. Home Region
- Everything you configure (directory configuration, permission sets, application instances,
  assignments, and identity store users and groups) is stored in the Region where you enable
  Identity Center. You can replicate the instance to additional Regions (`AddRegion` and
  `RemoveRegion` exist in the sso-admin API); check the Regions page for which applications
  support additional Regions.
- Choose the primary Region deliberately and read the Switching AWS Regions page before
  assuming a migration path.
- Prefer a Region that is enabled by default: an opt-in Region must be enabled in every
  account you manage through Identity Center, including new accounts.
- Account instances (standalone, per account) exist for app-only use cases; they cannot
  assign AWS account access. Do not confuse them with the organization instance.

## 3. Outage plan
Identity Center sign-in depends on its home Region and (for external IdPs) on the IdP.
- Keep a documented **break-glass** path: two IAM users (or root with hardware MFA) in the
  management account and in a security account, credentials in a safe, alarmed in
  CloudTrail (`ConsoleLogin` by those principals pages security).
- Existing role sessions keep working until expiry; long-running automation should use
  IAM roles, not Identity Center user sessions.
- Export assignments regularly (`list-account-assignments` per permission set and account)
  into version control so a rebuild is scripted.

## Gotchas
- Deregistering the delegated admin removes its ability to administer Identity Center and
  does not change existing permissions or assignments; automation running there loses access.
- Use an organization or multi-Region trail so Identity Center admin events are collected.
- Changing the identity source to Active Directory removes users, groups, memberships and
  assignments; changing between the Identity Center directory and external IdPs preserves them.
- If the identity source is Active Directory, the directory must reside in the delegated
  administrator account when you change the identity source.

## Verify
- [ ] From the delegated admin account, `aws sso-admin list-permission-sets` works and creating an assignment to a member account succeeds.
- [ ] Attempting to modify a permission set provisioned in the management account from the delegated admin is refused.
- [ ] Break-glass login tested this quarter and the alarm fired.
- [ ] Assignment export job output is current in the repo.

## Checked

Checked 2026-10-27 against the IAM Identity Center User Guide pages on delegated administration, registering and deregistering a member account, instance types, Region data storage, and considerations for changing the identity source, plus the botocore sso-admin model:
- One delegated administrator at a time; the list of tasks it cannot do; deregistering leaves permissions and assignments unchanged.
- Data is stored in the Region where Identity Center is enabled and can be replicated to additional Regions; opt-in Regions must be enabled in all managed accounts.
- Account instances give no multi-account permissions or access to AWS accounts through the portal.
- Identity source change behaviour.
The previous CLI example was replaced by the console path because the service principal string is not given on the pages read.

Method: documentation only; no commands were run.
