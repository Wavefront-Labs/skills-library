---
id: computing-software.cloud-infrastructure-engineering.google-cloud.confidential-space-attestation-token-verification
name: confidential-space-attestation-token-verification
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, shielded-confidential-vms, attestation-token-verification, confidential-space-workload, workload-identity-federation, oidc]
level: sme
status: docs-checked
description: "Release secrets only to an attested workload with Confidential Space: read the attestation OIDC token claims and gate keys with WIF attribute conditions on image digest."
sources: ["https://cloud.google.com/confidential-computing/confidential-space/docs/confidential-space-overview", "https://cloud.google.com/confidential-computing/confidential-space/docs/create-grant-access-confidential-resources", "https://cloud.google.com/confidential-computing/confidential-space/docs/reference/token-claims", "https://cloud.google.com/confidential-computing/confidential-space/docs/connect-external-resources"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Confidential Space attestation token verification

Confidential Space runs a container on a hardened Confidential VM image. The attestation service issues an OIDC token describing the hardware, image and container; data owners grant access only to tokens whose claims match. A launcher in the VM requests the token from the attestation service and returns it to the workload; the default token (audience `https://sts.googleapis.com`) is fetched every hour.

## 1. Data owner: WIF pool that trusts attestation
```bash
gcloud iam workload-identity-pools create cs-pool --location=global
gcloud iam workload-identity-pools providers create-oidc attestation-verifier --location=global \
  --workload-identity-pool=cs-pool --issuer-uri=https://confidentialcomputing.googleapis.com/ \
  --allowed-audiences=https://sts.googleapis.com \
  --attribute-mapping='google.subject="gcpcs::"+assertion.submods.container.image_digest+"::"+assertion.submods.gce.project_number+"::"+assertion.submods.gce.instance_id,attribute.image_digest=assertion.submods.container.image_digest' \
  --attribute-condition="assertion.swname == 'CONFIDENTIAL_SPACE' && 'STABLE' in assertion.submods.confidential_space.support_attributes && assertion.submods.container.image_digest == 'sha256:<DIGEST>'"
gcloud kms keys add-iam-policy-binding data-key --keyring=k --location=global \
  --member="principalSet://iam.googleapis.com/projects/<NUM>/locations/global/workloadIdentityPools/cs-pool/attribute.image_digest/sha256:<DIGEST>" \
  --role=roles/cloudkms.cryptoKeyDecrypter
```
The issuer URI matches the attestation service: Google Cloud Attestation `https://confidentialcomputing.googleapis.com`, or Intel Trust Authority `https://portal.trustauthority.intel.com`. The `google.subject` value must stay under 127 bytes.

## 2. Operator: launch the workload
Create the VM from a Confidential Space image (images live in the `confidential-space-images` project) as a Confidential VM, and pass the workload through metadata: `tee-image-reference` (location of the workload container) and `tee-restart-policy` (`Never` is the default; `Always`, `OnFailure` also valid). Use the debug image family only for testing: `dbgstat` is `enable` on debug images and `disabled-since-boot` on production images, and the operator picks the family with `--image-family`.

## 3. Policy claims worth pinning
- `assertion.swname == 'CONFIDENTIAL_SPACE'` (the value is `GCE` for a revoked image).
- `'STABLE' in assertion.submods.confidential_space.support_attributes`. Debug images have no support attribute. For long-running workloads do not require `LATEST`: the image can age out of LATEST while the workload runs and fail the next token refresh.
- `assertion.dbgstat == 'disabled-since-boot'` in production.
- `assertion.submods.container.image_digest == 'sha256:...'`; the digest lets several parties agree on one workload. `assertion.hwmodel` is one of `GCP_AMD_SEV`, `GCP_AMD_SEV_ES`, `GCP_SHIELDED_VM`, `GCP_INTEL_TDX`.
- `assertion.google_service_accounts`, `assertion.submods.gce.project_number`, `zone`, `instance_id`, and `container.restart_policy`, `env_override`, `cmd_override` to constrain what the operator may change (the workload author's launch policy governs which overrides are allowed).

## Gotchas
- Pin by **image digest**, never tag. Every rebuild changes the digest and needs a policy update.
- Add `assertion.dbgstat == 'disabled-since-boot'` in production conditions.

## Verify
- [ ] Workload decrypts with KMS; the same image on a debug VM or a different digest gets PERMISSION_DENIED; Cloud Logging shows the `gcpcs::` subject.

## Checked
2026-10-31. Confirmed against the Confidential Space "create and grant access" page and the token-claims reference: the OIDC provider command shape, issuer URIs, audience, attribute mapping and condition, the KMS binding with `attribute.image_digest`, support attributes and LATEST/STABLE guidance, `dbgstat` values, `swname`, `hwmodel` values, container and VM assertions, the hourly token refresh, the 127-byte subject limit. gcloud flags checked against the gcloud reference. Removed: the full `compute instances create` example, image family and machine-type values, the token file path and `credential_source` setup, `tee.launch_policy.*` label names, and the STS audit log claim (not on the pages read).
Method: documentation only; no commands were run.
