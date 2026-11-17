---
id: computing-software.database-administration.cloudnative-pg.verify-release-assets-cosign-sbom
name: verify-release-assets-cosign-sbom
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [supply-chain, cosign, sbom, slsa, provenance, signature, verification]
level: advanced
status: docs-checked
description: "Verify CloudNativePG release manifests, operator images and PostgreSQL operand images with cosign, slsa-verifier and docker buildx imagetools for signatures, SBOM and provenance."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/installation_upgrade.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Official release assets are signed. You need the `cosign` CLI for signatures and Docker Buildx for SBOM and provenance.

Operator manifest, using the `.sigstore.json` bundle from the GitHub release page:

```bash
cosign verify-blob \
  cnpg-{version}.yaml \
  --bundle cnpg-{version}.sigstore.json \
  --certificate-identity-regexp "^https://github.com/cloudnative-pg/cloudnative-pg/.github/workflows/release-publish.yml@refs/tags/v" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com"
```

Release binary SLSA provenance (download the artifact and `multiple.intoto.jsonl`):

```shell
slsa-verifier verify-artifact <ARTIFACT> \
  --provenance-path multiple.intoto.jsonl \
  --source-uri github.com/cloudnative-pg/cloudnative-pg
```

Operator image: `cosign verify ghcr.io/cloudnative-pg/cloudnative-pg:{tag}` with the same identity regexp and issuer. Operand (PostgreSQL) images come from the `postgres-containers` project, so the identity regexp differs:

```bash
cosign verify ghcr.io/cloudnative-pg/postgresql:{tag} \
  --certificate-identity-regexp="^https://github.com/cloudnative-pg/postgres-containers/" \
  --certificate-oidc-issuer="https://token.actions.githubusercontent.com"
```

Inspect attestations with `docker buildx imagetools inspect <image> --format '{{ json (index .SBOM "linux/amd64").SPDX }}'` for the SPDX SBOM, or `(index .Provenance "linux/amd64").SLSA` for build provenance.

In short, three identities apply: the `release-publish.yml` workflow of the `cloudnative-pg` repository for the manifest and operator image, the `multiple.intoto.jsonl` provenance for release binaries, and the `postgres-containers` repository for PostgreSQL operand images.

## Checked

2026-11-04. cosign, slsa-verifier and buildx commands with their certificate identity patterns confirmed on the Installation and upgrades page, section Verifying release assets.

Method: documentation only; no commands were run.
