---
id: computing-software.cloud-infrastructure-engineering.minio.openid-identity
name: openid-identity
category: computing-software
field: cloud-infrastructure-engineering
product: minio
tags: [minio, openid-identity, oidc, mc-idp-openid-add, assume-role-with-web-identity, role-policy, claim-name, jwt, sts]
level: advanced
status: docs-checked
description: "Configure MinIO OpenID Connect identity with mc idp openid add, JWT claim or role_policy authorisation and AssumeRoleWithWebIdentity temporary credentials."
sources: ["https://github.com/minio/docs/blob/main/source/operations/external-iam/configure-openid-external-identity-management.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MinIO OpenID Connect identity management

MinIO supports only the OIDC **Authorization Code Flow** for JWT claim-based authentication.

## Configure
```
mc idp openid add ALIAS \
  client_id=minio-oidc-client-id \
  client_secret=minio-oidc-client-secret \
  config_url="https://openid-provider.example.net/REALM/.well-known/openid-configuration" \
  claim_name="minio-policies" \
  scopes="openid,groups"
```
- With `claim_name`, policies come from the claim in the JWT.
- Alternatively `role_policy="readOnly"` gives all authenticated users one built-in policy and enables `RoleArn`-based functionality.
The server restarts as part of applying the configuration; read its logs to confirm persistence. For `role_policy` configurations the output includes an ARN for the STS API.

## Getting S3 credentials
Clients must sign requests with SigV4 using an access key and secret key, so an application logs in to the OIDC provider, gets the JWT, and calls the STS endpoint:
```
POST https://minio.example.net?Action=AssumeRoleWithWebIdentity
&WebIdentityToken=TOKEN&Version=2011-06-15&DurationSeconds=86400&Policy=Policy
```
- `DurationSeconds` sets credential lifetime (86400 is 24 hours in the example).
- `Policy` is an optional inline URL-encoded JSON policy that further restricts permissions; omit to use the policy from the claim.
- Optional `RoleArn` selects a single-policy OIDC configuration.
The XML response contains access key, secret key, session token and expiration. MinIO ships an example Go app (`web-identity.go`).

Policy details: `computing-software.cloud-infrastructure-engineering.minio.policy-based-access-control`.

## Checked
2026-11-03. Confirmed against the MinIO docs source: Configure OpenID page (configure-openid-external-identity-management.rst). Removed: the claim that external identity management disables the internal IDP (not on this page).
Method: documentation only; no commands were run.
