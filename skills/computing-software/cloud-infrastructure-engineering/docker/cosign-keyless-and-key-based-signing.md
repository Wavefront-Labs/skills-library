---
id: computing-software.cloud-infrastructure-engineering.docker.cosign-keyless-and-key-based-signing
name: cosign-keyless-and-key-based-signing
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, cosign, sigstore, image-signing, cosign-keyless, fulcio, rekor, cosign-key, cosign-verify, kms]
level: advanced
description: "Sign images by digest with cosign keyless (OIDC, Fulcio, Rekor) or with key pairs and cloud KMS keys, and verify with identity and issuer constraints."
sources: ["https://docs.sigstore.dev/cosign/signing/signing_with_containers/", "https://docs.sigstore.dev/cosign/verifying/verify/", "https://docs.sigstore.dev/cosign/key_management/overview/", "https://github.com/sigstore/cosign-installer", "https://github.com/sigstore/cosign/blob/main/doc/cosign_sign.md"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# cosign keyless and key-based signing

Always sign the **digest**, never a tag: `cosign sign reg/app@sha256:...`. Signing a tag
signs whatever it pointed to at that moment and cosign warns.

## Keyless (Sigstore public good or private Fulcio/Rekor)
```yaml
# GitHub Actions
permissions: { id-token: write, packages: write, contents: read }
steps:
  - uses: sigstore/cosign-installer@v4.1.0
  - run: cosign sign --yes ghcr.io/org/app@${{ steps.build.outputs.digest }}
```
Flow: keyless signing authenticates with an OIDC provider (the Sigstore docs name Google, GitHub and Microsoft; in CI the ambient workflow token is used) and signs with an ephemeral key. The signature is stored in the registry using the OCI 1.1 referrer specification; `cosign tree` shows it.

Verify by identity, not by key:
```sh
cosign verify ghcr.io/org/app@sha256:... \
  --certificate-identity-regexp '^https://github.com/org/app/\.github/workflows/release\.yml@refs/tags/v' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
```
Loose regexes (`.*`) make verification meaningless - anyone with a GitHub workflow passes.

## Key pairs
```sh
cosign generate-key-pair                          # cosign.key (encrypted) + cosign.pub
COSIGN_PASSWORD=... cosign sign --key cosign.key reg/app@sha256:...
cosign verify --key cosign.pub reg/app@sha256:...
```
Offline/air-gapped: `--tlog-upload=false` when signing and `--insecure-ignore-tlog` when
verifying (you lose transparency; accept consciously).

## KMS keys
```sh
cosign generate-key-pair --kms awskms:///alias/cosign-release
cosign sign --key awskms:///alias/cosign-release reg/app@sha256:...
cosign verify --key awskms:///alias/cosign-release reg/app@sha256:...
```
Also `gcpkms://projects/<project>/locations/global/keyRings/<ring>/cryptoKeys/<key>/versions/<n>`, `azurekms://<vault-name><vault-uri>/<key>`,
`hashivault://<key>`, `openbao://<key>`, `k8s://<namespace>/<secret>` and `env://<VAR>`. KMS permissions decide who can sign (for Google Cloud the docs name `roles/cloudkms.signerVerifier`).

## Annotations and attestations
`cosign sign -a git_sha=$GITHUB_SHA ...` adds signed annotations; verify with `-a git_sha=...`.
`cosign attest --predicate sbom.json --type spdxjson` signs an in-toto attestation;
`cosign verify-attestation --type spdxjson ...`.

## Gotchas
- Signatures live in the image's repository (or `COSIGN_REPOSITORY`), so plain image copies need the signature artifacts copied too.
- The signer needs push rights because the signature is pushed to the registry.
- `cosign sign --bundle <file> --upload=false` writes the verification material to a Sigstore bundle instead of pushing; upload it later with `oras attach --artifact-type=application/vnd.dev.sigstore.bundle.v0.3+json`.
- Pin the cosign version in CI (`cosign-release` input of the installer).

## Verify
`cosign tree reg/app@sha256:...` lists the signature and attestations; `cosign verify` fails unless the identity and issuer flags match the certificate.

## Checked
Documentation release: cosign v3.1.4 CLI reference, cosign-installer v4.1.2 README and docs.sigstore.dev (sigstore/docs main), checked 2026-10-26.
Confirmed: `cosign sign` flags `--key`, `-a`, `-r/--recursive`, `--bundle`, `--upload`, `--yes`; KMS URI forms from the signing-containers page; `cosign verify` flags `--certificate-identity-regexp`, `--certificate-oidc-issuer`, `--insecure-ignore-tlog`; `--tlog-upload=false` appears in the sign examples; OCI 1.1 referrer storage; `cosign tree`.
Corrected: installer pin moved from `@v3` to the README's `@v4.1.0`; removed the 10-minute certificate lifetime, Rekor flow detail, `cosign copy`, "v2 changed defaults" and `jq` Subject claims as unsupported; KMS URI examples aligned with the docs.
Method: documentation only; no commands were run.
