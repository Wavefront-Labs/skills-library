---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cosign-signing-keys-in-kms
name: cosign-signing-keys-in-kms
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, image-security, cosign-kms, cosign, sigstore, kms]
level: practitioner
status: docs-checked
description: "Keep cosign signing keys in AWS KMS, GCP KMS, Azure Key Vault or Vault, sign images from CI without key files, and verify with the public key."
sources: ["https://docs.sigstore.dev/cosign/key_management/overview/", "https://docs.sigstore.dev/cosign/signing/signing_with_containers/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cosign keys in a KMS

A key file on a CI runner can be stolen and used forever. With a KMS the private key never
leaves the service; CI gets permission to call Sign.

## Create the key
```bash
cosign generate-key-pair --kms awskms:///alias/cosign-prod
cosign generate-key-pair --kms gcpkms://projects/<p>/locations/global/keyRings/<r>/cryptoKeys/cosign
cosign generate-key-pair --kms azurekms://[VAULT_NAME][VAULT_URI]/[KEY]
cosign generate-key-pair --kms hashivault://cosign          # Vault transit engine
```
Or create an asymmetric signing key in the KMS yourself (the Sigstore AWS example uses key usage
`SIGN_VERIFY`) and reference it. Signing and verifying URIs for GCP end in
`/cryptoKeys/<key>/versions/<version>`.

## Sign in CI
```bash
cosign sign --yes --key awskms:///alias/cosign-prod registry.internal/app@sha256:<digest>
```
Sign by digest, not tag. Give the CI identity only what signing needs. On GCP the Sigstore docs list a KMS viewer role plus
`roles/cloudkms.signerVerifier`; on Azure the `Key Vault Crypto User` role can sign. For AWS check the
KMS key policy documentation for the exact signing and public-key actions.

## Verify
```bash
cosign public-key --key awskms:///alias/cosign-prod > cosign.pub
cosign verify --key cosign.pub registry.internal/app@sha256:<digest>
```
Distribute `cosign.pub` to admission policy (Kyverno image verification, Sigstore policy-controller)
so verification needs no KMS access.

## Rotation
Create a new key, sign new images with it, and trust both public keys in admission until all
running images are re-signed; then remove the old key.

## Gotchas
- Keyless signing (Fulcio + OIDC) is the alternative when you do not want to manage keys at all.

## Checked

Checked 2026-10-27 against the Sigstore docs source (sigstore/docs, `cosign/key_management/overview` and `cosign/signing/signing_with_containers`) and the cosign CLI reference.

- KMS URI schemes `awskms://`, `gcpkms://`, `azurekms://`, `hashivault://` (also `openbao://`, `ovhcloud://`, `k8s://`), the AWS three-slash form `awskms:///alias/...`, `cosign generate-key-pair --kms`, `cosign public-key --key`, `cosign sign --key` and `cosign verify --key` confirmed.
- Azure URI format `azurekms://[VAULT_NAME][VAULT_URI]/[KEY]` and roles (Key Vault Crypto Officer to create, Crypto User to sign) confirmed; GCP URI with `/versions/<n>` and role `roles/cloudkms.signerVerifier` confirmed.
- Removed unconfirmed claims: exact AWS IAM actions, ECDSA P-256 key type, KMS throttling, and Connaisseur.

Method: documentation only; no commands were run.
