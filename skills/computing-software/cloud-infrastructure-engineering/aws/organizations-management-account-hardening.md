---
id: computing-software.cloud-infrastructure-engineering.aws.organizations-management-account-hardening
name: organizations-management-account-hardening
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, organizations, payer-account-hardening, management-account, delegated-administrator, multi-account]
level: practitioner
status: docs-checked
description: "Harden the Organizations management (payer) account: no workloads, delegated admins for security services, tight access, root lockdown and alternate contacts."
sources: ["https://docs.aws.amazon.com/organizations/latest/userguide/orgs_best-practices_mgmt-acct.html", "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_integrate_services_list.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Management account hardening

**Why:** SCPs and RCPs do not apply to the management account, and it can change every account's
guardrails. Treat it as the most privileged account you own.

## 1. Keep it empty
- No application workloads, no CI pipelines, no developer access.
- Only org-level functions: Organizations, billing/CUR, Control Tower home, Identity Center (or
  delegate it), account vending.

## 2. Delegate everything that allows it
```bash
aws organizations register-delegated-administrator --account-id <AUDIT_ACCOUNT_ID> --service-principal <SERVICE_PRINCIPAL>
aws organizations list-delegated-administrators
```
Look up each service's principal in the "AWS services that you can use with AWS Organizations" table, which also shows
which services support delegated administration (for example Service Catalog and CloudFormation StackSets are named
on the best-practices page, and IAM Identity Center supports it). Many services have their own
enable-organization-admin-account call. Day-to-day security work then happens outside the payer.

## 3. Prevent departures and closures
The best-practices page recommends a root-level SCP that denies `organizations:LeaveOrganization` and
`account:CloseAccount`. Organizations created in the console after 10 July 2026 receive it automatically; organizations
created earlier, or through the CLI, SDKs or CloudFormation, need it attached manually.

## 4. Access
- Root: MFA (up to eight devices can be registered; keep more than one), no access keys, and enable
  centralized root access to remove member-account root credentials.
- Humans reach it only through an Identity Center permission set assigned to a small break-glass group,
  short session duration, plus one break-glass IAM user stored offline.
- Alarms on any console sign-in or root activity in this account.

## 5. Account hygiene
```bash
aws account put-alternate-contact --alternate-contact-type SECURITY \
  --email-address secops@example.com --name "Security" --phone-number "+1-555-0100" --title "SecOps"
```
Set BILLING and OPERATIONS too; use distribution lists, not a person's mailbox.

## Verify
- [ ] `aws ec2 describe-instances` and Lambda lists are empty in all Regions of the management account.
- [ ] Security services show the audit account as delegated admin.
- [ ] Only the break-glass group has an assignment to the management account.
- [ ] A root SCP denying `organizations:LeaveOrganization` and `account:CloseAccount` is attached.

## Checked

Checked 2026-10-27 against the AWS Organizations User Guide page "Best practices for the management account", the services table, the IAM User Guide pages on MFA and the root user, and the botocore organizations and account models:
- SCPs do not restrict the management account; keep workloads out of it; limit and review access; delegate outside it.
- The recommended root SCP denying `organizations:LeaveOrganization` and `account:CloseAccount`, and the date after which console-created organizations receive it.
- Root users and IAM users can register up to eight MFA devices.
- `put-alternate-contact` takes `--name`, `--title`, `--email-address`, `--phone-number` and a type of `BILLING`, `OPERATIONS` or `SECURITY`.
Replaced service principal strings with a placeholder because the pages read do not list them. The commands were not run.

Method: documentation only; no commands were run.
