---
id: computing-software.devops-ci-cd.github-actions.creating-releases-with-gh-release-and-action-gh-release
name: creating-releases-with-gh-release-and-action-gh-release
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, action-gh-release, gh-release-create, release-assets, draft-release]
level: practitioner
status: docs-checked
description: "Create GitHub Releases from a workflow with gh release create or softprops/action-gh-release: assets, drafts, prereleases, latest flag, and safe upload ordering."
sources: ["https://cli.github.com/manual/gh_release_create", "https://github.com/softprops/action-gh-release", "https://docs.github.com/en/rest/releases/releases"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Creating releases from Actions

## 1. gh CLI
```yaml
permissions: { contents: write }
steps:
  - uses: actions/checkout@v4
  - run: make dist
  - env: { GH_TOKEN: "${{ github.token }}", TAG: "${{ github.ref_name }}" }
    run: |
      gh release create "$TAG" dist/*.tar.gz dist/SHA256SUMS \
        --verify-tag --generate-notes --draft \
        $([[ "$TAG" == *-* ]] && echo --prerelease)
      gh release edit "$TAG" --draft=false          # publish only after all assets uploaded
```
Useful flags: `--title`, `--notes-file CHANGELOG.md`, `--notes-start-tag v1.4.0`,
`--latest=false` (do not mark as Latest), `--target <branch|sha>` (where a new tag is created),
`--discussion-category`, `--fail-on-no-commits`. Asset display labels: `'dist/app.zip#App for Windows'`.
With assets, `gh release create` makes a draft, uploads each asset, then publishes (not atomic).
Add assets later: `gh release upload v1.2.3 extra.bin --clobber`.

## 2. softprops/action-gh-release
```yaml
- uses: softprops/action-gh-release@v3
  if: startsWith(github.ref, 'refs/tags/')
  with:
    files: |
      dist/*.tar.gz
      dist/SHA256SUMS
    generate_release_notes: true
    draft: false
    prerelease: ${{ contains(github.ref_name, '-') }}
    fail_on_unmatched_files: true
```
If a release already exists for the tag it is updated with the assets (`overwrite_files` defaults to
true). v2 is no longer maintained; use v3. The action needs `contents: write`.

## 3. Gotchas
- The default `GITHUB_TOKEN` does not trigger another workflow; to run workflows on the `release` event,
  use a personal access token for the action.
- With immutable releases enabled, tags and assets cannot be changed after publishing: publish only after
  every asset is attached (use a draft first).
- `gh release edit <tag> --draft=false` publishes a draft; `--prerelease` and `--latest` exist on `edit` too.
- Pin the notes range with `previous_tag` (action) or `--notes-start-tag` (gh).

## Verify
- [ ] The release page lists every expected asset.
- [ ] Prerelease tags (`v2.0.0-rc.1`) are not marked Latest (drafts and prereleases cannot be Latest).

## Checked

2026-10-31. Confirmed against the gh source for release create, edit and upload (flags --draft, --prerelease, --target, --title, --notes-file, --generate-notes, --notes-start-tag, --verify-tag, --discussion-category, --fail-on-no-commits, --latest, --clobber, the `#` display label, draft-then-publish with assets, immutable-release behaviour), the gh_release_create manual examples, and the softprops/action-gh-release README (inputs files, draft, prerelease, generate_release_notes, previous_tag, fail_on_unmatched_files, overwrite_files default true, contents: write, v2 end of life, v3 current, GITHUB_TOKEN not triggering other workflows).
Removed: the preinstalled-on-runners claim, the GitHub App token advice (the README says a personal access token), the matrix already_exists claim, the first-release notes claim, the --verify-tag/--target interplay and the gh release view verify command.

Method: documentation only; no commands were run.
