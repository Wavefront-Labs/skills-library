---
id: computing-software.devops-ci-cd.github-actions.draft-then-publish-releases
name: draft-then-publish-releases
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, draft-release-publish, github-release, release-automation]
level: practitioner
status: gated
description: "Build releases as drafts, upload and verify every asset, then publish atomically; interaction with immutable releases and release-triggered workflows."
sources: ["https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository", "https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/immutable-releases"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Draft-then-publish releases

Publishing a release fires `release: published`, notifies watchers and (with immutable releases
enabled) **locks assets and the tag**. So assemble everything on a draft first.

```yaml
jobs:
  draft:
    runs-on: ubuntu-latest
    permissions: { contents: write }
    steps:
      - run: gh release create "$TAG" --draft --verify-tag --generate-notes --title "$TAG"
        env: { GH_TOKEN: ${{ github.token }}, TAG: ${{ github.ref_name }} }
  build:
    needs: draft
    strategy: { matrix: { os: [ubuntu-24.04, macos-15, windows-2025] } }
    runs-on: ${{ matrix.os }}
    permissions: { contents: write }
    steps:
      - run: make dist && gh release upload "$TAG" dist/* --clobber
        shell: bash
        env: { GH_TOKEN: ${{ github.token }}, TAG: ${{ github.ref_name }} }
  publish:
    needs: build
    runs-on: ubuntu-latest
    permissions: { contents: write }
    steps:
      - run: |
          n=$(gh release view "$TAG" --json assets --jq '.assets | length')
          test "$n" -ge 3 || { echo "missing assets: $n"; exit 1; }
          gh release edit "$TAG" --draft=false --latest
        env: { GH_TOKEN: ${{ github.token }}, GH_REPO: ${{ github.repository }}, TAG: ${{ github.ref_name }} }
```

## Gotchas
- Per GitHub's events reference, `release` workflows are not triggered for the `created`, `edited` or `deleted` types on draft releases; trigger downstream on `published`.
- GITHUB_TOKEN-published releases do **not** trigger other workflows' `release` event (gated: unconfirmed, source is paywalled or blocked). Use a GitHub
  App token if downstream automation must run.
- Immutable releases: after publishing you cannot add/replace assets or move the tag; a broken
  release means a new version.
- `--verify-tag` fails if the tag was not pushed, so gh does not create the tag itself (without it, gh creates a missing tag from the default branch).

## Verify
- [ ] Release page shows all assets and checksums before the draft flag is cleared.

## Checked

2026-11-02. Confirmed against the gh manual (release create, upload, edit, view: --draft, --verify-tag, --generate-notes, --clobber, --latest, --draft=false, --json/--jq assets field, immutable-release behaviour) and the GitHub events reference (release activity types and draft behaviour). Removed: the claim that drafts are invisible to releases/latest and the gh release view membership claim (not stated in the docs read). Fixed: the draft `created` claim contradicted the events reference. Gated: that GITHUB_TOKEN-published releases do not trigger other workflows; the page read did not state it.

Method: documentation only; no commands were run.
