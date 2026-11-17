---
id: computing-software.devops-ci-cd.secrets-management.cosign-key-pair-and-kms-signing
name: cosign-key-pair-and-kms-signing
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, artifact-signing, cosign, cosign-key-pair, cosign-kms, aws-kms, gcp-kms, azure-key-vault, hashivault-transit, generate-key-pair, private-signing, air-gapped-signing, key-rotation]
level: advanced
status: gated
description: "Sign with cosign using managed keys: generate-key-pair, KMS URIs for AWS/GCP/Azure/Vault, CI permissions, verifying with the public key, private-tlog choices and key rotation."
sources: ["https://docs.sigstore.dev/cosign/key_management/signing_with_self-managed_keys/", "https://docs.sigstore.dev/cosign/key_management/overview/", "https://github.com/sigstore/cosign/blob/main/KMS.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cosign with key pairs and KMS

Use keys instead of keyless when: the environment is air-gapped or can't reach public
Sigstore, identities must not appear in a public log, or policy requires HSM-held keys.

## Local key pair (bootstrap / small teams)
```bash
COSIGN_PASSWORD=... cosign generate-key-pair      # cosign.key (encrypted), cosign.pub
cosign sign --key cosign.key registry.example.com/app@sha256:...
cosign verify --key cosign.pub registry.example.com/app@sha256:...
```
Run on cosign v3.1.3 against a local registry (`crane registry serve`, add `--allow-insecure-registry` for plain-HTTP localhost): sign, verify and
`env://` keys all worked; v3 defaults to the new bundle format, stored as an OCI referrer (`cosign tree` shows it).
In CI store `cosign.key` + `COSIGN_PASSWORD` as secrets (`--key env://COSIGN_PRIVATE_KEY`
reads it from an env var). Weakest option: whoever gets the CI secret can sign.
`cosign generate-key-pair k8s://ns/secret-name` writes into a Kubernetes Secret.

## KMS-held keys (preferred)
The private key never leaves the KMS; CI needs only *sign* permission.
```bash
# create
cosign generate-key-pair --kms awskms:///alias/cosign-release
cosign generate-key-pair --kms gcpkms://projects/p/locations/global/keyRings/r/cryptoKeys/cosign
cosign generate-key-pair --kms azurekms://my-vault.vault.azure.net/cosign
cosign generate-key-pair --kms hashivault://cosign          # Vault transit engine
# sign / verify
cosign sign   --key awskms:///alias/cosign-release registry.example.com/app@sha256:...
cosign verify --key awskms:///alias/cosign-release registry.example.com/app@sha256:...
cosign public-key --key awskms:///alias/cosign-release > cosign.pub   # distribute to verifiers
```
- (gated: unconfirmed, no cloud account; `generate-key-pair --help` lists the `awskms://`, `gcpkms://`, `azurekms://` and `hashivault://` forms)
- AWS: key spec `ECC_NIST_P256` or RSA, usage `SIGN_VERIFY`. CI role needs
  `kms:Sign`, `kms:GetPublicKey`, `kms:DescribeKey`; verifiers need only the public key
  file (no KMS access).
- GCP: `roles/cloudkms.signerVerifier` for CI; Azure: key permissions sign/verify/get.
- Authenticate CI to the cloud with OIDC federation, not static keys, so no long-lived
  secret exists anywhere.

## Transparency log
By default signatures are still uploaded to public Rekor (v3 uses a signing config; verified OK with the transparency log). For private use on v3,
`--tlog-upload=false` is deprecated and is rejected unless combined with `--use-signing-config=false` (or pass a `--signing-config` file without Rekor URLs);
verify with `--insecure-ignore-tlog=true` (without it: `not enough verified log entries from transparency log: 0 < 1`)
(you lose tamper-evident timestamps; consider a private Rekor/TSA instead, `--rekor-url`,
`--timestamp-server-url`).

## Rotation
1. Create the new KMS key, publish both public keys to verifiers/admission policy (allow
   either).
2. Switch CI to the new key.
3. After all running images were re-signed or rotated out, remove the old public key from
   policy. Don't delete the old KMS key until no artifact you must verify depends on it.

## Verify
`cosign verify --key cosign.pub` succeeds for a fresh image. `cosign tree <image>` lists the signature (`cosign triangulate` still
prints the legacy `.sig` tag but is deprecated, removal planned for v4). An image verified with a different public key fails; on v3.1.3 the
message is `no matching attestations: ... accepted signatures do not match threshold, Found: 0, Expected 1` (older versions: `no matching signatures`).
