---
id: computing-software.devops-ci-cd.gitea.actions-artifacts
name: actions-artifacts
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-actions-artifacts, gitea, artifact-preview, artifact-preview-max-size, upload-artifact, signed-preview-urls]
level: practitioner
status: docs-checked
description: "Store workflow artifacts in Gitea, preview them in the run page, and tune ARTIFACT_PREVIEW_MAX_SIZE and file display limits."
sources: ["https://docs.gitea.com/usage/actions/artifacts/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea Actions artifacts

Workflows store test results, coverage reports and build output as artifacts, uploaded for example with `actions/upload-artifact`; they appear on the run page after upload finishes.

## Previewing
Selecting an artifact opens a file browser and preview in the same tab. The preview names the originating run and attempt and links back to the run and to a full download. Requirements and behaviour:
- Signing in and access to the Actions run is required.
- Text-based files, images (including SVG) and PDFs render; HTML and JavaScript run in a sandboxed frame.
- Content loads through signed URLs that expire after one hour and need no session cookie; reopen the preview page for a fresh URL.
- The file browser lists at most 2,000 files per artifact and shows a notice when truncated.
- Unsupported or oversized files can still be downloaded with the whole artifact.

## Configuration
In the `[actions]` section of `app.ini`: `ARTIFACT_PREVIEW_MAX_SIZE` caps the total artifact size that can be browsed or previewed. Default 10 MiB; `0` disables previews, `-1` allows any size. A single previewed file is also limited by `MAX_DISPLAY_FILE_SIZE` in `[ui]`.

If a preview is missing for a big artifact, raise `ARTIFACT_PREVIEW_MAX_SIZE`; if one file will not display inside an allowed artifact, check `MAX_DISPLAY_FILE_SIZE`.

## Checked

2026-11-03: read https://docs.gitea.com/usage/actions/artifacts/ line by line; the commands, options, defaults and values stated above match those pages.
Removed: nothing; every claim was confirmed.
Method: documentation only; no commands were run.
