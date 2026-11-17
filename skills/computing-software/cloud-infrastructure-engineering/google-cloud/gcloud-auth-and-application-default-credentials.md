---
id: computing-software.cloud-infrastructure-engineering.google-cloud.gcloud-auth-and-application-default-credentials
name: gcloud-auth-and-application-default-credentials
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, gcloud-auth, application-default-credentials, adc, gcloud-auth-login, gcloud-auth-application-default-login, google-application-credentials, quota-project, print-access-token, auth-activate-service-account, impersonation-adc, credential-lookup-order]
level: practitioner
status: docs-checked
description: "Tell gcloud credentials from Application Default Credentials: auth login vs application-default login, the ADC lookup order, quota projects and impersonated ADC."
sources: ["https://docs.cloud.google.com/docs/authentication/application-default-credentials", "https://docs.cloud.google.com/docs/authentication/provide-credentials-adc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gcloud auth and Application Default Credentials

**Goal:** a developer laptop, a CI runner and a VM each authenticate the right way, and the
"my code gets 403 but gcloud works" class of bug stops happening.

## 1. Two separate credential stores
| | gcloud commands | Client libraries, Terraform, SDKs |
|---|---|---|
| Set by | `gcloud auth login` | `gcloud auth application-default login` |
| Stored in | gcloud's own credential store | `$HOME/.config/gcloud/application_default_credentials.json` (Linux, macOS), `%APPDATA%\gcloud\application_default_credentials.json` (Windows) |
| Inspect | `gcloud auth list` | `gcloud auth application-default print-access-token` |
The two credential sets are distinct, so logging in to one does not set the other. A common "works in gcloud, fails in code" cause is a missing or different-account ADC file.

## 2. ADC lookup order (what the library does)
1. `GOOGLE_APPLICATION_CREDENTIALS` env var → path to a credential configuration file (Workforce or Workload Identity Federation) **or** a service account key (keys are a security risk and not recommended).
2. The `application_default_credentials.json` file written by `gcloud auth application-default login`.
3. The attached service account, returned by the metadata server.
Step 3 is the preferred method in production on Google Cloud: create a user-managed SA with least-privilege roles and attach it to the resource.

## 3. Laptop setup (no keys)
```bash
gcloud auth login                                   # for gcloud
gcloud auth application-default login               # for code; opens browser
gcloud auth application-default set-quota-project <PROJECT_ID>
```
The quota project setting is for APIs that need a billing/quota project when called with user credentials; see the `set-quota-project` command reference.

Impersonated ADC — act as the deployer SA without downloading a key:
```bash
gcloud auth application-default login --impersonate-service-account=deployer@<PROJECT_ID>.iam.gserviceaccount.com
```
ADC created this way contains credentials from impersonating the service account. To use scopes beyond cloud-platform (default for user ADC), pass `--scopes`; for non-Google-Cloud scopes use an OAuth client ID file (`--client-id-file`) or impersonation.

## 4. CI and VMs
- On Google Cloud resources: attach the SA; nothing to configure.
- External CI: use a Workload Identity Federation credential configuration file via `GOOGLE_APPLICATION_CREDENTIALS`.
- Last resort: `gcloud auth activate-service-account --key-file=key.json` for gcloud; service account keys are not recommended.

## 5. Tokens by hand
```bash
gcloud auth print-access-token                       # user/SA token for curl against APIs
gcloud auth print-identity-token --audiences=https://<RUN_URL>   # ID token to call Cloud Run
gcloud auth print-access-token --impersonate-service-account=<SA>
```
Do not paste tokens into config files.

## Gotchas
- By default, access tokens from a user-credential ADC file include the `https://www.googleapis.com/auth/cloud-platform` scope.
- `GOOGLE_APPLICATION_CREDENTIALS` is searched first, ahead of the login file and the metadata server, so a stale env var on a VM is used instead of the attached SA.

## Verify
- [ ] `gcloud auth list` and `gcloud auth application-default print-access-token` both succeed for the intended identity.
- [ ] A client-library hello-world (list buckets) runs on the laptop with no key file in the environment.
- [ ] On the VM, `echo $GOOGLE_APPLICATION_CREDENTIALS` is empty so the attached SA is used.

## Checked
2026-10-31. Confirmed on "How Application Default Credentials works": search order, accepted GOOGLE_APPLICATION_CREDENTIALS file types and key warning, ADC file locations per OS, ADC distinct from gcloud credentials, default cloud-platform scope, `--scopes`, `--client-id-file`, `--impersonate-service-account`, attached SA preferred in production. Removed: credentials.db names, quota-project explanation and permission, token-creator role, metadata curl, `--cred-file` login, token lifetime, revoke behaviour, org policy name, process-caching note (not on fetched pages). Commands checked with check_commands.py.
Method: documentation only; no commands were run.
