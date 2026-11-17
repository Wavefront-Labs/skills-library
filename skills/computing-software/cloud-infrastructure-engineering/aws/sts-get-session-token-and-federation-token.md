---
id: computing-software.cloud-infrastructure-engineering.aws.sts-get-session-token-and-federation-token
name: sts-get-session-token-and-federation-token
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sts, get-session-token, get-federation-token, mfa-cli, temporary-credentials]
level: advanced
status: docs-checked
description: "Use GetSessionToken for MFA-backed CLI sessions and GetFederationToken for broker-issued federated users, with their duration limits and API restrictions."
sources: ["https://docs.aws.amazon.com/STS/latest/APIReference/API_GetSessionToken.html", "https://docs.aws.amazon.com/STS/latest/APIReference/API_GetFederationToken.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_request.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_control-access_disable-perms.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_enable-console-custom-url.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GetSessionToken and GetFederationToken

## 1. GetSessionToken: MFA session for an IAM user
```bash
creds=$(aws sts get-session-token --serial-number arn:aws:iam::<ACCOUNT_ID>:mfa/<user> \
  --token-code 123456 --duration-seconds 43200 --query Credentials --output json)
export AWS_ACCESS_KEY_ID=$(jq -r .AccessKeyId <<<"$creds")
export AWS_SECRET_ACCESS_KEY=$(jq -r .SecretAccessKey <<<"$creds")
export AWS_SESSION_TOKEN=$(jq -r .SessionToken <<<"$creds")
```
- Duration 900 s to 129,600 s (36 h) for IAM users; root is capped at 3,600 s.
- Same permissions as the IAM user that made the call.
- Cannot call IAM APIs unless MFA was included; cannot call STS except `AssumeRole` and `GetCallerIdentity`.
- Must be called with long-term user keys, not role credentials.

## 2. GetFederationToken: custom identity broker
```bash
aws sts get-federation-token --name alice --duration-seconds 3600 \
  --policy-arns arn=arn:aws:iam::aws:policy/ReadOnlyAccess \
  --policy file://session-policy.json
```
- Called by an IAM user (the broker). Effective permissions = broker user's policies ∩ passed
  session policies. With no session policy the federated user gets **no** permissions.
- Principal appears as `arn:aws:sts::<ACCOUNT_ID>:federated-user/alice` in CloudTrail.
- Duration up to 36 h (root 1 h). No IAM or STS calls except `GetCallerIdentity`.
- Console access: exchange the creds at `https://signin.aws.amazon.com/federation?Action=getSigninToken`.

## 3. When to use something else
- Humans: IAM Identity Center (`aws sso login`) beats both.
- Cross-account or role-based: `AssumeRole` with `mfa_serial` in the profile.
- GetFederationToken remains useful only where a legacy broker cannot use roles.

## Gotchas
- Permissions are evaluated on every request, so you cut off these credentials by changing the IAM user's permissions
  (or denying the principal ARN with `aws:PrincipalArn`); allow a few minutes for policy changes. You cannot change the
  permissions of credentials created while signed in as the root user, so never call these operations as root.
- Session policy limit: the plaintext of inline and managed session policies combined cannot exceed 2,048
  characters; up to 10 managed policy ARNs.

## Verify
- [ ] `aws sts get-caller-identity` with the exported creds shows the user (or federated-user) ARN.
- [ ] An MFA-gated action succeeds only with the session-token credentials.

## Checked

Checked 2026-10-27 against the AWS STS API reference pages for GetSessionToken and GetFederationToken, the IAM User Guide pages on requesting temporary credentials, disabling permissions for temporary credentials and enabling custom identity broker console access, and the botocore sts model:
- Duration range 900 to 129,600 seconds for IAM users (default 43,200), root capped at 3,600; IAM calls need MFA information and only AssumeRole and GetCallerIdentity are allowed as STS calls (GetSessionToken); only GetCallerIdentity for GetFederationToken; no session policy means no permissions; session policy limit 2,048 characters and 10 managed ARNs.
- The `federated-user` ARN form and the `https://signin.aws.amazon.com/federation` `getSigninToken` action are documented.
- Parameters shown in the CLI examples exist in the model (`Name` is required for GetFederationToken).
Removed: the `aws:MultiFactorAuthPresent` sentence and the key-deactivation advice, which the pages do not state.

Method: documentation only; no commands were run.
