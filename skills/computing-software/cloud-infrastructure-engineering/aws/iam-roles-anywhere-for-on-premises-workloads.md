---
id: computing-software.cloud-infrastructure-engineering.aws.iam-roles-anywhere-for-on-premises-workloads
name: iam-roles-anywhere-for-on-premises-workloads
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, iam, roles-anywhere, trust-anchor, x509-credentials, credential-helper-roles-anywhere, hybrid, temporary-credentials]
level: practitioner
status: docs-checked
description: "Give on-prem servers and other clouds short-lived AWS credentials with IAM Roles Anywhere: trust anchors, profiles, role trust conditions and the signing helper."
sources: ["https://docs.aws.amazon.com/rolesanywhere/latest/userguide/trust-model.html", "https://docs.aws.amazon.com/rolesanywhere/latest/userguide/credential-helper.html", "https://docs.aws.amazon.com/rolesanywhere/latest/userguide/authentication-create-session.html", "https://github.com/boto/botocore/blob/develop/botocore/data/rolesanywhere/2018-05-10/service-2.json"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IAM Roles Anywhere

**Goal:** replace long-term IAM user access keys on servers outside AWS (datacentre VMs,
CI runners, other clouds) with X.509-certificate-based temporary credentials.

## 1. Pieces
- **Trust anchor:** the CA that issued the workload certificates. Source types are `AWS_ACM_PCA` (an AWS Private
  CA), `CERTIFICATE_BUNDLE` (your own CA certificate, PEM) and `SELF_SIGNED_REPOSITORY`. A trust anchor
  certificate needs key usage `Certificate Sign` (and may include `CRL Sign`) and basic constraints `CA: true`.
- **Profile:** which roles may be assumed, session duration (`durationSeconds`, default 3600), optional session
  policies and managed policy ARNs, and `acceptRoleSessionName`.
- **Role:** normal IAM role whose trust policy trusts `rolesanywhere.amazonaws.com`.
- **Credential helper** (`aws_signing_helper`) on the host: signs `CreateSession` with the private key and returns
  credentials. `CreateSession` is a wrapper around `AssumeRole`.

## 2. Setup
```bash
aws rolesanywhere create-trust-anchor --name corp-ca --enabled \
  --source "sourceType=CERTIFICATE_BUNDLE,sourceData={x509CertificateData=$(cat ca.pem)}"
aws rolesanywhere create-profile --name batch-servers --enabled \
  --role-arns arn:aws:iam::111122223333:role/OnPremBatch --duration-seconds 3600
```
Role trust policy, pinned to the anchor and to certificate fields. The policy must grant `sts:AssumeRole`,
`sts:TagSession` and `sts:SetSourceIdentity`:
```json
{"Version": "2012-10-17",
 "Statement": [{
   "Effect": "Allow",
   "Principal": {"Service": "rolesanywhere.amazonaws.com"},
   "Action": ["sts:AssumeRole", "sts:TagSession", "sts:SetSourceIdentity"],
   "Condition": {
     "ArnEquals": {"aws:SourceArn": "arn:aws:rolesanywhere:eu-west-1:111122223333:trust-anchor/TA_ID"},
     "StringEquals": {"aws:PrincipalTag/x509Subject/CN": "batch-worker"}}}]}
```
AWS recommends extra conditions on certificate attributes; without them any certificate from the trusted CA could
be used to assume the role. `aws:SourceArn` / `aws:SourceAccount` are set from the trust anchor ARN in the
`CreateSession` call and guard against confused-deputy use.
Certificate fields become session principal tags: `x509Subject/<RDN>` (for example `x509Subject/CN`),
`x509Issuer/<RDN>`, and `x509SAN/DNS`, `x509SAN/URI`, `x509SAN/Name/<RDN>` (the first value of each SAN type).
Repeated RDNs (several OU values) are joined with `/` into one tag value, in certificate order, so a condition on
`x509Subject/OU` must match the combined string. Values that do not match the STS tag pattern are ignored.
The session's source identity comes from the subject common name.

## 3. Host configuration
End-entity certificate requirements: X.509v3; if `CA` is present in basic constraints it must be `false`; key
usage must include `Digital Signature`; signature algorithm SHA-256 or stronger (MD5 and SHA-1 are rejected).
Certificates with an empty subject are not supported.
```ini
# ~/.aws/config
[profile onprem]
credential_process = aws_signing_helper credential-process \
  --certificate /etc/pki/app/cert.pem --private-key /etc/pki/app/key.pem \
  --trust-anchor-arn arn:aws:rolesanywhere:eu-west-1:111122223333:trust-anchor/TA_ID \
  --profile-arn arn:aws:rolesanywhere:eu-west-1:111122223333:profile/PROFILE_ID \
  --role-arn arn:aws:iam::111122223333:role/OnPremBatch
```
Key storage: a PKCS#11 URI can be given to `--certificate` / `--private-key` (with `--pkcs11-lib` where p11-kit is
not available), a TPM-wrapped key file or `handle:` reference can be given to `--private-key`, and on Windows and
macOS `--cert-selector` uses the OS certificate store. `aws_signing_helper serve` starts a local endpoint on
127.0.0.1 (port 9911 by default) that implements the IMDSv2 URIs; point SDKs at it with
`AWS_EC2_METADATA_SERVICE_ENDPOINT`. Any process that can reach that address can read the credentials.
`aws_signing_helper update` writes credentials to the credentials file instead.
The session duration can be requested per call (`--session-duration`, 900-43200 seconds); the effective value is
the smaller of the profile and request values, and a value above the role's maximum session duration fails.

## 4. Revocation and rotation
- Import a CRL: `aws rolesanywhere import-crl --name corp-crl --crl-data fileb://crl.der
  --trust-anchor-arn ...`. Revocation is supported through imported CRLs only (API and CLI); callbacks to CRL
  distribution points and OCSP are not supported, so re-import on every CRL publish.
- Disable a whole anchor (`disable-trust-anchor`) or profile (`disable-profile`) in an emergency.
- Rotate host certs well before expiry; sessions already issued last until their expiry.
- Notification settings (`put-notification-settings`) support the events `CA_CERTIFICATE_EXPIRY` and
  `END_ENTITY_CERTIFICATE_EXPIRY`.

## 5. Monitoring
The default role session name is the certificate's serial number, so CloudTrail entries for calls made with the
session identify the certificate; a custom `roleSessionName` is honoured only if the profile sets
`acceptRoleSessionName`. Alert on sessions from unexpected subjects, and add source-IP conditions in policies if
hosts have fixed egress.

## Gotchas
- `CreateSession` is regional: use the Region of the trust anchor and profile.
- Only anchor to a CA you control: the trust anchor decides which certificates may reach `CreateSession`.
- The credential helper's `serve` and `update` commands refresh credentials about five minutes before expiry.

## Verify
- [ ] `aws sts get-caller-identity --profile onprem` returns the assumed role with the expected session name (cert serial).
- [ ] A certificate with a different subject is rejected with AccessDenied.
- [ ] A certificate revoked in an imported CRL cannot create a session.
- [ ] No IAM user access keys remain on the migrated hosts.

## Checked
Checked 2026-10-24 against the IAM Roles Anywhere User Guide pages "Trust model", "Get temporary security
credentials" (credential helper) and "CreateSession API", and the botocore Roles Anywhere model. Corrected: the
old text said `--pkcs11` / `--tpm-key` options exist (the helper uses PKCS#11 URIs, TPM key files or handles, and
`--pkcs11-lib`); said the OU subject tag is a simple value (repeated OUs are joined with `/`); said expiry
notifications are for trust anchor CA certificates only (the events are `CA_CERTIFICATE_EXPIRY` and
`END_ENTITY_CERTIFICATE_EXPIRY`); and described the CloudTrail session name loosely. Confirmed: trust policy
actions, `aws:SourceArn`, principal tag names, certificate requirements, CRL-only revocation, `serve` behaviour
(127.0.0.1:9911, IMDSv2 URIs), session duration range 900-43200 and profile default 3600, and CLI parameter names.
Removed the unchecked claims that clock skew breaks validation, that public CAs are unsafe in general (reworded to
trust-anchor control), that profile session policies can only reduce permissions, and the CloudTrail `AssumeRole`
event detail.
Method: documentation only; no commands were run.
