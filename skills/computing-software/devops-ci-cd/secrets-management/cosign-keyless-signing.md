---
id: computing-software.devops-ci-cd.secrets-management.cosign-keyless-signing
name: cosign-keyless-signing
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, artifact-signing, cosign, cosign-sign-keyless, keyless-signing, sigstore, fulcio, rekor, oidc, certificate-identity, certificate-oidc-issuer, github-actions-oidc, gitlab-id-token, sign-by-digest]
level: advanced
status: gated
description: "Sign container images keylessly with cosign in CI: OIDC to Fulcio, Rekor transparency log, signing by digest, and verifying with exact certificate identity and issuer."
sources: ["https://docs.sigstore.dev/cosign/signing/overview/", "https://docs.sigstore.dev/cosign/verifying/verify/", "https://docs.sigstore.dev/certificate_authority/oidc-in-fulcio/", "https://github.com/sigstore/cosign-installer"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keyless signing with cosign

**How it works:** the CI job's OIDC token proves its identity to **Fulcio**, which issues
a ~10-minute X.509 certificate binding an ephemeral key to that identity (e.g. the
workflow path and ref). cosign signs, uploads the signature to the registry, and records
it in the **Rekor** transparency log. No long-lived key to leak or rotate.

## GitHub Actions
```yaml
permissions:
  contents: read
  packages: write
  id-token: write            # required for the OIDC token
steps:
  - uses: sigstore/cosign-installer@v4      # latest release v4.1.2 (not run in Actions: gated: unconfirmed)
  - id: build
    uses: docker/build-push-action@v7
    with: { push: true, tags: "ghcr.io/acme/api:${{ github.sha }}" }
  - run: cosign sign --yes "ghcr.io/acme/api@${{ steps.build.outputs.digest }}"
```
- **Sign the digest**, never a tag: tags move, and `cosign sign image:tag` warns because
  you might sign something else than you built.
- `--yes` skips the interactive Rekor upload confirmation.

## GitLab CI
```yaml
sign:
  image: alpine:3.20
  id_tokens:
    SIGSTORE_ID_TOKEN: { aud: sigstore }
  script:
    - apk add --no-cache cosign
    - cosign sign --yes "$CI_REGISTRY_IMAGE@$IMAGE_DIGEST"
```
cosign picks up `SIGSTORE_ID_TOKEN` automatically (GitLab docs show `aud: sigstore` and require cosign >= 2.0.1; the `alpine:3.20` `apk add cosign` version was not checked: gated: unconfirmed).

## Verify (the important half)
```bash
cosign verify ghcr.io/acme/api@sha256:... \
  --certificate-identity "https://github.com/acme/api/.github/workflows/release.yml@refs/heads/main" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com"
# regex variants for tags/branches:
#   --certificate-identity-regexp '^https://github.com/acme/api/.github/workflows/release.yml@refs/tags/v'
```
GitLab issuer: `https://gitlab.com`; identity is the project path + ref
(`https://gitlab.com/acme/api//.gitlab-ci.yml@refs/heads/main`). Without pinning
identity *and* issuer, any Sigstore user's signature would pass: verification must
answer "signed by *our* release workflow on *main*", not "signed by someone".

Enforce at deploy with an admission policy (Kyverno `verifyImages` / Sigstore
policy-controller) using the same identity constraints.

## Gotchas
- `getting signer: ... id-token` errors: missing `id-token: write` (GitHub) or `id_tokens`
  (GitLab); fork PRs get no OIDC token.
- Private projects: Rekor entries are **public** (they include the workflow identity and
  repo name). If that leaks sensitive names, use a private Sigstore deployment or
  key-based signing (`--tlog-upload=false` has its own verification implications).
- cosign v2+ defaults to keyless when no `--key` is given; older pipelines with
  `COSIGN_EXPERIMENTAL=1` can drop it.
- Registry must accept OCI artifacts/tags `sha256-<digest>.sig` (or referrers with newer
  cosign bundle formats).

## Verify it works
Run on cosign 3.1.3 against the real keyless-signed `cgr.dev/chainguard/static:latest`: with `--certificate-identity-regexp 'https://github.com/chainguard-images/images/.*'` and the GitHub issuer it exits 0 (claims validated, Rekor entry verified offline, certificate chain verified);
with no identity flag: `--certificate-identity or --certificate-identity-regexp is required for verification in keyless mode`;
with a wrong identity or issuer: `no matching signatures: none of the expected identities matched what was in the certificate, got subjects [...] with issuer ...`.
Signing with the GitHub/GitLab OIDC token was not run (gated: unconfirmed, needs a CI identity).
