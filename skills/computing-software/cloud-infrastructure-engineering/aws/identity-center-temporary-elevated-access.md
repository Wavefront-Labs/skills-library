---
id: computing-software.cloud-infrastructure-engineering.aws.identity-center-temporary-elevated-access
name: identity-center-temporary-elevated-access
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, identity-center, temporary-elevated-access, just-in-time-access, team, permission-sets, approval-workflow]
level: advanced
status: docs-checked
description: "Give engineers time-bound, approved admin access in IAM Identity Center with TEAM or an IdP-driven JIT flow: eligibility, approvals, auto-expiry and session audit."
sources: ["https://docs.aws.amazon.com/singlesignon/latest/userguide/temporary-elevated-access.html", "https://aws-samples.github.io/iam-identity-center-team/", "https://docs.aws.amazon.com/singlesignon/latest/userguide/useraccess.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/howtosessionduration.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/revoke-user-permissions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Temporary elevated access with IAM Identity Center

**Goal:** nobody holds standing admin permission sets in production. Engineers request
elevation for a reason and a duration, an approver accepts, Identity Center creates the
account assignment, and it is removed automatically at expiry, with an audit trail.

## 1. Mechanism underneath every option
All JIT tools do the same two calls with the Identity Center admin API:
```bash
aws sso-admin create-account-assignment --instance-arn arn:aws:sso:::instance/ssoins-xxxx \
  --target-id 111122223333 --target-type AWS_ACCOUNT \
  --permission-set-arn arn:aws:sso:::permissionSet/ssoins-xxxx/ps-admin \
  --principal-type USER --principal-id <identity-store-user-id>
# ... later
aws sso-admin delete-account-assignment  (same arguments)
```
Assignment provisioning is asynchronous: poll
`describe-account-assignment-creation-status`. Deleting an assignment stops **new**
sessions; existing role sessions last until their permission-set session duration
(default 1 h, max 12 h). Set elevated permission sets to 1 h.

## 2. Options
- **TEAM** (Temporary Elevated Access Management, AWS open-source solution, MIT-0): a custom
  application deployed with AWS Amplify, using Amazon Cognito group-based authorization and SAML
  integration with Identity Center. Users request access to an account for a period, approvers
  review, access is removed automatically at expiry, and session logs support audit. Read its
  security and resiliency considerations before deploying.
- **Partner solutions**: the Identity Center user guide lists solutions validated by AWS Security
  Competency: Apono, CyberArk Secure Cloud Access, Okta Access Requests and Tenable. Some
  IdP-native tools add the user to an IdP group that is synced to an Identity Center group with a
  pre-made assignment; group-sync latency and revoke timing then depend on the IdP.
- **Home-grown**: an EventBridge/Step Functions workflow calling the two APIs above with a
  Slack approval. Fine for small orgs; you own audit and edge cases.

## 3. TEAM deployment outline
1. Follow the TEAM documentation's deployment steps, including its prerequisites for the
   account it runs in and for session logging.
2. Define eligibility and approvers as the TEAM documentation describes (for example a group
   allowed to request a permission set in an account for a limited time, with named approvers).
3. Run the end-to-end example scenario from the TEAM docs before relying on it.

## 4. Policy and guardrails
- Add an inline policy to elevated sets denying the ability to change Identity Center itself
  (`sso:*`, `identitystore:*`) and to disable logging.
- If you reference permission sets in resource policies, EKS cluster config maps or KMS key
  policies, read the user guide page on referencing permission sets before choosing a JIT
  solution.
- Break-glass: keep one documented emergency path that does not depend on the JIT tool
  (the user guide recommends setting up emergency access to the console).
- Review standing assignments monthly:
  `aws sso-admin list-account-assignments-for-principal`.

## Gotchas
- Deleting the assignment does not cut an active console session; plan incident-grade revocation
  separately; the Identity Center user guide page "Revoke user access" describes the SCP-based procedure.
- Identity Center data lives in the Region where it is enabled; automation must call that Region.
- If the requester's group is managed by an external IdP, manual group edits in Identity Center
  can be overwritten at the next synchronization.

## Verify
- [ ] No user or group holds a standing admin permission set in prod accounts (script the assignment listing).
- [ ] A request flows request, approve, assignment created, access works, auto-revoked at expiry.
- [ ] CloudTrail shows the user's actions under the elevated role session, attributable to the requester.
- [ ] Break-glass path tested this quarter.

## Checked

Checked 2026-10-27 against the IAM Identity Center User Guide page on temporary elevated access, the TEAM project site, the botocore sso-admin model, and the sessions pages:
- Validated partner solutions listed on the user guide page; the note about resource policies, EKS and KMS.
- TEAM is open source under MIT-0, built on Amplify, Cognito and SAML with Identity Center, with automatic removal and session logs.
- `create-account-assignment`, `delete-account-assignment` and `describe-account-assignment-creation-status` exist; ending an assignment does not end active role sessions (permission set duration 1 to 12 hours, default 1 hour).
Removed because no page confirmed them: TEAM internals (Step Functions, DynamoDB, CloudTrail Lake, deploy script and its parameters, notification defaults), non-validated vendor names, and the `aws:SourceIdentity` and TokenIssueTime statements for Identity Center roles.

Method: documentation only; no commands were run.
