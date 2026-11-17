---
id: computing-software.devops-ci-cd.forgejo.artifacts-upload-download
name: artifacts-upload-download
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [artifacts, upload-artifact, download-artifact, artifact-retention]
level: practitioner
status: docs-checked
description: "Persist files between jobs or after a run with artifacts, noting the 90-day default and v3 or patched v4 actions."
sources:
  - https://forgejo.org/docs/latest/user/actions/advanced-features/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Artifacts persist files produced during a workflow run. They have two uses: keeping non-permanent data such as test results after the workflow finishes, and passing data from one job to a later job in the same workflow.

Facts from the docs:

- They expire after 90 days by default; the instance admin can change that.
- They can be downloaded from the web page showing a workflow's job details.
- An artifact name is limited to 255 characters.
- Artifacts of other workflow runs cannot currently be accessed within Forgejo (issue #8004).
- The upload and download actions must be v3 or patched v4, as shown in the docs' example based on `upload-artifact` and `download-artifact`.

For reliable exchange of information between jobs, the Cache section tells you to use artifacts, because caching makes no guarantee that a cache gets populated even when two jobs run in sequence.

Another place to publish build output is a package registry: Forgejo offers built-in package registries for various package managers, or just generic build output.

## Checked

2026-11-04. Confirmed against the Forgejo Actions advanced features page (Artifacts, Cache, Uploading to a package registry): the two uses, 90-day default, web download, 255-character name limit, issue 8004 note and the v3 or patched v4 requirement. Reworded the package registry sentence to match the page.

Method: documentation only; no commands were run.
