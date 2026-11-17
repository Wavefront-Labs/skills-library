---
id: computing-software.devops-ci-cd.github-actions.artifact-digest-and-attesting-artifacts
name: artifact-digest-and-attesting-artifacts
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, artifact-digest, attest-build-provenance, upload-artifact]
level: advanced
status: gated
description: "Use upload-artifact's artifact-id/artifact-digest outputs to verify downloads and generate build provenance for files you upload, then verify with gh attestation."
sources: ["https://github.com/actions/upload-artifact#outputs", "https://github.com/actions/attest-build-provenance"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Artifact digests and attesting uploaded artifacts

`actions/upload-artifact@v4` outputs `artifact-id`, `artifact-url` and `artifact-digest`
(SHA-256 digest of the artifact). Whether `download-artifact` verifies the digest on download was not confirmed (gated: unconfirmed, source is paywalled or blocked).

## Attest the files you ship
Attest the files themselves, not the artifact zip, since consumers verify the file:
```yaml
permissions: { id-token: write, attestations: write, contents: read }
steps:
  - run: make dist   # produces dist/app-linux-amd64
  - uses: actions/attest-build-provenance@<sha> # v4+ wraps actions/attest; new workflows should use actions/attest
    with:
      subject-path: 'dist/app-*'
  - uses: actions/upload-artifact@<sha> # v4
    id: up
    with: { name: dist, path: dist/ }
  - run: echo "digest=${{ steps.up.outputs.artifact-digest }}" >> "$GITHUB_STEP_SUMMARY"
```
For the zip as a unit (e.g. a deployment bundle consumed via API), attest by digest:
```yaml
  - uses: actions/attest-build-provenance@<sha>
    with:
      subject-name: dist.zip
      subject-digest: sha256:${{ steps.up.outputs.artifact-digest }}
```

## Verify downstream
```bash
gh run download <run-id> -n dist
gh attestation verify dist/app-linux-amd64 --repo org/repo \
  --signer-workflow org/repo/.github/workflows/release.yml
```

## Gotchas
- Private repos need GitHub Enterprise Cloud for attestations; public repos use public Sigstore.
- Attesting before compression vs after: pick one convention, verifiers must hash the same bytes.
- Artifacts expire (retention-days); attestations are stored separately (gated: unconfirmed, source is paywalled or blocked). Keep shipped files in a release or registry.

## Verify
- [ ] `gh attestation verify` succeeds and fails on a modified copy of the file.

## Checked

2026-11-02. Confirmed from the upload-artifact README: artifact-id, artifact-url and artifact-digest outputs (SHA-256), retention input, v4 artifacts immutable; from the gh manual: attestation verify --signer-workflow; from GitHub attestation docs: id-token/attestations write permissions, subject-name/subject-digest inputs, and private repositories needing Enterprise Cloud on Free/Pro/Team plans. Removed: the (v4.6+) version gate and the download-artifact verification claim (not stated). Fixed: attest-build-provenance v2 pin comment (v4+ is a wrapper on actions/attest). Gated: attestation retention.

Method: documentation only; no commands were run.
