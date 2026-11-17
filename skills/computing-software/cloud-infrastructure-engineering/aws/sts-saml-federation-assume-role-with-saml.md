---
id: computing-software.cloud-infrastructure-engineering.aws.sts-saml-federation-assume-role-with-saml
name: sts-saml-federation-assume-role-with-saml
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sts, assume-role-with-saml, saml-federation-console, saml-provider, iam-role, federation, adfs]
level: practitioner
status: docs-checked
description: "Federate an IdP straight into IAM roles with a SAML provider and AssumeRoleWithSAML: metadata, role/attribute mapping, trust policy, session tags and CLI access."
sources: ["https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_saml.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_saml_assertions.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_enable-console-saml.html", "https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRoleWithSAML.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Direct SAML 2.0 federation into IAM roles

**When:** a single account (or a few) where Identity Center is not an option, or a legacy
ADFS/Okta/Entra setup that maps groups straight to IAM roles. For many accounts prefer
IAM Identity Center; this is the per-account mechanism underneath.

## 1. Create the SAML provider
Download the IdP metadata XML, then:
```bash
aws iam create-saml-provider --name CorpIdP --saml-metadata-document file://idp-metadata.xml
# rotate signing certs later with:
aws iam update-saml-provider --saml-provider-arn arn:aws:iam::111122223333:saml-provider/CorpIdP \
  --saml-metadata-document file://idp-metadata-new.xml
```
IAM does not evaluate or act on the expiry of X.509 certificates in SAML metadata, so monitor
certificate expiry and rotate by uploading new metadata before the IdP switches. IAM also supports
encrypted assertions (upload your private key; `--assertion-encryption-mode` accepts `Required` or `Allowed`).
With encryption required the sign-in URL carries the provider's unique ID (`/saml/acs/<IdP-ID>`).

## 2. Role trust policy
```json
{"Version": "2012-10-17",
 "Statement": [{
   "Effect": "Allow",
   "Principal": {"Federated": "arn:aws:iam::111122223333:saml-provider/CorpIdP"},
   "Action": ["sts:AssumeRoleWithSAML"],
   "Condition": {"StringEquals": {"SAML:aud": "https://signin.aws.amazon.com/saml"}}}]}
```
For regional sign-in endpoints use `https://<region>.signin.aws.amazon.com/saml` as the
ACS URL (the SAML `Recipient`, which becomes `saml:aud`). Add `sts:TagSession` to the action list if the
IdP sends `PrincipalTag` attributes, and `sts:SetSourceIdentity` if it sends a `SourceIdentity` attribute;
roles connected to the IdP without that permission make the assume call fail.

## 3. Assertion attributes the IdP must send
| Attribute name | Value |
|---|---|
| `https://aws.amazon.com/SAML/Attributes/Role` | `arn:aws:iam::111122223333:role/Dev,arn:aws:iam::111122223333:saml-provider/CorpIdP` (one value per role the user may pick) |
| `https://aws.amazon.com/SAML/Attributes/RoleSessionName` | email or UPN (2-64 chars, `[\w+=,.@-]`) |
| `https://aws.amazon.com/SAML/Attributes/SessionDuration` | optional, 900-43200 seconds; extends console sessions only, and the shorter of this and `SessionNotOnOrAfter` applies |
| `https://aws.amazon.com/SAML/Attributes/PrincipalTag:team` | optional session tags for ABAC |
| `https://aws.amazon.com/SAML/Attributes/SourceIdentity` | optional, survives role chaining; trust policy needs `sts:SetSourceIdentity` |
NameID formats supported include persistent, transient, emailAddress and unspecified; the assertion must
contain exactly one `SubjectConfirmation` with `NotOnOrAfter` and a `Recipient` matching the sign-in URL.
Each `Role` value is a comma-delimited pair of the role ARN and the provider ARN, like the `RoleArn` and
`PrincipalArn` parameters of `AssumeRoleWithSAML`. Attribute names are case-sensitive.

Map IdP groups to roles with a naming convention: group `AWS-111122223333-Dev` becomes
the Role attribute above. One mapping rule then covers all accounts.

## 4. Console and CLI
- Console: IdP-initiated SSO to `https://signin.aws.amazon.com/saml`; users with more
  than one role see a role picker.
- CLI: the AWS CLI has no built-in SAML login; use your IdP's tooling to obtain the assertion, or call STS
  with an assertion you captured:
```bash
aws sts assume-role-with-saml --role-arn arn:aws:iam::111122223333:role/Dev \
  --principal-arn arn:aws:iam::111122223333:saml-provider/CorpIdP \
  --saml-assertion "$(cat assertion.b64)" --duration-seconds 3600
```
  The call needs no AWS credentials. Wrap in `credential_process` so SDKs refresh.

## 5. Troubleshooting
A browser SAML tracer shows the assertion. The API returns `InvalidIdentityToken` (assertion could not be
validated), `ExpiredToken`, `IDPRejectedClaim`, `PackedPolicyTooLarge` (session token too large) or
`RegionDisabled`. Typical causes to check:
- `Recipient` or audience not matching the sign-in URL you used, or an expired or rotated signing certificate in the IAM metadata.
- A role or provider ARN in the `Role` attribute with a typo or an account ID mismatch, or a trust policy that does not name the provider.
- `RoleSessionName` missing or containing characters outside letters, digits and `_ . , + = @ -` (2 to 64 characters).
- `DurationSeconds` above the role's maximum session duration fails (`aws iam update-role --max-session-duration 43200`).
CloudTrail records the `AssumeRoleWithSAML` call including the NameID value, so prefer a persistent identifier
that is not personally identifiable; use it to audit who used which role.

## Gotchas
- Removing a user from the IdP group does not end sessions already issued; they last
  until expiry. Keep durations short for admin roles; the IAM console can revoke a role's sessions.
- Each account needs its own SAML provider and roles; use StackSets to deploy them.
- Assertion size: dozens of Role values bloat the assertion; filter groups to AWS-only.

## Verify
- [ ] `aws iam list-saml-providers` shows the provider with a non-expired `ValidUntil`.
- [ ] A test user mapped to exactly one role lands directly in it; a user with several `Role` values sees the picker.
- [ ] CloudTrail shows `AssumeRoleWithSAML` with the expected RoleSessionName and tags.
- [ ] Certificate rotation tested: new metadata uploaded before the IdP switches signing certificates.

## Checked

Checked 2026-10-27 against the IAM User Guide pages "About SAML 2.0-based federation", "Configure SAML assertions for the authentication response" and "Enable SAML 2.0 federated users to access the console", the AWS STS API reference for AssumeRoleWithSAML, and the botocore iam and sts models:
- Attribute names (`Role`, `RoleSessionName`, `SessionDuration`, `PrincipalTag:<key>`, `TransitiveTagKeys`, `SourceIdentity`), their value rules, NameID formats, Recipient requirement and the sign-in URL forms.
- IAM does not act on certificate expiry; encrypted assertions need an uploaded private key; `--assertion-encryption-mode` values `Required` and `Allowed`.
- `AssumeRoleWithSAML` needs no AWS credentials, role chaining and `DurationSeconds` rules, the error names listed, and that CloudTrail records the NameID.
Removed because not found: the two-certificate limit, the clock-skew figure, exact console error strings, third-party CLI tool names and the `SAMLUser` identity type.

Method: documentation only; no commands were run.
