---
id: computing-software.cloud-infrastructure-engineering.cert-manager.signature-verification
name: signature-verification
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [cosign, signature, helm-verify, gpg, supply-chain, public-key]
level: practitioner
status: docs-checked
description: "Verify cert-manager container images with cosign and Helm charts with a GPG keyring, using the published public keys."
sources:
  - https://cert-manager.io/docs/installation/code-signing/
  - https://cert-manager.io/docs/installation/helm/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Container images (signed from v1.8.0) live on Quay: `quay.io/jetstack/cert-manager-controller`, `-webhook`, `-cainjector`, `-acmesolver`, `-startupapicheck`.

Set `KEY=https://cert-manager.io/public-keys/cert-manager-pubkey-2021-09-20.pem` and `IMAGE_TAG` to the release tag, then per image:

`cosign verify --signature-digest-algorithm sha512 --insecure-ignore-tlog --key $KEY quay.io/jetstack/<image-name>:$IMAGE_TAG`

`--insecure-ignore-tlog` skips transparency-log checks; the project says it would like to drop it later. Verification uses a static key, not a certificate identity or OIDC issuer. The signing key sits in Google Cloud KMS and is used by Google Cloud Build only when a release is signed.

Helm charts (signed from v1.6.0) use PGP. Helm needs a GPG keyring; a plain PEM key fails. Use the keyring `cert-manager-keyring-2021-09-20-1020CF3C033D4F35BAE1C19E1226061C665DF13E.gpg` from `cert-manager.io/public-keys/`:

`helm verify --keyring <keyring>.gpg /path/to/cert-manager-vx.y.z.tgz`

The ASCII-armored key is the `.asc` with the same key ID. When installing from the OCI chart, pass `--verify --keyring <file>` to `helm install`.

At the time of writing all signing uses the same underlying key.

## Checked

2026-11-03: Confirmed against the Signature Verification page: images signed from v1.8.0 and the five Quay image names, the key URL and `cosign verify` flags, the `--insecure-ignore-tlog` explanation and Google Cloud KMS note, Helm charts signed from v1.6.0 with PGP, the GPG keyring name, `helm verify --keyring`, the ASCII-armored `.asc` key, and the single underlying key note. The `--verify --keyring` use with `helm install` is shown on the Helm installation page, added to sources. Nothing removed.

Method: documentation only; no commands were run.
