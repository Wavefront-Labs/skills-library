---
id: computing-software.cloud-infrastructure-engineering.google-cloud.customer-supplied-encryption-keys-csek
name: customer-supplied-encryption-keys-csek
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, encryption, csek, customer-supplied-encryption-keys, persistent-disk, cloud-storage, key-management]
level: advanced
status: docs-checked
description: "Encrypt Compute Engine disks and Cloud Storage objects with customer-supplied keys: key file formats, supplying keys on every use, rotation, and why CMEK is usually better."
sources: ["https://cloud.google.com/compute/docs/disks/customer-supplied-encryption", "https://cloud.google.com/storage/docs/encryption/customer-supplied-keys", "https://cloud.google.com/storage/docs/encryption/using-customer-supplied-keys"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Customer-supplied encryption keys (CSEK)

With CSEK you provide the key and Google does not store it on its servers. Lose the key and there
is no way for Google to recover the key or the data. Only choose CSEK when a requirement says keys
must be held entirely outside Google; otherwise consider **CMEK** (Cloud KMS / EKM).

## 1. Compute Engine disks
The key is a 256-bit string encoded in RFC 4648 standard base64.
```bash
openssl rand -base64 32       # 256-bit key; store it in your HSM/vault
cat > keys.json <<'EOF'
[{"uri": "https://www.googleapis.com/compute/v1/projects/<P>/zones/<Z>/disks/secure-data",
  "key": "<BASE64_KEY>", "key-type": "raw"}]
EOF
gcloud compute disks create secure-data --zone=<Z> --size=200GB --csek-key-file=keys.json
gcloud compute instances attach-disk vm1 --zone=<Z> --disk=secure-data --csek-key-file=keys.json
```
`key-type` is `raw` or `rsa-encrypted`. An RSA-wrapped key is wrapped with the public key
certificate Compute Engine provides (OAEP padding, not PKCS #1 v1.5), so only Google Cloud services
can unwrap it; the docs say to use `gcloud beta` for RSA-wrapped keys.
Starting or restarting a VM with CSEK disks: follow "Restarting a VM with an encrypted disk" in the Compute Engine CSEK page.

Snapshots: creating a snapshot from a CSEK disk needs the disk's key and the snapshot must also be
encrypted with a CSEK; snapshots of CSEK disks are always full, not incremental. Converting to
Google-managed keys means creating a new disk or snapshot.

## 2. Cloud Storage objects
```bash
gcloud storage cp report.pdf gs://<B>/report.pdf --encryption-key=<BASE64_KEY>
gcloud storage cp gs://<B>/report.pdf . --decryption-keys=<BASE64_KEY>
# rotate: supply the new key and the old key as the decryption key
gcloud storage objects update gs://<B>/report.pdf --encryption-key=<NEW> --decryption-keys=<OLD>
```
Cloud Storage keeps only a hash of the key, and uses the SHA256 in object metadata to pick the matching key.
Keys can only be set on individual objects, not as a bucket default, and the console cannot upload,
download or rotate CSEK objects.

## Limits that bite
- Compute Engine does not store encryption keys with instance templates, so a managed instance group cannot use CSEK disks directly; the docs point to keys in KMS for MIGs.
- Key loss is not recoverable by Google.

## Verify
- [ ] A disk or object created with the key cannot be read without it.
- [ ] Key backup and rotation runbook tested on a sandbox disk and object.

## Checked
2026-10-31. Confirmed against the Compute Engine CSEK page (256-bit base64 key, raw and rsa-encrypted types, RSA wrapping with OAEP, gcloud beta for RSA, instance templates, snapshot rules, key loss) and the two Cloud Storage CSEK pages (per-object only, console limits, SHA256 matching, `--encryption-key`, `--decryption-keys`, rotation command). Commands checked with check_commands.py. Removed unconfirmed claims: the list of services lacking CSEK support (Cloud SQL, GKE, BigQuery), autohealing, autoscaling, scheduled-start and live-migration behaviour, and the "needed on every start" statement.
Method: documentation only; no commands were run.
