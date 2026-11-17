---
id: computing-software.devops-ci-cd.argo-workflows.key-only-artifacts
name: key-only-artifacts
category: computing-software
field: devops-ci-cd
product: argo-workflows
tags: [key-only-artifacts, artifact-key, s3-key, artifact-location, status-nodes]
level: practitioner
status: docs-checked
description: "Declare artifacts with only a key so bucket and credentials come from the configured artifact repository, shrinking Workflow objects."
sources: ["https://argo-workflows.readthedocs.io/en/latest/key-only-artifacts/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Key-only artifacts
A key-only artifact specifies only the key (for example `s3: {key: my-file}`) on an input or output artifact; the bucket and secrets are filled in from the configured artifact repository. This moves repository configuration out of the workflow and is described as the likely default choice.

Benefits listed:
- smaller Workflow objects, so better performance
- the repository setup is owned by users or admins
- you can reconfigure the repository without editing workflows or templates

Example shape: a `generate` template with `outputs.artifacts` of `name: file`, `path: /mnt/file`, `s3.key: my-file`, and a `consume` template whose `inputs.artifacts` use the same `s3.key: my-file` and `path: /tmp/file`; a DAG makes `consume` depend on `generate`.

Use it together with `artifactRepositoryRef` to pick which repository entry applies.

Warning: artifact location data is no longer stored in `/status/nodes`, so any tooling that reads locations from there must change.

## Checked
2026-11-03. Confirmed against the Argo Workflows Key-Only Artifacts page: definition, the three listed benefits, the artifact repository ref pairing, the generate and consume example and the /status/nodes warning. Removed an uncited paragraph about changing the bucket.
Method: documentation only; no commands were run.
