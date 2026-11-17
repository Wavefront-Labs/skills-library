---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-external-key-manager-ekm
name: cloud-external-key-manager-ekm
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-kms, cloud-ekm, external-key-manager, ekm-via-vpc, key-access-justifications, hyok]
level: practitioner
status: docs-checked
description: "Use Cloud EKM to keep CMEK key material in an external key manager: internet vs VPC connectivity, EKM connections, key creation, and availability risks."
sources: ["https://cloud.google.com/kms/docs/ekm", "https://cloud.google.com/kms/docs/create-ekm-connection", "https://cloud.google.com/kms/docs/create-external-key"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud External Key Manager (EKM)

With EKM, a Cloud KMS key (protection level `EXTERNAL` or `EXTERNAL_VPC`) is a reference to a key
in a supported external KMS partner. Every encrypt/decrypt calls out to that system, so Google
never holds the key material. Used for sovereignty/HYOK requirements.

## Connectivity
- **EKM via internet** (`EXTERNAL`): KMS calls the partner's public endpoint over TLS.
- **EKM via VPC** (`EXTERNAL_VPC`): KMS reaches the EKM through your VPC using Service Directory;
  coordinated external keys (EKM management mode Cloud KMS) use this path. Not available in multi-regional locations.
- Supported partners listed on the EKM page: Fortanix, Futurex and Thales. Manually managed keys have no automatic rotation.

## Setup (VPC)
```bash
gcloud service-directory namespaces create ekm-ns --location=europe-west2
gcloud service-directory services create ekm-svc --namespace=ekm-ns --location=europe-west2
gcloud service-directory endpoints create ekm-ep --service=ekm-svc --namespace=ekm-ns --location=europe-west2 \
  --address=10.10.0.5 --port=443 --network=projects/<PN>/locations/global/networks/prod
gcloud kms ekm-connections create ekm-conn --location=europe-west2 \
  --service-directory-service=projects/<P>/locations/europe-west2/namespaces/ekm-ns/services/ekm-svc \
  --hostname=ekm.example.com --server-certificates-files=ekm-server.pem \
  --key-management-mode=manual
gcloud kms keyrings create ext-ring --location=europe-west2
gcloud kms keys create gcs-key --keyring=ext-ring --location=europe-west2 --purpose=encryption \
  --protection-level=external-vpc --default-algorithm=external-symmetric-encryption \
  --crypto-key-backend=projects/<P>/locations/europe-west2/ekmConnections/ekm-conn --skip-initial-version-creation
gcloud kms keys versions create --key=gcs-key --keyring=ext-ring --location=europe-west2 \
  --ekm-connection-key-path=<PATH_FROM_PARTNER> --primary
```
Grant `roles/servicedirectory.viewer` and `roles/servicedirectory.pscAuthorizedService` in the VPC project to
`service-<KEY_PROJECT_NUMBER>@gcp-sa-ekms.iam.gserviceaccount.com`. Grant the Google Cloud project access to the key in the partner system too.

## Risks
- If the EKM is unreachable or the key is revoked, all dependent data is unreadable (by design); an unavailable
  key returns `FAILED_PRECONDITION`. Enable data access audit logging. Preview metrics `cloudkms.googleapis.com/ekm/external/request_count`
  and `request_latencies` show usage. Example from Google: a Spanner database whose CMEK key is unavailable for more than 30 consecutive days is deleted.
- Internet connectivity adds reliability and latency risk; Google suggests Cloud EKM over VPC or Cloud HSM for better availability.
- Not every CMEK-integrated service supports EKM; check the compatibility list.
- Key Access Justifications can make the EKM approve/deny per request reason.

## Verify
- [ ] Bucket with EKM CMEK reads/writes; revoking at the partner causes access errors (in a test project).

## Checked
Date: 2026-10-28. Confirmed against the Cloud EKM overview and Create an EKM connection pages: protection levels `EXTERNAL`/`EXTERNAL_VPC`, partners, coordinated versus manual management, `--key-management-mode manual`, no initial key version via API/CLI, service agent and Service Directory roles, metric names (Preview), `FAILED_PRECONDITION`, Spanner 30-day example, multi-region limits; gcloud flags checked against the CLI reference. Removed: the DEK-caching latency remark and the "HA EKM" advice (not on the pages). Hostnames, IPs and paths are placeholders.
Method: documentation only; no commands were run.
