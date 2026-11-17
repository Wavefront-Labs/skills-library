---
id: computing-software.cloud-infrastructure-engineering.google-cloud.workload-identity-federation-from-azure-and-oidc
name: workload-identity-federation-from-azure-and-oidc
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, workload-identity-federation, wif-oidc, wif-azure, entra-id-workload, managed-identity-to-gcp, oidc-provider, issuer-uri, allowed-audiences, jwks, gitlab-oidc, kubernetes-oidc, keyless-auth]
level: advanced
status: docs-checked
description: "Federate any OIDC issuer (Azure managed identity, GitLab CI, on-prem Kubernetes) into GCP: OIDC provider, issuer and audience pinning, claim mapping, credential config."
sources: ["https://cloud.google.com/iam/docs/workload-identity-federation-with-other-clouds#azure", "https://cloud.google.com/iam/docs/workload-identity-federation-with-other-providers", "https://cloud.google.com/sdk/gcloud/reference/iam/workload-identity-pools/providers/create-oidc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Workload Identity Federation from Azure and OIDC issuers

**Goal:** any workload that can obtain an OIDC JWT from a trusted issuer can call Google APIs
without a stored Google credential — Azure VMs via managed identity, GitLab CI jobs,
Kubernetes clusters anywhere.

## 1. Azure (managed identity)
Azure side: create an **app registration** (or use the managed identity's own audience) and
note the tenant ID. The token comes from the Azure IMDS endpoint with
`resource=<APP_ID_URI>`.
```bash
gcloud iam workload-identity-pools create azure-pool --location=global
gcloud iam workload-identity-pools providers create-oidc azure --workload-identity-pool=azure-pool --location=global \
  --issuer-uri="https://sts.windows.net/<TENANT_ID>" \
  --allowed-audiences="<APPLICATION_ID_URI>" \
  --attribute-mapping="google.subject=assertion.sub,attribute.tid=assertion.tid" \
  --attribute-condition="assertion.tid=='<TENANT_ID>'"
gcloud iam workload-identity-pools create-cred-config \
  projects/<NUM>/locations/global/workloadIdentityPools/azure-pool/providers/azure \
  --service-account=<SA_EMAIL> --azure --app-id-uri="<APPLICATION_ID_URI>" --output-file=gcp-cred.json
```
`<APPLICATION_ID_URI>` is the Application ID URI of the Entra app registration (for example `api://my-app`).
Grant `roles/iam.workloadIdentityUser` on the SA to `principal://.../azure-pool/subject/<SUBJECT>`.
Google's guide notes the issuer URI can vary: decode a real token (for example at jwt.io) and match its `iss` claim.

## 2. Generic OIDC (GitLab, Kubernetes, Vault, Okta)
Requirements (Google guide): tokens are JWTs with an issuer claim such that `ISSUER/.well-known/openid-configuration`
points at the IdP's OIDC metadata, and the JWKS URL in that metadata is HTTPS. If the issuer is not
reachable, upload keys with `--jwk-json-path`. Then:
```bash
gcloud iam workload-identity-pools providers create-oidc gitlab --workload-identity-pool=ci-pool --location=global \
  --issuer-uri="https://gitlab.example.com/" --allowed-audiences="https://gitlab.example.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.project_path=assertion.project_path,attribute.ref=assertion.ref" \
  --attribute-condition="assertion.project_path.startsWith('platform/') && assertion.ref_protected=='true'"
```
GitLab's Google Cloud guide gives the issuer as the instance address with a trailing slash and the allowed
audience as the address without one; confirm both against your token's `iss` and `aud`.
GitLab job: `id_tokens: { GCP_ID_TOKEN: { aud: "https://gitlab.example.com" } }` then a cred
config with `--credential-source-file` pointing at a file containing the token (or
`--credential-source-url`/`--executable-command` for other sources).
Kubernetes (non-GKE): see the Workload Identity Federation with Kubernetes guide for the issuer and projected token setup.

## 3. Which claims to map
- `google.subject` cannot exceed 127 characters and must be stable and unique per workload. GitLab's default `sub` is `project_path:{group}/{project}:ref_type:{type}:ref:{branch}`, so group grants by `project_path` or `namespace_id`.
- `attribute.*` whatever you will grant on: environment, repo, ref, tenant.
- Use an `--attribute-condition`: Google's best-practices page says to use attribute conditions when federating with GitHub or other multi-tenant providers.

## 4. Grant and test
```bash
gcloud iam service-accounts add-iam-policy-binding <SA_EMAIL> --role=roles/iam.workloadIdentityUser \
  --member="principalSet://iam.googleapis.com/projects/<NUM>/locations/global/workloadIdentityPools/ci-pool/attribute.project_path/platform/infra"
export GOOGLE_APPLICATION_CREDENTIALS=gcp-cred.json; gcloud auth login --cred-file=gcp-cred.json; gcloud projects list
```

## Gotchas
- `issuer-uri` must match the token's `iss` claim exactly; decode a token and compare before debugging anything else.
- `allowed-audiences` is the audience the token's `aud` must carry; set it explicitly and mint tokens with that `aud`.

## Verify
- [ ] Decode an issuer token and confirm `iss`, `aud`, `sub` match the provider config.
- [ ] A workload with a matching claim set authenticates; one failing the attribute condition gets `PERMISSION_DENIED` at STS.
- [ ] No Google service-account keys exist for the federated SA.

## Checked

- Date: 2026-10-27
- Confirmed against the gcloud reference pages for `providers create-oidc` (`--issuer-uri`, `--allowed-audiences`, `--attribute-mapping`, `--attribute-condition`, `--jwk-json-path`) and `create-cred-config` (`--azure`, `--app-id-uri`), the Azure and other-providers sections of the WIF guide (issuer form `https://sts.windows.net/TENANT_ID`, OIDC discovery and HTTPS JWKS requirement, 127-character subject), the best-practices page (attribute conditions for multi-tenant IdPs) and GitLab's Google Cloud guide (issuer with trailing slash, audience without, default `sub`).
- Changed: Azure issuer URI to the documented form without a trailing slash; GitLab issuer to the trailing-slash form from GitLab's guide.
- Removed unconfirmed claims: managed-identity `sub` is the object ID, Entra v2 issuer form, `kubectl get --raw` discovery step, default audience, token lifetime and JWKS-rotation notes, Azure v1/v2 default, error message text, and the offline `jq` decode command.

Method: documentation only; no commands were run.
