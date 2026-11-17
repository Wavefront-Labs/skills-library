---
id: computing-software.cybersecurity-defensive.application-security.artifact-signing-sigstore
name: artifact-signing-sigstore
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [supply-chain-security, artifact-signing, sigstore, cosign, slsa-provenance, keyless-signing, verification-policy]
level: advanced
status: docs-checked
description: "Sign container images with Sigstore cosign (keyless OIDC or KMS keys), attach provenance and SBOM attestations and verify with pinned identity and issuer."
sources: ["https://docs.sigstore.dev/cosign/signing/overview/", "https://docs.sigstore.dev/cosign/signing/signing_with_containers/", "https://docs.sigstore.dev/cosign/verifying/verify/", "https://github.com/sigstore/cosign/blob/main/doc/cosign_attest.md", "https://github.com/sigstore/cosign/blob/main/doc/cosign_verify.md", "https://github.com/sigstore/cosign/blob/main/doc/cosign_generate-key-pair.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Artefact signing with Sigstore

**Goal:** consumers can verify an artefact was built by your CI from your repo, unmodified.

## Keyless signing
Keyless signing associates an identity, not a key, with the signature: Fulcio issues a short-lived certificate binding an ephemeral key to an OpenID Connect identity, and signing events are logged in Rekor, a transparency log. In CI, run `cosign sign` against the image **digest** (`registry/app@sha256:...`), not a tag, with the CI platform's OIDC identity token available to the job (see the signing docs for your CI).

## Key-based (KMS)
`cosign generate-key-pair --kms <provider>://...` creates the key pair in the KMS (providers include AWS, Azure, GCP and HashiCorp Vault), then `cosign sign --key <kms uri> <image@digest>`.

## Attestations
- `cosign attest --predicate <file> --type <type> <image@digest>` where `--type` is one of `slsaprovenance`, `slsaprovenance02`, `slsaprovenance1`, `link`, `spdx`, `spdxjson`, `cyclonedx`, `vuln`, `openvex` or `custom` (the default), or a URI.
- Example: `--type cyclonedx --predicate sbom.json` for an SBOM, `--type slsaprovenance --predicate provenance.json` for provenance.

## Verification
Keyless verification must pin both the expected identity and issuer:
```
cosign verify ghcr.io/org/app@sha256:... \
  --certificate-identity-regexp '^https://github.com/org/app/' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
```
`--certificate-identity` (or `-regexp`) and `--certificate-oidc-issuer` (or `-regexp`) are required for keyless flows. With a key, use `cosign verify --key <key path|url|kms uri> <image>`. By default cosign checks that the signature payload digest matches the image.

## Gotchas
- Verifying without pinning identity and issuer would accept anyone's valid Sigstore signature; cosign requires them for keyless flows.
- Sign digests: the signature payload records the image digest, and tags are mutable.
- Enforce verification at deploy time with an admission or policy tool of your choice and test that it blocks an unsigned image (not covered by the sources above; check that tool's docs).

## Verify
- [ ] `cosign verify` with identity constraints succeeds for releases and fails for an unsigned test image.
- [ ] Admission policy blocks unsigned images in a staging namespace test.

## Checked
2026-11-01 against the Sigstore docs (signing overview, signing with containers, verifying) and the cosign reference pages for attest, verify and generate-key-pair: confirmed Fulcio short-lived certificates bound to OIDC identity, Rekor logging, `--kms` on generate-key-pair, `--key` with KMS URIs for sign, the full list of attest `--type` values, `--certificate-identity(-regexp)` and `--certificate-oidc-issuer` being required for keyless verify, and the digest check. Removed: workflow YAML (permissions, installer action version), the GitHub attest-build-provenance action and `gh attestation verify`, Kyverno and policy-controller claims, npm and PyPI provenance, the SLSA and GitHub Docs citations and the public Rekor privacy note (none fetched).
Method: documentation only; no commands were run.
