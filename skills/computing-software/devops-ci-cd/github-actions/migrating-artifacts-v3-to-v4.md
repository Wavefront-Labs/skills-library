---
id: computing-software.devops-ci-cd.github-actions.migrating-artifacts-v3-to-v4
name: migrating-artifacts-v3-to-v4
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, artifact-v4-migration, upload-artifact, download-artifact]
level: practitioner
status: docs-checked
description: "Migrate upload/download-artifact v3 to v4: immutable unique names, matrix uploads, merge-multiple, hidden files, and the GHES and cross-version incompatibility."
sources: ["https://github.com/actions/upload-artifact/blob/main/docs/MIGRATION.md", "https://github.com/actions/upload-artifact#readme", "https://github.blog/changelog/2024-04-16-deprecation-notice-v3-of-the-artifact-actions/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating artifact actions v3 to v4

The upload-artifact README announced v3 (and v1/v2) for deprecation, with v3 scheduled for 30 November 2024 and
v1/v2 for 30 June 2024; check the GitHub changelog entry for the current enforcement status. v4 uses a new
artifact backend with breaking behaviour (see the migration guide).

## Breaking changes and fixes
| v3 behaviour | v4 | Fix |
|---|---|---|
| Multiple jobs could upload to the same name (appending) | artifacts are immutable (unless deleted), so each upload needs its own name | unique names: `name: dist-${{ matrix.os }}` |
| Download by shared name into one dir | filter by `pattern`; with several matches each artifact extracts to its own directory unless merged | `download-artifact` with `pattern: dist-*` + `merge-multiple: true` |
| Re-upload same name | fails by default | `overwrite: true` (deletes the old artifact first; the result is an entirely new artifact with a new ID) |
| Hidden files included | ignored by default; versions before v4.4.0 included them | `include-hidden-files: true` if you really need hidden files |
| Single archive from many jobs | one artifact per job | `actions/upload-artifact/merge` with `pattern:` to combine into one artifact (it downloads and re-uploads) |
| Artifacts per job | limit of 500 artifacts per job | consolidate |

GHES: the README says `upload-artifact@v4+` is not currently supported on GitHub Enterprise Server; use
v3.2.2 (Node 24) or v3.2.2-node20 there.

## Example matrix fan-in
```yaml
- uses: actions/upload-artifact@v7
  with: { name: coverage-${{ matrix.shard }}, path: coverage/ }
# later job
- uses: actions/download-artifact@v8
  with: { pattern: coverage-*, merge-multiple: true, path: coverage }
```
With `merge-multiple`, files with the same name in several artifacts: the last writer wins. (The current README
majors at review were upload-artifact v7 and download-artifact v8.)

## Verify
- [ ] No workflow or composite action still references `artifact@v3`.
- [ ] Run summary lists one artifact per leg; the fan-in job sees all files.

## Checked

Date: 2026-10-25. Documentation release: actions/upload-artifact and actions/download-artifact READMEs (v7 and v8).
- Immutability, unique names with pattern and merge-multiple (last writer wins), overwrite: true creating a new artifact, include-hidden-files and the v4.4.0 default change, upload-artifact/merge, v3 deprecation dates: confirmed in actions/upload-artifact docs/MIGRATION.md and README.
- 500 artifacts per job and the GHES statement: confirmed in the upload-artifact README. Current majors upload v7 and download v8: README examples.
- Removed the 409 status, the quoted v3 failure text, the cutoff month claim, the cross-version incompatibility row and the GHES 3.13 gate, which none of the fetched pages state.

Method: documentation only; no commands were run.
