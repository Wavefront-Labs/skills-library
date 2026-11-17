---
id: computing-software.cloud-infrastructure-engineering.aws.sts-role-chaining-session-duration-and-tags
name: sts-role-chaining-session-duration-and-tags
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sts, assume-role, role-chaining, session-duration, session-tags, transitive-tags, abac]
level: practitioner
status: docs-checked
description: "Handle STS session mechanics: MaxSessionDuration, the 1-hour role-chaining cap, passing session tags and transitive tags, and the trust policy permissions they require."
sources: ["https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html", "https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# STS role chaining, session duration and session tags

## 1. Session duration
- Role setting `MaxSessionDuration`: 1–12 hours (`update-role` accepts 3600 to 43200 seconds).
  `aws iam update-role --role-name deploy --max-session-duration 14400`
- Caller requests `--duration-seconds` from 900 up to that max (default 3600); asking for more fails.
- **Role chaining** (using role credentials to assume another role) limits the session to a maximum of
  **1 hour** regardless of `MaxSessionDuration`; requesting more than 3600 seconds in a chained call
  fails. Long jobs that chain must refresh, or assume the target role directly from the original
  identity (user/SSO/instance role).

## 2. Chaining in CLI config
```ini
[profile org-admin]
sso_session = corp
sso_account_id = 111111111111
sso_role_name = Admin

[profile prod-deploy]
role_arn = arn:aws:iam::222222222222:role/deploy
source_profile = org-admin
role_session_name = jo-deploy
duration_seconds = 3600
```
`prod-deploy` is a chained session (SSO role → deploy role) → max 1 hour.

## 3. Session tags
Pass key/value tags when assuming a role; they become `aws:PrincipalTag/<key>` in policy
evaluation for that session — the basis of ABAC without per-user roles.
```bash
aws sts assume-role --role-arn arn:aws:iam::<ACCOUNT_ID>:role/data-access --role-session-name jo \
  --tags Key=team,Value=finance Key=project,Value=ledger --transitive-tag-keys team
```
- Trust policy must allow **`sts:TagSession`** (in addition to `sts:AssumeRole`), optionally
  restricting values with `aws:RequestTag/team` and `aws:TagKeys`.
- **Transitive** tags persist through role chaining (by default STS does not pass tags to the next
  session); use them for identity attributes (team) that must survive chaining.
- Limits: at most 50 tags, keys up to 128 characters, values up to 256 characters, session policies
  up to 2,048 characters in total, and the session token must stay within its size limit
  (`SessionTokenUtilization` in the response shows usage; `PackedPolicySize` is deprecated).
- IdPs (SAML `https://aws.amazon.com/SAML/Attributes/PrincipalTag:team`, OIDC
  `https://aws.amazon.com/tags` claim) and Identity Center attributes pass tags automatically.

## Gotchas
- Session tags override the role's tags with the same key for that session, regardless of character case.
- A trust policy lacking `sts:TagSession` makes any tagged assume fail, which is confusing when
  the untagged call works.
- Credentials from `AssumeRole` can't call `GetFederationToken`/`GetSessionToken`.

## Verify
- [ ] `aws sts get-caller-identity --profile prod-deploy` works and expiry ≤ 1 h for chained profiles.
- [ ] The CloudTrail `AssumeRole` event shows the `principalTags` and `transitiveTagKeys` that were passed.
- [ ] A policy condition on `aws:PrincipalTag/team` allows finance data only for team=finance sessions.

## Checked

Checked 2026-10-27 against the IAM User Guide pages on terms and concepts (role chaining) and session tags, the AWS STS API reference for AssumeRole and AssumeRoleWithSAML, and the botocore iam and sts models:
- Role chaining limits the session to one hour and a longer `DurationSeconds` in a chained call fails.
- `update-role` MaxSessionDuration range 3600 to 43200; `AssumeRole` accepts `Tags` and `TransitiveTagKeys`.
- `sts:TagSession` is required in trust policies; session tag limits (50 tags, key 128, value 256, session policies 2,048 characters, token size); `PackedPolicySize` is deprecated in favour of `SessionTokenUtilization`; SAML attribute name and OIDC namespace for tags.
- Session tags override same-key role tags; CloudTrail shows `principalTags` and `transitiveTagKeys`.
Removed: the exact validation error text and the claim that transitive tags cannot be overridden, which were not found.

Method: documentation only; no commands were run.
