---
id: computing-software.cloud-infrastructure-engineering.aws.identity-center-cloudtrail-audit
name: identity-center-cloudtrail-audit
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, identity-center, sso-cloudtrail-audit, signin-events, cloudtrail, aws-sso]
level: advanced
status: docs-checked
description: "Audit IAM Identity Center sign-ins, role credential requests and assignment changes in CloudTrail, and trace a member-account action back to the user."
sources: ["https://docs.aws.amazon.com/singlesignon/latest/userguide/logging-using-cloudtrail.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/sso-info-in-cloudtrail.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/understanding-sign-in-events.html", "https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-service-event-cloudtrail.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Auditing Identity Center in CloudTrail

Identity Center API calls are recorded as CloudTrail events like other AWS services. Use an organization trail or a multi-Region trail so events are not missed when you search in the wrong Region.

## 1. Event map
| What | eventSource | eventName |
|---|---|---|
| User sign-in | AWS Sign-In (see the CloudTrail events table in the user guide) | `UserAuthentication`, `CredentialChallenge`, `CredentialVerification` |
| Portal activity | `sso.amazonaws.com` | `Authenticate`, `Federate` (no public API), `ListAccounts`, `GetRoleCredentials` |
| Admin changes | `sso.amazonaws.com` | `CreateAccountAssignment`, `DeleteAccountAssignment`, `CreatePermissionSet`, `AttachManagedPolicyToPermissionSet`, `PutInlinePolicyToPermissionSet`, `ProvisionPermissionSet` |
| Directory changes | `identitystore.amazonaws.com`, `sso-directory.amazonaws.com` | `CreateUser`, `CreateGroupMembership`, `DeleteGroupMembership` |
`CredentialChallenge` and `CredentialVerification` are logged for Identity Center users and AD sources, not for an external IdP. They carry `userIdentity.additionalEventData.CredentialType` (`PASSWORD`, `TOTP`, `WEBAUTHN`, `EXTERNAL_IDP`, `RESYNC_TOTP` or `EMAIL_OTP`) and say whether the credential succeeded or failed; `AuthWorkflowID` correlates all events of one sign-in. A `UserAuthentication` event is logged only after every required challenge is solved.

## 2. Following a user into a member account
In the member account the user works through an Identity Center managed role whose name starts with `AWSReservedSSO_`.
Inspect one real event in your own trail for the exact `userIdentity.arn` format, then adapt the pattern below.
Query across accounts with the org trail:
```sql
SELECT eventtime, recipientaccountid, eventsource, eventname
FROM cloudtrail_logs
WHERE useridentity.arn LIKE '%AWSReservedSSO_%/<USERNAME>'
  AND eventtime > '2026-10-01'
ORDER BY eventtime;
```

## 3. Alerts worth having
- `CreateAccountAssignment` or `AttachManagedPolicyToPermissionSet` outside the IaC pipeline role.
- Bursts of `CredentialVerification` failures for one user (password spraying).
- MFA device and MFA settings changes (Identity Store events).
EventBridge rule pattern (CloudTrail API calls arrive with this detail-type): `{"detail-type":["AWS API Call via CloudTrail"],"detail":{"eventSource":["sso.amazonaws.com"],"eventName":["CreateAccountAssignment"]}}`.

## Gotchas
- Looking in the wrong Region is a common "no events" cause; confirm which Region the instance is enabled in.
- With an external IdP, the password step happens at the IdP; check its logs for authentication failures.

## Verify
- [ ] A test sign-in shows up as a `UserAuthentication` event in CloudTrail.
- [ ] The Athena query links a member-account action to the human username.

## Checked

Checked 2026-10-27 against the IAM Identity Center User Guide pages Logging IAM Identity Center API calls with AWS CloudTrail, IAM Identity Center information in CloudTrail, Understanding sign-in events, the AWS STS AssumeRoleWithSAML reference and the EventBridge page on events delivered via CloudTrail:
- Sign-in event names, `CredentialType` values, `AuthWorkflowID` and the rule that challenge events exist only for Identity Center and AD sources are as listed on the sign-in events page.
- Event source names `sso.amazonaws.com`, `sso-directory.amazonaws.com` and `identitystore.amazonaws.com`, and the event names in the table, are listed on the CloudTrail information page (`Authenticate` and `Federate` have no public API).
- Role names starting with `AWSReservedSSO_` are Identity Center managed roles (STS API reference).
- EventBridge delivers CloudTrail API calls with detail-type `AWS API Call via CloudTrail`.
The sign-in event source name is printed inconsistently in the documentation, so it is not stated here. `PutInlinePolicyToPermissionSet` and `ProvisionPermissionSet` are operations in the botocore sso-admin model.

Method: documentation only; no commands were run.
