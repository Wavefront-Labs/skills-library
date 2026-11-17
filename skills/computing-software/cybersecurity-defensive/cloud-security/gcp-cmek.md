---
id: computing-software.cybersecurity-defensive.cloud-security.gcp-cmek
name: gcp-cmek
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cmek, cloud-kms, customer-managed-encryption-keys, cloud-ekm, key-rotation, org-policy, cloud-data-protection]
level: practitioner
status: docs-checked
description: "Customer-managed encryption keys in Google Cloud: service agent grants, CMEK org policy constraints and gaps, Autokey defaults, Cloud EKM availability risk."
sources: ["https://docs.cloud.google.com/kms/docs/cmek", "https://docs.cloud.google.com/kms/docs/cmek-org-policy", "https://docs.cloud.google.com/kms/docs/autokey-overview", "https://docs.cloud.google.com/kms/docs/ekm"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CMEK in Google Cloud

With Google-managed keys you cannot view or manage the keys or their usage logs. With CMEK you own the keys and control location, protection level, access, rotation, use and destruction.

## How it works
- Each service uses its project's **service agent** to encrypt and decrypt; as long as the service agent holds the Cloud KMS CryptoKey Encrypter/Decrypter role on the key, the service works. Requesters do not need the role.
- Place key rings geographically near the protected resources. Rotation period can be set, or a rotation triggered.
- **Key usage tracking** shows which resources, projects and products in the organisation are protected by a key.
- Revoking the service agent's role, or disabling or destroying the key, makes the data inaccessible; some services can suffer permanent data loss if a CMEK stays disabled or inaccessible too long.

## Enforce with org policy
- `constraints/gcp.restrictNonCmekServices`: list of service names (for example `bigquery.googleapis.com`) set to Deny; creating resources there without a Cloud KMS key fails, and removing CMEK is blocked. Supported services only.
- `constraints/gcp.restrictCmekCryptoKeyProjects`: Allow-list of `projects/ID` or `under:folders/ID` that keys must come from. It does not guarantee CMEK use, so pair it with the first constraint.
- Applies only to newly created resources, or when changing the key on an existing resource. Not fully enforced for BigQuery dataset default keys; built-in Cloud Logging buckets need separate configuration; Storage Transfer Service needs both `storagetransfer.googleapis.com` and `secretmanager.googleapis.com` listed. Requiring CMEK for one service can block a CMEK-unaware service it triggers.
- Console users need `orgpolicy.policies.check` to avoid choosing a disallowed key and failing later.

## Autokey
Creates key rings (`autokey`) and keys on demand and grants the service account encrypt/decrypt, so developers need no KMS access. Defaults: HSM protection, AES-256 GCM, one-year rotation (changeable), key in the resource's location, not exportable, no charge beyond Cloud HSM key pricing. Keys live in a dedicated key project for a folder or in the resource's own project. Cloud KMS admins cannot encrypt or decrypt. Limits: some integrations only via Terraform or REST; it does not create keys for Cloud SQL backups, Storage objects or Compute snapshots (they follow the parent key); only where Cloud HSM is available.

## Cloud EKM
Keys stay in a partner system (Fortanix, Futurex, Thales) and are contacted on each request; nothing is cached. Both the EKM key version and the external key must be available, or Cloud KMS returns `FAILED_PRECONDITION` and data can be lost (Spanner deletes a database whose key is unavailable over 30 consecutive days). Google cannot recover data if you lose externally managed keys. Key Access Justifications attach a reason code to each request that the partner can allow or deny. Connection over internet (`EXTERNAL`) or VPC (`EXTERNAL_VPC`); no automatic rotation for manually managed keys; `global` location not supported.

## Verify
- [ ] Org policy blocks creating a non-CMEK resource in the scoped service and folder.
- [ ] Key usage tracking lists the expected resources.

## Checked
Method: 2026-11-08 read the four cited pages (now at docs.cloud.google.com) in full. Updated source URLs to the redirect targets. Dropped as unsupported: the HSM FIPS level, the 30-day destroy delay and `DestroyCryptoKeyVersion` monitoring, data-access-log advice, the 90-365 day rotation range, the example service agent address and bucket command, and the claim that a separate key project is required (Autokey docs show both models). Core CMEK, org policy and EKM facts unchanged.
