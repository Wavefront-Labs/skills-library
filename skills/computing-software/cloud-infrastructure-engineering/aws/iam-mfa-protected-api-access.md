---
id: computing-software.cloud-infrastructure-engineering.aws.iam-mfa-protected-api-access
name: iam-mfa-protected-api-access
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, iam, mfa-protected-api, multifactorauthpresent, mfa, iam-conditions]
level: advanced
status: docs-checked
description: "Require MFA for sensitive IAM API calls with aws:MultiFactorAuthPresent and MultiFactorAuthAge, using BoolIfExists for denies and MFA-gated role trust."
sources: ["https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa_configure-api-require.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_examples_aws_my-sec-creds-self-manage.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html", "https://docs.aws.amazon.com/sdkref/latest/guide/feature-assume-role-credentials.html", "https://github.com/boto/botocore/blob/develop/botocore/data/iam/2010-05-08/service-2.json"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MFA-protected API access

**Goal:** sensitive actions only succeed when the caller's credentials were obtained with MFA.

## 1. Know when the key exists
| Credential | `aws:MultiFactorAuthPresent` |
|---|---|
| Long-term access keys (IAM user or root) | **absent** |
| Temporary credentials from `GetSessionToken` called with `--serial-number` + `--token-code` | `true` on later requests (and `aws:MultiFactorAuthAge` is present) |
| `AssumeRole` called with `--serial-number` + `--token-code` | `true` when the role's **trust policy** is evaluated; the role session credentials do **not** carry MFA information, so individual API calls in the session cannot be checked for MFA |
| `AssumeRoleWithSAML` / `AssumeRoleWithWebIdentity` / `GetFederationToken` | absent (MFA happens at the external provider, or is not tied to a user) |
MFA protection works only with temporary credentials from `AssumeRole` or `GetSessionToken`, and not with root
user credentials or U2F security keys. The absence case drives every design choice below.

## 2. Allow-with-MFA (safe pattern)
```json
{"Effect":"Allow","Action":["ec2:StopInstances","ec2:TerminateInstances"],"Resource":"*",
 "Condition":{"Bool":{"aws:MultiFactorAuthPresent":"true"},
              "NumericLessThan":{"aws:MultiFactorAuthAge":"3600"}}}
```
`Bool ... true` does not match when the key is missing, so the allow does not apply to long-term keys.
`aws:MultiFactorAuthAge` is the seconds since MFA authentication and is also absent without MFA. Users need
to sign out and in again for a new policy of this kind to take effect in the console.

## 3. Deny-without-MFA (use BoolIfExists)
This is the pattern in the AWS self-service credentials example:
```json
{"Effect":"Deny","NotAction":["iam:CreateVirtualMFADevice","iam:EnableMFADevice","iam:GetUser",
  "iam:GetMFADevice","iam:ListMFADevices","iam:ListVirtualMFADevices","iam:ResyncMFADevice","sts:GetSessionToken"],
 "Resource":"*","Condition":{"BoolIfExists":{"aws:MultiFactorAuthPresent":"false"}}}
```
`"Bool": {"...": "false"}` in a Deny is not recommended: it would NOT match long-term keys (key absent), so
access keys would bypass the deny. `BoolIfExists` treats a missing key as matching. The NotAction list lets a
user enrol a device; that statement denies everything else, so other statements must grant the permissions the
user actually needs. Programmatic callers must call `GetSessionToken` with MFA first.

## 4. MFA on role assumption
Trust policy on the privileged role (the AWS example uses the trusted account as principal):
```json
{"Effect":"Allow","Principal":{"AWS":"arn:aws:iam::<ACCOUNT_ID>:root"},"Action":"sts:AssumeRole",
 "Condition":{"Bool":{"aws:MultiFactorAuthPresent":"true"}}}
```
CLI profile:
```ini
[profile admin]
role_arn = arn:aws:iam::<ACCOUNT_ID>:role/Admin
source_profile = base
mfa_serial = arn:aws:iam::<ACCOUNT_ID>:mfa/<user>
duration_seconds = 3600
```
`mfa_serial` is required when the role's trust policy requires MFA; its value is a hardware serial number or a
virtual MFA device ARN. `duration_seconds` ranges from 900 up to the role's maximum session duration
(default 3600); role chaining limits a session to one hour.

## Gotchas
- Federated (SAML/OIDC) sessions never carry the key; enforce MFA at the identity provider instead, or such
  users are locked out of policies that require it.
- Because `AssumeRole` credentials carry no MFA information, enforce MFA at assume time (trust policy). For
  resource-based policies with an MFA condition, callers must use `GetSessionToken` credentials.
- MFA conditions for cross-account roles rely on the trusted account's own controls: any identity there that can
  create virtual MFA devices can construct an MFA claim.

## Verify
- [ ] With access keys only, a protected call returns `AccessDenied`; after `get-session-token` with a code it succeeds.
- [ ] `aws iam simulate-principal-policy --policy-source-arn <USER_ARN> --action-names ec2:TerminateInstances --context-entries ContextKeyName=aws:MultiFactorAuthPresent,ContextKeyValues=false,ContextKeyType=boolean` shows `explicitDeny` for the deny statement above.

## Checked
Checked 2026-10-24 against the IAM User Guide pages "Secure API access with MFA" and the self-service
credentials example policy, the global condition keys page, the AWS SDKs and Tools assume-role provider page and
the botocore IAM model. Corrected: the old table said `AssumeRole` with an MFA code makes the key `true`
for the resulting session; the guide says AssumeRole credentials do not include MFA information in the
context (the trust policy sees it at assume time); the old `NotAction` list omitted `iam:GetMFADevice`, which the
AWS example includes; and the console-sign-in row, `~/.aws/cli/cache` path and the role-chaining advice were not
supported and were removed or reworded. Confirmed: key absent for long-term credentials, `Bool` vs
`BoolIfExists` behaviour, `aws:MultiFactorAuthAge`, no MFA for root or U2F, federation limitation, `mfa_serial`,
`role_arn`, `source_profile`, `duration_seconds` settings, and the simulator `--context-entries` shape.
Method: documentation only; no commands were run.
