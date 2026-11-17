---
id: computing-software.cloud-infrastructure-engineering.docker.github-artifact-attestations-for-images
name: github-artifact-attestations-for-images
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, provenance, attest-build-provenance, gh-attestation, slsa, github-actions, sigstore]
level: practitioner
status: docs-checked
description: "Generate signed SLSA build provenance for container images with actions/attest-build-provenance, push it to the registry, and verify with gh attestation verify."
sources: ["https://github.com/actions/attest", "https://github.com/actions/attest-build-provenance", "https://github.com/actions/attest-sbom", "https://github.com/cli/cli/blob/trunk/pkg/cmd/attestation/verify/verify.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GitHub artifact attestations for images

GitHub can sign a SLSA provenance statement for an image digest using Sigstore (public repos)
or GitHub's own Sigstore instance (private repos), tying the image to the workflow, commit
and runner that built it.

## Workflow
```yaml
permissions:
  contents: read
  packages: write
  id-token: write          # OIDC for signing
  attestations: write      # store attestation in GitHub
  artifact-metadata: write # create the artifact storage record
steps:
  - uses: docker/login-action@v3
    with: { registry: ghcr.io, username: ${{ github.actor }}, password: ${{ secrets.GITHUB_TOKEN }} }
  - uses: docker/setup-buildx-action@v3
  - id: push
    uses: docker/build-push-action@v6
    with:
      push: true
      tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
  - uses: actions/attest@v4                            # attest-build-provenance v4 is a wrapper over actions/attest
    with:
      subject-name: ghcr.io/${{ github.repository }}     # fully qualified name, no tag
      subject-digest: ${{ steps.push.outputs.digest }}
      push-to-registry: true                             # also push the attestation to the registry
```
With no `sbom-path` or predicate inputs `actions/attest` generates SLSA build provenance; pass
`sbom-path` (SPDX or CycloneDX) for an SBOM attestation or `predicate-type` plus a predicate for a
custom one. `actions/attest-build-provenance` and `actions/attest-sbom` still work as wrappers, but
new workflows should use `actions/attest`.

## Verify
```bash
gh attestation verify oci://ghcr.io/org/app:<tag> --owner org
gh attestation verify oci://ghcr.io/org/app@sha256:<digest> --repo org/app \
  --signer-workflow org/app/.github/workflows/release.yml
gh attestation verify oci://ghcr.io/org/app:<tag> --owner org --format json
```
Offline/air-gapped: `gh attestation download`, then `gh attestation verify --bundle <file>` with
`--custom-trusted-root <trusted_root.jsonl>`; `--bundle-from-oci` reads the bundle from the registry
instead of GitHub.

## Relationship to BuildKit provenance
- BuildKit `--provenance=mode=max` records detailed build inputs but is unsigned (trust
  comes from whoever controls the registry).
- GitHub attestations are signed by an identity bound to the workflow, which is what admission
  policies need. Many teams emit both.

## Gotchas
- `subject-name` must not include a tag; the digest is the subject.
- Artifact attestations in private or internal repositories need GitHub Enterprise Cloud; public repositories work on all current plans. They are not supported on GitHub Enterprise Server.
- Public repositories sign with the public-good Sigstore instance, private ones with GitHub's private Sigstore instance, so verifiers must trust the matching root.
- `gh attestation verify` enforces predicate type `https://slsa.dev/provenance/v1` by default; use `--predicate-type` for SBOM attestations.

## Checked
Documentation release: actions/attest v4.2.2 and actions/attest-build-provenance v4.2.2 READMEs, actions/attest-sbom README, and cli/cli `gh attestation verify` source (pkg/cmd/attestation/verify/verify.go), checked 2026-10-26.
Confirmed: `id-token`, `attestations` and `artifact-metadata` permissions; inputs `subject-name`, `subject-digest`, `push-to-registry`, `sbom-path`, `predicate-type`; Sigstore public-good vs private instance; plan restrictions; `gh attestation verify` flags `--owner`, `--repo`, `--signer-workflow`, `--bundle`, `--bundle-from-oci`, `--custom-trusted-root`, `--predicate-type` (default SLSA provenance v1).
Corrected: the action is now `actions/attest` (v4; the other two are wrappers, attest-sbom deprecated); added the `artifact-metadata: write` permission; removed the `jq` buildDefinition path, `gh attestation trusted-root` verify usage and admission-controller claims as unsupported.
Method: documentation only; no commands were run.
