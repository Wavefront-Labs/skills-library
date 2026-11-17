---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-hsm-key-attestation-verification
name: cloud-hsm-key-attestation-verification
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-kms, hsm-attestation, cloud-hsm, fips-140, compliance-evidence]
level: advanced
status: docs-checked
description: "Prove a Cloud KMS key was generated in an HSM: download the attestation statement and certificate chains, verify them with Google's script, and parse key attributes for audits."
sources: ["https://cloud.google.com/kms/docs/attest-key"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud HSM key attestation verification

You verify an attestation to determine whether a key version was created inside an HSM. The attestation statement is produced by the HSM hardware (all Cloud HSM devices are made by Marvell, formerly Cavium) and signed by certificates owned by Google and by the HSM manufacturer.

## 1. Download
```bash
gcloud kms keys versions describe 1 --key=payments --keyring=prod --location=us-east1 \
  --attestation-file=attestation.dat
gcloud kms keys versions get-certificate-chain 1 --key=payments --keyring=prod --location=us-east1 \
  --output-file=certs.pem
```
Console: Key Management > key > key version menu > **Verify attestation**. "Open Cloud Shell" pre-populates the whole verification, or "Download Attestation Bundle" gives a zip with the attestation and certificate chains.

## 2. Verify signatures
Use Google's open-source Python attestation script (linked from the attest-key page) with the attestation file and certificates. Do not use the manufacturer's `verify_attest.py`; the page says to use Google's verification script instead. Read the script's source to learn the format.

## 3. Parse attributes
Download the manufacturer's `verify_pubkey.py`, `parse_v1.py` and `parse_v2.py` (the page links them). The attestation is compressed; decompress first: `gzip -d < compressed_attestation.dat > attestation.dat`. In the parsed output:
- `0x0162` field: extractable? `\x00` is false; Cloud HSM keys are not extractable.
- `0x0163` field: `\x01` = created locally on the HSM, `\x00` = imported (expected for imported keys; the key was wrapped in transit by the import job's wrapping key).
- `0x0100` field: key type, PKCS #11 `CKK_*` values (an AES key is `\x1f`).
- `0x0102` key ID field: two concatenated SHA-256 digests in hex; the second must match the SHA-256 of the key version resource name `projects/PROJECT_ID/locations/LOCATION/keyRings/KEY_RING/cryptoKeys/KEY_NAME/cryptoKeyVersions/KEY_VERSION`. The key ID is hex-encoded twice in the parsed dump, so decode one layer before comparing.
- For an asymmetric key, the manufacturer's `verify_pubkey.py` checks the public key against the attestation.

## Gotchas
- Manual `openssl` handling fails on the compressed attestation; run `gzip -d` first.
- Imported keys show the imported attribute; that is expected for BYOK.

## Verify
- [ ] The script reports the chains valid and the parsed attributes show non-extractable; archive the attestation, chain and script output as audit evidence.

## Checked
2026-10-31. Confirmed against the Cloud KMS "Verify attestations" page: gcloud commands and `--attestation-file`/`--output-file`, console path, the Marvell statement, the three manufacturer scripts and the warning about `verify_attest.py`, `gzip -d`, fields 0x0100/0x0102/0x0162/0x0163 and their values. Removed: `OBJ_ATTR_*` attribute names and the "both manufacturer and Google owner roots" fingerprint wording (not on the page), `--certificate-chain-type`, the claim that only HSM keys have attestations, and the `get-public-key` comparison. The parse-hsm-attestation URL returned 404.
Method: documentation only; no commands were run.
