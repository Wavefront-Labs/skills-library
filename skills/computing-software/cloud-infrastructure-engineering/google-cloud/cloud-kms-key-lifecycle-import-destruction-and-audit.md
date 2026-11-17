---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-kms-key-lifecycle-import-destruction-and-audit
name: cloud-kms-key-lifecycle-import-destruction-and-audit
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-kms, kms-key-import, import-jobs, kms-key-destruction, scheduled-destruction, key-state, key-usage-tracking, kms-audit-logging, kms-terraform, prevent-destroy-kms]
level: advanced
status: docs-checked
description: "Manage Cloud KMS key versions: import key material, disable and schedule destruction with restore windows, track protected resources, audit usage, guard keys in Terraform."
sources: ["https://cloud.google.com/kms/docs/importing-a-key", "https://cloud.google.com/kms/docs/destroy-restore", "https://cloud.google.com/kms/docs/key-states", "https://cloud.google.com/kms/docs/view-key-usage", "https://cloud.google.com/kms/docs/audit-logging", "https://raw.githubusercontent.com/hashicorp/terraform-provider-google/main/website/docs/r/kms_crypto_key.html.markdown"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud KMS key lifecycle: import, destruction and audit

## 1. States
`PENDING_GENERATION` (asymmetric keys only) → `ENABLED` ⇄ `DISABLED` → `DESTROY_SCHEDULED` → `DESTROYED`
(`PENDING_IMPORT` / `IMPORT_FAILED` for imported material; a `DESTROYED` or `IMPORT_FAILED` version can be re-imported to `ENABLED` with the original key material).
A version can decrypt as long as it is enabled; which version is primary does not affect decryption.

## 2. Before destroying anything: who uses this key?
```bash
gcloud kms inventory get-protected-resources-summary \
  --keyname=projects/<P>/locations/<L>/keyRings/<KR>/cryptoKeys/<K>
gcloud kms inventory search-protected-resources --scope=organizations/<ORG_ID> \
  --keyname=projects/<P>/locations/<L>/keyRings/<KR>/cryptoKeys/<K> --format='table(name,resourceType,cryptoKeyVersion)'
```
Data protected by a version cannot be decrypted once that version is destroyed, so list protected resources first.

## 3. Disable → schedule destroy → (restore)
```bash
gcloud kms keys versions disable 3 --key=<K> --keyring=<KR> --location=<L>
# soak for weeks; watch for decrypt errors
gcloud kms keys versions destroy 3 --key=<K> --keyring=<KR> --location=<L>   # -> DESTROY_SCHEDULED
gcloud kms keys versions restore 3 --key=<K> --keyring=<KR> --location=<L>   # within the window
```
The window is the key's `--destroy-scheduled-duration` (`destroy_scheduled_duration` in the API): default 30 days, set only at key
creation and not changeable later, minimum 24 hours (0 for import-only keys), maximum 120 days. Google recommends keeping the 30-day default
unless a requirement says otherwise. The organization policy constraint "Minimum destroy scheduled duration per key" enforces a minimum org-wide.

## 4. Import key material (BYOK)
```bash
gcloud kms keys create byok-key --keyring=<KR> --location=<L> --purpose=encryption \
  --protection-level=hsm --skip-initial-version-creation
gcloud kms import-jobs create job1 --keyring=<KR> --location=<L> \
  --import-method=rsa-oaep-3072-sha256-aes-256 --protection-level=hsm
gcloud kms keys versions import --import-job=job1 --keyring=<KR> --location=<L> --key=byok-key \
  --algorithm=google-symmetric-encryption --target-key-file=./key.bin
```
gcloud wraps the key with the import job's public key (needs the `cryptography` library); or wrap
offline with your HSM and pass `--wrapped-key-file`. Keep your own escrowed copy — that's the point of BYOK.

## 5. Audit
- Alert on method `DestroyCryptoKeyVersion` (filter `protoPayload.methodName="DestroyCryptoKeyVersion"`).
- `DATA_READ` audit logs for `cloudkms.googleapis.com` cover Encrypt, Decrypt, AsymmetricSign and similar calls.

## 6. Terraform guard
```hcl
resource "google_kms_crypto_key" "data" {
  name            = "data"
  key_ring        = google_kms_key_ring.ring.id
  rotation_period = "7776000s"
  destroy_scheduled_duration = "2592000s"
  lifecycle { prevent_destroy = true }
}
```
CryptoKeys cannot be deleted from Google Cloud; destroying a Terraform-managed key removes it from state and
deletes all its versions, making data encrypted with it irrecoverable. `prevent_destroy` stops that plan.

## Gotchas
- Rotation creates a new primary; old versions still decrypt old data while enabled — don't destroy them after rotation without re-encrypting.

## Verify
- [ ] Protected-resources summary for a key scheduled for destruction is zero.
- [ ] An alert fires on a test `DestroyCryptoKeyVersion` in a sandbox key.

## Checked
Date: 2026-10-28. Confirmed against Cloud KMS pages (Key states, Destroy and restore, Importing a key, Viewing key usage, Audit logging) and the terraform-provider-google `google_kms_crypto_key` docs on GitHub: key states, 30-day default and 24 hour/120 day bounds, import steps and algorithm name, Pyca cryptography requirement, `--wrapped-key-file`, inventory commands, `DATA_READ` methods, `DestroyCryptoKeyVersion` filter, Terraform destroy behaviour and `prevent_destroy`; gcloud flags checked against the CLI reference. Removed: the exact org policy constraint id, "always on" and "high volume" log remarks, Key Access Justifications line, key-ring deletion claim, CMEK outage-in-minutes claim, and the list of resource types.
Method: documentation only; no commands were run.
