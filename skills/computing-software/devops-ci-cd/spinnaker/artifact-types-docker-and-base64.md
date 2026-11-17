---
id: computing-software.devops-ci-cd.spinnaker.artifact-types-docker-and-base64
name: artifact-types-docker-and-base64
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [artifacts, docker-image, embedded-base64, artifact-types, references]
level: intro
status: docs-checked
description: "Read and write two artifact types by their fields: docker/image (reference, name, version by tag or digest) and embedded/base64 (contents inline in reference)."
sources:
  - https://spinnaker.io/docs/reference/artifacts/types/docker-image/
  - https://spinnaker.io/docs/reference/artifacts/types/embedded-base64/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Spinnaker artifacts are JSON objects with a `type`, a `reference` and optional metadata. Two simple types show the pattern.

**docker/image.** References an image in a registry such as GCR or Docker Hub. Such artifacts can be deployed to Kubernetes or App Engine and generally trigger pipelines from registry notifications.

| Field | Meaning |
|---|---|
| `type` | Always `docker/image` |
| `reference` | Fully qualified image name with version and registry, by tag (`gcr.io/project/my-image:v1.2`) or digest (`gcr.io/project/my-image@sha256:28f82eba`) |
| `name` | Image name without version, e.g. `gcr.io/project/my-image` |
| `version` | The tag or digest |
| `location` | Not applicable |

**embedded/base64.** Instead of a URI, the artifact's contents are base64 encoded directly into `reference`. Fields: `type` (always `embedded/base64`), `reference` (the encoded contents), and an optional human-readable `name`. Example from the page: `{"type": "embedded/base64", "reference": "dmFsdWU6IDEKbXlrZXk6IG15dmFsdWU=", "name": "my-properties-file"}`. In the pipeline UI the account is always "embedded-artifact", with a Name and the Base64-encoded Contents.

When writing pipeline JSON by hand, match these field names exactly.

## Checked

Method: docs-checked 2026-11-09 against the full spinnaker.io Docker Image and Embedded Base64 artifact type pages. Confirmed both field tables and examples. Replaced the unsourced example reference with the page's own, and removed the Bake output and name/version binding remarks, which those pages do not state.
