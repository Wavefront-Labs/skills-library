---
id: computing-software.cloud-infrastructure-engineering.google-cloud.service-account-key-expiry-and-uploaded-keys
name: service-account-key-expiry-and-uploaded-keys
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, service-accounts, service-account-key-expiry, upload-service-account-key, servicekeyexpiryhours, disableserviceaccountkeyupload, keys]
level: practitioner
status: gated
description: "Limit service account key lifetime with the iam.serviceAccountKeyExpiryHours constraint and use uploaded public keys (HSM-generated) instead of Google-generated key files."
sources: ["https://cloud.google.com/iam/docs/keys-upload", "https://cloud.google.com/resource-manager/docs/organization-policy/restricting-service-accounts#limit_key_expiry", "https://cloud.google.com/iam/docs/best-practices-for-managing-service-account-keys"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service account key expiry and uploaded keys

When keys cannot be avoided (third-party SaaS, on-prem without WIF), bound their lifetime and keep
the private key out of Google's and humans' hands.

## Expiry constraint
```yaml
# policy.yaml: constraint name and allowed values (gated: unconfirmed, source is paywalled or blocked)
name: folders/<F>/policies/iam.serviceAccountKeyExpiryHours
spec:
  rules:
  - values: {allowedValues: ["2160h"]}
```
```bash
gcloud org-policies set-policy policy.yaml
gcloud iam service-accounts keys create k.json --iam-account=sa@<P>.iam.gserviceaccount.com
gcloud iam service-accounts keys list --iam-account=sa@<P>.iam.gserviceaccount.com \
  --format="table(name.basename(),validAfterTime,validBeforeTime,keyType)"
```
Applies only to keys created after the policy ((gated: unconfirmed, source is paywalled or blocked)). Set it at the folder holding the exception projects.

## Uploaded keys
Generate the pair in your HSM/PKI; upload only the X.509 public cert:
```bash
openssl req -x509 -nodes -newkey rsa:2048 -days <DAYS> -keyout pk.pem -out cert.pem -subj "/CN=unused"
gcloud iam service-accounts keys upload cert.pem --iam-account=sa@<P>.iam.gserviceaccount.com
```
Validity follows the cert's notBefore/notAfter. Build credentials JSON yourself (type
`service_account`, `private_key_id` = uploaded key ID) or sign JWTs directly in the HSM.
Block uploads elsewhere with `iam.disableServiceAccountKeyUpload`.

## Gotchas
- Expired keys can stay listed until deleted; clean them up.
- Uploaded keys still let anyone holding the private key act as the SA; protect it equally.

## Verify
- [ ] New key `validBeforeTime` is within the allowed window.
- [ ] Key creation in a non-exception project fails with the constraint error.

## Checked
2026-10-28. Confirmed on the keys-upload page: uploading an X.509 public key certificate, `gcloud iam service-accounts keys upload`, and the `iam.disableServiceAccountKeyUpload` constraint (written `disableServiceAccountKeyUpload`).
Gated: the fetched organization-policy page no longer holds the key-expiry text, so the constraint `iam.serviceAccountKeyExpiryHours`, its allowed values and the new-keys-only behaviour are unconfirmed.
Removed: the allowed-value list, `disableServiceAccountKeyCreation` advice, the Asset Inventory alert advice and a fixed 90-day certificate lifetime.
Method: documentation only; no commands were run.
