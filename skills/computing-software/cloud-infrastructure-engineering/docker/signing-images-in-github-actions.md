---
id: computing-software.cloud-infrastructure-engineering.docker.signing-images-in-github-actions
name: signing-images-in-github-actions
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, image-signing, sign-in-ci, cosign-installer, cosign-keyless, github-actions, oidc]
level: practitioner
status: docs-checked
description: "Sign every pushed image digest keylessly in GitHub Actions with sigstore/cosign-installer and the workflow's OIDC identity, then verify the identity policy consumers will use."
sources: ["https://github.com/sigstore/cosign-installer", "https://docs.sigstore.dev/cosign/signing/signing_with_containers/", "https://docs.sigstore.dev/cosign/verifying/verify/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Signing images in GitHub Actions

## Workflow
```yaml
permissions:
  contents: read
  packages: write
  id-token: write                 # lets cosign get a Fulcio certificate for this workflow
jobs:
  release:
    runs-on: ubuntu-24.04
    steps:
      - uses: sigstore/cosign-installer@v4.1.0
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with: { registry: ghcr.io, username: ${{ github.actor }}, password: ${{ secrets.GITHUB_TOKEN }} }
      - id: meta
        uses: docker/metadata-action@v5
        with: { images: ghcr.io/${{ github.repository }} }
      - id: build
        uses: docker/build-push-action@v6
        with: { push: true, tags: ${{ steps.meta.outputs.tags }}, labels: ${{ steps.meta.outputs.labels }} }
      - name: Sign
        env:
          DIGEST: ${{ steps.build.outputs.digest }}
          TAGS: ${{ steps.meta.outputs.tags }}
        run: |
          images=""
          for t in $TAGS; do images="$images ${t}@${DIGEST}"; done
          cosign sign --yes $images
```
Signing `tag@digest` records the tag for humans while the signature binds to the digest.

## Verify like a consumer
```bash
cosign verify ghcr.io/org/app:1.4.0 \
  --certificate-identity-regexp '^https://github.com/org/app/\.github/workflows/release\.yml@refs/(heads/main|tags/v.*)$' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
```
Add this exact step after signing in CI so a broken identity policy fails the release, not
production admission.

## Key-based alternative
```yaml
      - run: cosign sign --yes --key env://COSIGN_PRIVATE_KEY "$IMAGE@$DIGEST"
        env:
          COSIGN_PRIVATE_KEY: ${{ secrets.COSIGN_PRIVATE_KEY }}
          COSIGN_PASSWORD: ${{ secrets.COSIGN_PASSWORD }}
```
Or a KMS URI such as `awskms://[ENDPOINT]/[ID/ALIAS/ARN]`, `gcpkms://...`, `azurekms://...`, `hashivault://...`.

## Gotchas
- `id-token: write` is required for the workflow to obtain the GitHub OIDC token (the installer README sets it for signing).
- Sign after push and only the digest you pushed.
- Sign only on trusted refs (main and tags), not on pull request builds.

## Checked
Documentation release: cosign-installer v4.1.2 README (its example uses `sigstore/cosign-installer@v4.1.0`, `permissions: id-token: write`, and the `${tag}@${DIGEST}` loop with `cosign sign --yes`), docker/build-push-action v6 and cosign v3.1.4 reference, checked 2026-10-26.
Confirmed: the sign loop, `--key env://COSIGN_PRIVATE_KEY` with `COSIGN_PASSWORD`, `--certificate-identity-regexp` and `--certificate-oidc-issuer` verify flags, KMS URI forms.
Corrected: installer pin `@v3` to `@v4.1.0`; removed the exact OIDC error text, reusable-workflow identity, fork-PR and re-tagging claims and the `jq` output filter as unsupported by the docs.
Method: documentation only; no commands were run.
