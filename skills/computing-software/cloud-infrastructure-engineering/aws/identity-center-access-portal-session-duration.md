---
id: computing-software.cloud-infrastructure-engineering.aws.identity-center-access-portal-session-duration
name: identity-center-access-portal-session-duration
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, identity-center, portal-session-duration, access-portal, session-duration, aws-sso]
level: practitioner
status: docs-checked
description: "Set IAM Identity Center access portal session duration separately from permission-set session duration, and revoke active portal sessions."
sources: ["https://docs.aws.amazon.com/singlesignon/latest/userguide/configure-user-session.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/user-interactive-sessions.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/howtosessionduration.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/end-active-sessions.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/user-session-duration-prereqs-considerations.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/howtochangeURL.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/revoke-user-permissions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Identity Center access portal session settings

## 1. Two different clocks
| Setting | Where | Range | Controls |
|---|---|---|---|
| Access portal session duration (user interactive sessions) | Settings, Authentication, Session duration | 15 minutes to 90 days (default 8 h) | how long a user stays signed in to the portal and AWS managed applications without re-authenticating |
| Permission set session duration | per permission set | 1 to 12 h (default 1 h) | lifetime of the role credentials for one account/role |
A user with an 8 h portal session and a 1 h permission set can fetch fresh role credentials without signing in again until the portal session ends. Changes to the portal duration apply only to new sessions. With an external IdP that sends `SessionNotOnOrAfter`, the shorter of the two applies; with AWS Managed Microsoft AD or AD Connector the Kerberos ticket lifetime (10 hours by default) also caps it.

```bash
aws sso-admin update-permission-set --instance-arn <INSTANCE_ARN> \
  --permission-set-arn <PS_ARN> --session-duration PT4H
aws sso-admin provision-permission-set --instance-arn <INSTANCE_ARN> --permission-set-arn <PS_ARN> --target-type ALL_PROVISIONED_ACCOUNTS
```

## 2. Choosing values
- Admin permission sets: short (1 h). Read-only: longer is fine.
- Portal: match your IdP session policy; with an external IdP, the IdP session also has to be valid.

## 3. Ending sessions
Console, Users, user, Active sessions tab, select sessions, End sessions. Ending a portal session
does **not** end active IAM role sessions in the console or CLI: those last until their permission-set duration ends. For an immediate cut-off follow the user guide's "Revoke user access" procedure: a deny-all SCP that names the user ID, removal of all assignments, deleting the active portal session, disabling the user, and leaving the deny in place for at least 12 hours so issued role sessions expire.

## 4. Portal URL
The access portal URL `https://d-xxxxxxxxxx.awsapps.com/start` can be customised once to a
subdomain; it cannot be edited or reversed afterwards, so pick a stable name.

## Verify
- [ ] Signing in, waiting past the permission-set duration, and running an AWS CLI call triggers a silent refresh, not a new login.
- [ ] After ending a session, the portal asks the user to sign in again.

## Checked

Checked 2026-10-27 against the IAM Identity Center User Guide pages on user interactive sessions, session duration for AWS accounts, ending active sessions, session duration considerations, and customizing the access portal URL:
- Interactive session default 8 hours, range 15 minutes to 90 days; permission set default 1 hour, range 1 to 12 hours.
- Ending an active portal session does not end IAM role sessions in the console or CLI.
- The portal URL customization is one-time and cannot be reversed.
- `update-permission-set` accepts `SessionDuration` as an ISO 8601 duration and `provision-permission-set` accepts target type `ALL_PROVISIONED_ACCOUNTS` (botocore sso-admin model).
- The user guide page "Revoke user access" gives the cut-off procedure above (https://docs.aws.amazon.com/singlesignon/latest/userguide/revoke-user-permissions.html).
The earlier statement about portal sign-out timing and a role-session revocation trick for Identity Center roles was not found in the documentation and was removed.

Method: documentation only; no commands were run.
