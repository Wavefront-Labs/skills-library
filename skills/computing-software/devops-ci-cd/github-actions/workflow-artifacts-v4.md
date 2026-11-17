---
id: computing-software.devops-ci-cd.github-actions.workflow-artifacts-v4
name: workflow-artifacts-v4
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, workflow-artifacts, upload-artifact, download-artifact, artifacts-v4, artifact-retention, retention-days, artifact-immutability, merge-multiple, artifact-pattern, compression-level, if-no-files-found, cross-run-download, run-id, gh-run-download, artifact-storage-quota, artifact-id, overwrite, include-hidden-files, matrix-artifacts, test-reports]
level: practitioner
status: docs-checked
description: "Use upload/download-artifact v4 correctly: immutable names, per-matrix-leg naming and merge-multiple, retention and storage quota, cross-run download, the path-flattening rule."
sources: ["https://docs.github.com/en/actions/tutorials/store-and-share-data", "https://github.com/actions/upload-artifact#readme", "https://github.com/actions/download-artifact#readme"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Workflow artifacts (v4)

**Goal:** move build outputs and reports between jobs and out of the run, without the
v4-specific traps (name collisions, flattened paths, surprise storage bills).

## 1. v4 changed the rules
- Artifacts are **immutable** (unless deleted): upload with a name that already exists fails unless
  `overwrite: true`, which deletes the old artifact and creates a new one. Matrix jobs **must** use unique
  names: `name: test-results-${{ matrix.os }}-${{ matrix.shard }}`.
- At most **500 artifacts per job**.
- v3 is deprecated; see the migration skill. On GitHub Enterprise Server `upload-artifact@v4+` is not currently supported.

## 2. Upload
```yaml
- uses: actions/upload-artifact@v7
  with:
    name: dist-${{ github.sha }}
    path: |
      dist/
      !dist/**/*.map
    if-no-files-found: error      # default is "warn"; "ignore" is also available
    retention-days: 7             # 1-90 days unless the repository settings allow more; default = repository setting
    compression-level: 6          # 0-9, default 6; 0 is recommended for large files that compress poorly
    include-hidden-files: false   # default false
```
**Path rule:** with several search paths, the least common ancestor of all the search paths is the root of the
artifact; exclude paths do not change the structure. With a wildcard, the hierarchy is preserved after the first
wildcard pattern (for example `path/to/*/directory/foo?.txt` uploads `some/directory/foo1.txt`).

File permissions are not maintained in a zipped upload (directories get 755, files 644), so an executable bit is
not guaranteed after download. To keep permissions, `tar` the files first and upload the tarball with
`archive: false`.

## 3. Download
```yaml
- uses: actions/download-artifact@v8
  with:
    name: dist-${{ github.sha }}     # omit name = download all artifacts for the run
    path: dist
```
Merge matrix legs:
```yaml
- uses: actions/download-artifact@v8
  with:
    pattern: test-results-*
    merge-multiple: true          # all into one folder instead of one named folder per artifact
    path: reports
```
Cross-run / cross-repo download (a `github-token` is required; `repository` and `run-id` select the source):
```yaml
- uses: actions/download-artifact@v8
  with:
    name: dist
    run-id: ${{ github.event.workflow_run.id }}
    github-token: ${{ secrets.GITHUB_TOKEN }}
    repository: ${{ github.repository }}
```
CLI: `gh run download <run-id> -n dist -D ./dist` (`-n` name, `-D` destination directory, `-p` glob pattern).
The download action also validates a SHA-256 digest (`digest-mismatch`, default `error`).

## 4. Retention and storage
- `retention-days` cannot exceed the limit set by the repository, organisation or enterprise; the upload
  action's default is 90 days unless changed in repository settings.
- Artifact storage counts toward the plan's Actions storage quota (calculated every 6-12 hours, per the
  upload-artifact README); see the billing documentation for amounts.
- Outputs of the upload step include `artifact-id`, `artifact-url` (login required) and `artifact-digest`.

## 5. Security
- Artifacts produced by untrusted code (for example a fork pull request) should be treated as data in any
  privileged `workflow_run` consumer: never execute their contents.
- Upload hidden files only after validating their contents (the action's own warning); exclude secrets and
  state files with `!` patterns.

## 6. Alternatives
`actions/cache` for restoring dependencies across runs; job outputs for small strings; the job summary for
human-readable reports.

## Verify
- [ ] Matrix uploads have unique names; no `Conflict` errors.
- [ ] `if-no-files-found: error` set on every build artifact upload.
- [ ] Downloaded layout matches expectations (least-common-ancestor rule checked once).
- [ ] CI bundles have short `retention-days`.

## Checked

Date: 2026-10-25. Documentation release: actions/upload-artifact README (v7), download-artifact README (v8), github/docs commit of 2026-10-23.
- Inputs and defaults (if-no-files-found warn|error|ignore, retention-days 1-90 and repository limit, compression-level 0-9 default 6, overwrite, include-hidden-files default false, archive), outputs (artifact-id, artifact-url, artifact-digest), 500 artifacts per job, permission loss and tar advice, least-common-ancestor rule: confirmed in the upload-artifact README (v7).
- download-artifact inputs (name, pattern, merge-multiple, github-token, repository, run-id, digest-mismatch default error) and gh run download flags (-n, -D, -p from cli source): confirmed.
- Removed the unconfirmed 10x speed claim, the 400-day enterprise retention, the free storage figure and billing rates, the artifact deletion endpoint and the immediate API availability claim.

Method: documentation only; no commands were run.
