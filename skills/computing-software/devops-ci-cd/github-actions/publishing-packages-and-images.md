---
id: computing-software.devops-ci-cd.github-actions.publishing-packages-and-images
name: publishing-packages-and-images
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, publish-package, github-packages, ghcr, ghcr-io, docker-build-push-action, metadata-action, docker-login-action, setup-buildx-action, npm-publish, pypi-trusted-publishing, pypa-gh-action-pypi-publish, maven-publish, nuget-publish, release-assets, packages-write, package-visibility, package-permissions, link-package-to-repo, image-tags, oci-labels, multi-arch-images, provenance, sbom-attestation, retention-cleanup]
level: practitioner
status: draft
description: "Publish from GitHub Actions: GHCR images with metadata-action tags and multi-arch buildx, npm/PyPI trusted publishing, Maven/NuGet to GitHub Packages, release assets, cleanup."
sources: ["https://docs.github.com/en/actions/use-cases-and-examples/publishing-packages/publishing-docker-images", "https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry", "https://github.com/docker/build-push-action", "https://github.com/docker/metadata-action", "https://docs.pypi.org/trusted-publishers/", "https://docs.github.com/en/actions/use-cases-and-examples/publishing-packages/publishing-nodejs-packages"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Publishing packages and images

**Goal:** one workflow that builds once, tags consistently (semver + sha), pushes to the
right registry with the minimum token, and attaches provenance.

## 1. Container images to GHCR
```yaml
permissions: { contents: read, packages: write, id-token: write, attestations: write }
steps:
  - uses: docker/setup-qemu-action@v3          # only for multi-arch
  - uses: docker/setup-buildx-action@v3
  - uses: docker/login-action@v3
    with: { registry: ghcr.io, username: ${{ github.actor }}, password: ${{ secrets.GITHUB_TOKEN }} }
  - id: meta
    uses: docker/metadata-action@v5
    with:
      images: ghcr.io/${{ github.repository }}
      tags: |
        type=semver,pattern={{version}}
        type=semver,pattern={{major}}.{{minor}}
        type=sha,format=long
        type=ref,event=pr
        type=raw,value=latest,enable={{is_default_branch}}
  - id: build
    uses: docker/build-push-action@v6
    with:
      context: .
      platforms: linux/amd64,linux/arm64
      push: ${{ github.event_name != 'pull_request' }}
      tags: ${{ steps.meta.outputs.tags }}
      labels: ${{ steps.meta.outputs.labels }}      # OCI labels incl. org.opencontainers.image.source → links package to repo
      cache-from: type=gha
      cache-to: type=gha,mode=max
      provenance: mode=max
      sbom: true
  - uses: actions/attest-build-provenance@v2
    with: { subject-name: ghcr.io/${{ github.repository }}, subject-digest: ${{ steps.build.outputs.digest }}, push-to-registry: true }
```
- `GITHUB_TOKEN` can push to GHCR packages **owned by the same repo/org** once the package
  is linked to the repo (the `org.opencontainers.image.source` label does this on first push,
  or link manually in package settings). First push creates the package **private**; flip
  visibility in package settings if it should be public.
- Package *Manage Actions access* must include the repo with **write** for other repos'
  workflows to push.
- `type=sha,format=long` gives the immutable tag you deploy by; `latest` is for humans.
- Build on PRs with `push: false` + `load: true` to test the image; push only on merge/tag.

## 2. npm
```yaml
- uses: actions/setup-node@v4
  with: { node-version: 20, registry-url: https://registry.npmjs.org }
- run: npm publish --provenance --access public
  env: { NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }} }
```
`--provenance` needs `id-token: write` and links the package to the workflow on npmjs. npm
**trusted publishing** (OIDC, no token) is GA since 2025: configure the publisher on
npmjs (repo + workflow filename), then `npm publish` with no `NODE_AUTH_TOKEN` (npm CLI ≥ 11.5).
For GitHub Packages npm: `registry-url: https://npm.pkg.github.com`, scope must equal the
org (`@org/name`), token `GITHUB_TOKEN` with `packages: write`.

## 3. PyPI (trusted publishing, no API token)
```yaml
jobs:
  publish:
    environment: pypi
    permissions: { id-token: write }
    steps:
      - uses: actions/download-artifact@v4
        with: { name: dist, path: dist }
      - uses: pypa/gh-action-pypi-publish@release/v1
```
Register the publisher on PyPI (owner, repo, workflow file name, environment). Build in a
separate job (`python -m build`) so publishing runs no project code. Use TestPyPI first
(`with: repository-url: https://test.pypi.org/legacy/`).

## 4. Maven / Gradle / NuGet to GitHub Packages
- Maven: `distributionManagement` URL `https://maven.pkg.github.com/<org>/<repo>`,
  `actions/setup-java` with `server-id: github` writes `settings.xml` using
  `GITHUB_TOKEN`; `mvn deploy`. Consumers need a PAT with `read:packages` even for public
  packages (GitHub Packages Maven does not allow anonymous reads).
- Gradle: `maven { url = uri("https://maven.pkg.github.com/org/repo"); credentials { username = System.getenv("GITHUB_ACTOR"); password = System.getenv("GITHUB_TOKEN") } }`.
- NuGet: `dotnet nuget add source --username <org> --password $GITHUB_TOKEN --store-password-in-clear-text --name github "https://nuget.pkg.github.com/<org>/index.json"`; `dotnet nuget push *.nupkg --source github`.

## 5. Release assets
```yaml
- uses: softprops/action-gh-release@v2
  if: startsWith(github.ref, 'refs/tags/')
  with:
    files: dist/*
    generate_release_notes: true
```
Needs `contents: write`. For checksums: `sha256sum dist/* > dist/SHA256SUMS` before upload;
sign with `cosign sign-blob` or attach `actions/attest-build-provenance` attestations
(`gh attestation verify <file> --owner <org>` for consumers).

## 6. Cleanup and quotas
GHCR storage is billed for private packages. Prune untagged/old versions:
`actions/delete-package-versions@v5` (`min-versions-to-keep: 10, delete-only-untagged-versions: true`)
or `dataaxiom/ghcr-cleanup-action` (keeps multi-arch manifests consistent — naive deletion
of untagged versions **breaks** multi-arch images by deleting platform manifests; prefer a
tool that understands manifest lists).

## Verify
- [ ] `docker pull ghcr.io/org/app:sha-<commit>` works from a clean machine with expected visibility.
- [ ] `docker buildx imagetools inspect` shows both platforms and the provenance/SBOM attestations.
- [ ] `gh attestation verify oci://ghcr.io/org/app@sha256:… --owner org` passes.
- [ ] Publishing jobs carry only `packages: write`/`id-token: write`; no long-lived registry PATs remain.
