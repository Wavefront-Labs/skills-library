---
id: computing-software.devops-ci-cd.packer.hcp-packer-registry-block
name: hcp-packer-registry-block
category: computing-software
field: devops-ci-cd
product: packer
tags: [hcp-packer, registry, bucket, hcp-packer-registry, hcp-registry]
level: advanced
status: docs-checked
description: "Push build metadata to HCP Packer by adding an hcp_packer_registry block with bucket_name and labels."
sources:
  - "https://developer.hashicorp.com/packer/docs/templates/hcl_templates/blocks/build/hcp_packer_registry/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The `hcp_packer_registry` block, available from Packer 1.7.7, switches Packer into HCP Packer mode. In that mode Packer pushes metadata for all builds in the template to the HCP Packer registry.

```hcl
hcp_packer_registry {
  bucket_name = "ubuntu-web"
  description = "Hardened Ubuntu base image."
  bucket_labels = {
    "team" = "platform"
    "os"   = "ubuntu"
  }
  build_labels = {
    "tool-version" = "1.2.3"
  }
}
```

Arguments:

- `bucket_name` (string) is the image name in the registry. Keep it constant, otherwise a new image is created. It defaults to `build.name` and is overwritten by the `HCP_PACKER_BUCKET_NAME` environment variable.
- `description` (string) is a summary shown on the image page, at most 255 characters; it defaults to `build.description`.
- `bucket_labels` (map of string) appear on the image's main page and update when a new iteration is pushed.
- `build_labels` (map of string) appear in the build section of an iteration. They are specific to an iteration, and updating build labels on a completed iteration is not allowed.
- `labels` is deprecated since Packer 1.7.9; use `bucket_labels`.

Credentials: set `HCP_CLIENT_ID` and `HCP_CLIENT_SECRET`. If no HCP credentials are set, Packer fails the build and exits immediately, to avoid drift between the defined source blocks and the registry.

Referencing metadata from a deactivated or deleted registry is an error. An administrator can deactivate or delete a registry, and HCP Packer deactivates registries with billing issues.

Where the block sits in the template: the reference page's example places it in the template file next to a `build` block, so copy the placement from the page for your Packer version.

## Checked

2026-11-09. Checked against the Packer v1.15 documentation page for the hcp_packer_registry block: version 1.7.7 and 1.7.9 gates, the five arguments and their defaults, the 255 character limit, the two credential variables, the fail-fast behaviour and the deactivated-registry error.

Removed as unsupported by that page: the claim that the block is nested inside `build`, the fingerprint and ULID (Packer 1.9.0) statement, the `packer validate` and iteration advice, and the `timestamp()` example label.

Method: documentation only; no commands were run.
