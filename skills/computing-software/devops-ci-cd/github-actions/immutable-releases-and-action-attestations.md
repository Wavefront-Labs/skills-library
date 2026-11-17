---
id: computing-software.devops-ci-cd.github-actions.immutable-releases-and-action-attestations
name: immutable-releases-and-action-attestations
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, immutable-actions, action-attestations, immutable-releases, gh-release-verify, sha-pinning-policy]
level: advanced
status: docs-checked
description: "Make action and release versions tamper-proof: immutable releases with release attestations, gh release verify, artifact attestations and the org SHA-pinning policy."
sources: ["https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/immutable-releases", "https://docs.github.com/en/actions/security-for-github-actions/using-artifact-attestations/using-artifact-attestations-to-establish-provenance-for-builds", "https://cli.github.com/manual/gh_release_verify"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Immutable releases and action attestations

**Threat:** `uses: some/action@v2` follows a movable tag. A compromised maintainer token can re-point
`v2` to malicious code and every consumer runs it.

## 1. As an action publisher: immutable releases
Enable immutable releases for the repository or organisation (see "Preventing changes to your releases" in GitHub Docs).
Once a release is **published**:
- its Git tag is locked to a commit and cannot be moved or deleted while the release exists, and its assets cannot be modified or deleted (title, notes and pre-release/latest flags can still be edited);
- GitHub generates a **release attestation** (verifiable record of tag, commit SHA and release assets).
Workflow: create the release as a **draft**, upload all assets, then publish — after publishing
you cannot fix a missing asset, only cut a new version.

## 2. As a consumer: verify
```bash
gh release verify v1.2.3 -R some/action      # release attestation valid?
# see `gh release verify-asset --help` and `gh attestation verify --help` for asset and build-provenance checks
```

## 3. Still pin to SHAs
Immutability only protects releases published after it was enabled. Pin third-party actions by full commit SHA with a version comment and let Dependabot/Renovate bump them. Check the org Actions policies in GitHub Docs for enforcing SHA pinning.

## 4. Attest your own build outputs
```yaml
permissions: { id-token: write, attestations: write, contents: read }
steps:
  - uses: actions/attest@v4
    with: { subject-path: 'dist/*' }
```

## Verify
- [ ] Moving or deleting the tag of a published immutable release is rejected.
- [ ] `gh release verify` passes for the versions you consume.
- [ ] `zizmor`/`actionlint` reports no unpinned `uses:`.

## Checked
2026-10-28. Confirmed on the GitHub Docs immutable releases page: tags locked and not movable or deletable while the release exists; assets cannot be modified or deleted; title, notes and pre-release/latest flags remain editable; draft, attach assets, publish workflow; release attestation contents. Confirmed on the artifact attestations page: permissions `id-token: write`, `contents: read`, `attestations: write` and the `subject-path` input. The gh_release_verify manual returned a stub, so only the `gh release verify <tag>` form (shown in that manual's examples) is kept.
Fixed: the attestation step now uses `actions/attest@v4` as shown in current docs instead of `actions/attest-build-provenance@v2`.
Removed (not confirmed): the incident name and date, settings menu paths, the OCI immutable-actions preview, `verify-asset` and `attestation verify` argument forms, the SHA-pinning policy menu path, the checkout SHA.

Method: documentation only; no commands were run.
