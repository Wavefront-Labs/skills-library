---
id: computing-software.cloud-infrastructure-engineering.google-cloud.workforce-identity-pools-and-providers
name: workforce-identity-pools-and-providers
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, workforce-identity-federation, workforce-pools, workforce-identity-pool-provider, okta-gcp, azure-ad-gcp, entra-id-federation, principalset-workforce, gcloud-iam-workforce-pools, console-federated-login, browser-based-sign-in, workforce-attribute-mapping]
level: advanced
status: docs-checked
description: "Federate a workforce IdP (Okta, Entra ID, OIDC or SAML) into GCP: create workforce pools and providers, map attributes, grant principalSet IAM, sign in."
sources: ["https://cloud.google.com/iam/docs/workforce-identity-federation", "https://cloud.google.com/iam/docs/configuring-workforce-identity-federation", "https://cloud.google.com/iam/docs/workforce-sign-in-gcloud", "https://cloud.google.com/sdk/gcloud/reference/iam/workforce-pools"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Workforce identity pools and providers

**Goal:** employees sign in to the console and gcloud with the corporate IdP and get IAM by
IdP group, with no Google accounts synced — the alternative to GCDS + SAML SSO.

## 1. When to choose it
Workforce Identity Federation (WIF for humans) suits: no Workspace, no desire to provision
Google identities, multiple IdPs, M&A. Trade-off: not every product fully supports federated
principals (check the *federated identity supported products* page per product), and IAM is granted to principals built from IdP
claims (`google.subject`, `google.groups`, `attribute.*`).

## 2. Create the pool and provider (org level)
```bash
gcloud iam workforce-pools create corp-pool --organization=<ORG_ID> --location=global \
  --display-name="Corporate IdP" --session-duration=28800s
# OIDC (Okta / Entra ID)
gcloud iam workforce-pools providers create-oidc okta --workforce-pool=corp-pool --location=global \
  --issuer-uri="https://<tenant>.okta.com" --client-id="<OIDC_CLIENT_ID>" \
  --client-secret-value="<CLIENT_SECRET>" --web-sso-response-type=code --web-sso-assertion-claims-behavior=merge-user-info-over-id-token-claims \
  --attribute-mapping="google.subject=assertion.sub,google.groups=assertion.groups,google.display_name=assertion.name,attribute.email=assertion.email"
# SAML
gcloud iam workforce-pools providers create-saml adfs --workforce-pool=corp-pool --location=global \
  --idp-metadata-path=metadata.xml --attribute-mapping="google.subject=assertion.subject"
```
IdP side: redirect URI `https://auth.cloud.google/signin-callback/locations/global/workforcePools/corp-pool/providers/okta`.
`google.subject` must be stable and unique (maximum 127 bytes; if it changes in the IdP the user loses access). Add an attribute condition
to limit who can federate, for example `--attribute-condition="assertion.role == 'gcp-users'"`.

## 3. Grant IAM
Principals look like:
```
principal://iam.googleapis.com/locations/global/workforcePools/corp-pool/subject/<sub>
principalSet://iam.googleapis.com/locations/global/workforcePools/corp-pool/group/<group>
principalSet://iam.googleapis.com/locations/global/workforcePools/corp-pool/attribute.department/finance
```
```bash
gcloud projects add-iam-policy-binding <PROJECT_ID> --role=roles/viewer \
  --member="principalSet://iam.googleapis.com/locations/global/workforcePools/corp-pool/group/gcp-payments-devs"
```


## 4. Sign in
- Console: use the workforce sign-in URL given in Google's *Configure Workforce Identity Federation* guide, and register the callback `https://auth.cloud.google/signin-callback/...` shown above at the IdP.
- gcloud:
```bash
gcloud iam workforce-pools create-login-config locations/global/workforcePools/corp-pool/providers/okta --output-file=login.json
gcloud auth login --login-config=login.json          # browser flow
```
`create-login-config` also takes `--activate` to make the file the default for the gcloud CLI. For client libraries see
*Obtain short-lived credentials for Workforce Identity Federation*.

## 5. Logs and access controls
Session duration (`--session-duration`) defaults to one hour and must be between 15 minutes (900s) and 12 hours
(43200s). Workforce Identity Federation detailed audit logging is a provider option (`--detailed-audit-logging`) and uses Cloud Logging.

## Gotchas
- See the Essential Contacts section of the workforce guide: federated users need contacts configured separately.
- `google.groups` only matches if the IdP sends a groups claim and the provider maps it.
- Changing the `google.subject` mapping orphans every per-user binding; map it once, correctly.
- Managing pools needs `roles/iam.workforcePoolAdmin` on the organisation.

## Verify
- [ ] A test user signs in via the pool URL and `gcloud auth list` shows `principal://...` as the account.
- [ ] A `principalSet` group binding grants access and removing the user from the IdP group revokes it at next login.

## Checked

- Date: 2026-10-27
- Confirmed against the gcloud references for `workforce-pools create` (`--organization`, `--location`, `--display-name`, `--session-duration`), `providers create-oidc` (`--client-id`, `--client-secret-value`, `--web-sso-response-type=code`, `--web-sso-assertion-claims-behavior=merge-user-info-over-id-token-claims`, `--detailed-audit-logging`), `create-saml` (`--idp-metadata-path`), `create-login-config` (`--output-file`, `--activate`), `auth login --login-config`, and the Workforce Identity Federation guides (127-byte `google.subject`, 15-minute to 12-hour session range with 1-hour default, redirect URL pattern, principal formats, `roles/iam.workforcePoolAdmin`).
- Removed or replaced: console sign-in URL (page not confirmed), `auth/login_config_file` config key, application-default login command, SAML groups mapping, Terraform resource names, case-sensitivity, super-admin and billing limits, audit-log service name, VPC-SC and Access Context Manager statements, and product-support examples. The attribute-condition example now matches the guide.

Method: documentation only; no commands were run.
