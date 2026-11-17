---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.s3-oidc-sts-setup
name: s3-oidc-sts-setup
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [assumerolewithwebidentity, keycloak, iam-config, oidc, sts]
level: advanced
status: docs-checked
description: "Wire an OIDC identity provider to SeaweedFS S3 with -s3.iam.config: sts block, provider roleMapping, roles with trust policies and role assumption."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/OIDC-Integration
  - https://github.com/seaweedfs/seaweedfs/wiki/S3-Configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# s3 oidc sts setup

Use `-s3.iam.config` for OIDC, STS and IAM-style policies (not for static access keys). The page gives issuer guidance for Keycloak, Okta, Auth0 and AWS Cognito.

Structure: `sts`, `providers`, `policies`, `roles`.
```json
{"sts":{"tokenDuration":"1h","maxSessionLength":"12h","issuer":"seaweedfs-sts","signingKey":"<base64, 32+ bytes>"}}
```
Provider (type `oidc`):
```json
{"name":"my-idp","type":"oidc","enabled":true,"config":{
  "issuer":"https://idp.example.com","clientId":"seaweedfs-s3","jwksUri":"https://idp.example.com/.well-known/jwks.json",
  "scopes":["openid","profile","email","groups"],
  "roleMapping":{"rules":[{"claim":"groups","value":"admins","role":"arn:aws:iam::role/S3AdminRole"}],"defaultRole":"arn:aws:iam::role/S3ReadOnlyRole"}}}
```
Role:
```json
{"roleName":"S3ReadOnlyRole","roleArn":"arn:aws:iam::role/S3ReadOnlyRole","attachedPolicies":["S3ReadOnlyPolicy"],
 "trustPolicy":{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Federated":"*"},"Action":["sts:AssumeRoleWithWebIdentity"],"Condition":{"StringEquals":{"oidc:iss":"https://idp.example.com"}}}]}}
```
Clients can send an OIDC bearer token directly (RSA and ECDSA) or assume a role via STS.

All S3 gateway instances must share the same STS issuer and `signingKey` (use the same IAM config on each). Make `oidc:iss` in the trust policy match the token `iss` claim exactly.

## Checked

2026-11-04. Confirmed against the SeaweedFS wiki pages OIDC Integration (sts block, signingKey 32+ bytes base64, provider and role JSON, trust policy, bearer tokens RSA and ECDSA, shared signingKey) and S3 Configuration (`-s3.iam.config`). Narrowed the provider list to those the page names; removed the stability-across-restarts claim and the Verify line.
Method: documentation only; no commands were run.
