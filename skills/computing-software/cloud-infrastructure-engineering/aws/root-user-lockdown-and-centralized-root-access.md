---
id: computing-software.cloud-infrastructure-engineering.aws.root-user-lockdown-and-centralized-root-access
name: root-user-lockdown-and-centralized-root-access
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, iam, root-user-mfa, centralized-root-access, root-credentials, organizations, account-security, break-glass]
level: practitioner
status: docs-checked
description: "Lock down the AWS root user: MFA, no access keys, centralized root access for member accounts, root-only tasks via AssumeRoot, and alerts on any root sign-in."
sources: ["https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-enable-root-access.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa.html", "https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRoot.html", "https://docs.aws.amazon.com/securityhub/latest/userguide/iam-controls.html", "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-service-event-cloudtrail.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Root user lockdown

**Goal:** no account in the organization has usable long-term root credentials except the
management account, which has hardware MFA held under dual control; root-only tasks in
member accounts are performed via short-lived `AssumeRoot` sessions; any root sign-in
pages someone.

## 1. Management account (and any standalone account)
1. Sign in as root once, set a strong unique password stored in a vault with two
   custodians.
2. Register **two** MFA devices (up to 8 allowed): FIDO2 security keys kept in separate
   safes. Passkeys are fine; virtual MFA on one phone is a single point of failure.
3. Delete any root access keys: IAM console, Security credentials, or check with
   `aws iam get-account-summary --query 'SummaryMap.AccountAccessKeysPresent'` (must be 0).
4. Set the account **alternate contacts** (security, billing, operations) to distribution
   lists, and the root email to a group mailbox you control, not a person.
5. Do not create workloads in the management account.

## 2. Member accounts: centralized root access
Organizations can remove root credentials from member accounts entirely. From the management
account (or the IAM delegated administrator):
```bash
aws organizations enable-aws-service-access --service-principal iam.amazonaws.com
aws iam enable-organizations-root-credentials-management
aws iam enable-organizations-root-sessions
aws iam list-organizations-features
```
- **Root credentials management:** delete the root password, access keys, signing certificates and
  MFA in member accounts (console, or script via `AssumeRoot` with the
  `IAMDeleteRootUserCredentials` task policy). New accounts created in Organizations have no root
  credentials by default; member accounts cannot sign in as root or recover the password unless
  password recovery is allowed (the "Allow password recovery" privileged task).
- **Root sessions:** run privileged root-only tasks without credentials:
```bash
aws sts assume-root --target-principal 444455556666 \
  --task-policy-arn arn=arn:aws:iam::aws:policy/root-task/S3UnlockBucketPolicy \
  --duration-seconds 900
```
Task policies available include `IAMAuditRootUserCredentials`,
`IAMCreateRootUserPassword` (recovery), `IAMDeleteRootUserCredentials`,
`S3UnlockBucketPolicy` (fix a bucket policy that denies everyone) and
`SQSUnlockQueuePolicy`. Sessions last at most 900 seconds (the default), `AssumeRoot` must go to a
Regional STS endpoint, and it must be called with management account or IAM delegated administrator
credentials, not root credentials.

## 3. Root-only tasks to know
Things only root can do (so you plan for them), per the IAM page "Tasks that require root user
credentials": for standalone accounts, change the root email, password or access keys, close or reopen the
account; restore IAM permissions if the only administrator revoked their own; activate IAM access to
Billing; some billing tasks; unlock an S3 bucket or SQS queue policy that denies all principals (for member
accounts use `AssumeRoot`); configure S3 MFA delete; register as an EC2 Reserved Instance Marketplace seller;
sign up for GovCloud. In an organization, the management account and delegated admins can close member
accounts and update their root email, name and contacts without the root user.

## 4. Prevent and detect
- SCP on all OUs except the management account (SCPs never apply to the management
  account):
```json
{"Effect": "Deny", "Action": "*", "Resource": "*",
 "Condition": {"ArnLike": {"aws:PrincipalArn": "arn:aws:iam::*:root"}}}
```
  The key's root-user value limits only the root user; AWS recommends ARN condition operators.
- EventBridge rule in each account (or an org trail with a metric filter):
```json
{"detail-type": ["AWS Console Signin via CloudTrail"],
 "detail": {"userIdentity": {"type": ["Root"]}}}
```
  target SNS/PagerDuty. Security Hub controls `IAM.9` (MFA for root) and `IAM.6` (hardware MFA for root)
  cover MFA; `IAM.4` checks that no root access key exists.
- Credential report column `root` row: `password_last_used`, `mfa_active`,
  `access_key_1_active` for audits.

## Gotchas
- Losing root MFA on the management account requires AWS account recovery (email and
  phone verification); keep the phone number on the account current.
- After you delete member root credentials, recovery needs the "Allow password recovery" privileged
  task and someone with access to that account's root email inbox; make sure the address is still deliverable.
- SCP root deny does not stop the management account root; protect it with physical
  controls and alerts.

## Verify
- [ ] `list-organizations-features` shows `RootCredentialsManagement` and `RootSessions` enabled.
- [ ] Security Hub IAM.4/IAM.6/IAM.9 pass in every account; credential report shows no root keys anywhere.
- [ ] A test `assume-root` with `IAMAuditRootUserCredentials` succeeds against a member account and appears in CloudTrail.
- [ ] A root console sign-in in a sandbox triggers the alert within minutes.

## Checked

Checked 2026-10-27 against the IAM User Guide pages on the root user (tasks that require root credentials), centralizing root access and MFA, the AWS STS API reference for AssumeRoot, the EventBridge page on CloudTrail events, the Security Hub IAM controls page and the botocore iam and sts models:
- `enable-organizations-root-credentials-management`, `enable-organizations-root-sessions` and `list-organizations-features` exist, with features `RootCredentialsManagement` and `RootSessions`; the delegated administrator service principal for IAM is `iam.amazonaws.com`.
- `AssumeRoot`: task policies (`IAMAuditRootUserCredentials`, `IAMCreateRootUserPassword`, `IAMDeleteRootUserCredentials`, `S3UnlockBucketPolicy`, `SQSUnlockQueuePolicy`), duration 0 to 900 seconds, Regional endpoint required, not callable with root credentials.
- Root and IAM users can register up to eight MFA devices; the root-only task list; Security Hub IAM.4, IAM.6 and IAM.9 titles; the detail-type `AWS Console Signin via CloudTrail`.
- `aws:PrincipalArn` with the root ARN limits only the root user.
Removed: the "late 2024" date, the CIS control number, the support plan item and the sentence that AssumeRoot sessions bypass the SCP, none of which the pages confirm. The commands were not run.

Method: documentation only; no commands were run.
