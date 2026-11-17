---
id: computing-software.devops-ci-cd.atlantis.atlantis-terraform-versions-and-opentofu
name: atlantis-terraform-versions-and-opentofu
category: computing-software
field: devops-ci-cd
product: atlantis
tags: [terraform-version, opentofu, default-tf-version, required-version, tofu-files]
level: practitioner
status: docs-checked
description: "Control which Terraform or OpenTofu version Atlantis downloads using flags, atlantis.yaml and required_version."
sources: ["https://www.runatlantis.io/docs/terraform-versions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Atlantis terraform versions and opentofu

Precedence, highest first: `terraform_version` in `atlantis.yaml`, then `--default-tf-version`, then `required_version` in HCL. Atlantis downloads the latest version satisfying the constraint.

```yaml
version: 3
projects:
- dir: .
  terraform_version: v1.1.5
```

`required_version` forms: exact (`= 1.2.9` or `1.2.9`), `"~> 1.2.0"` (any patch of 1.2), `"~> 1.2"` (any 1.x from 1.2), `">= 1.2.0"`. Comparison and pessimistic constraints arrived in v0.21.0.

OpenTofu: set `terraform_distribution: opentofu` per project, or `--default-tf-distribution=opentofu` server-wide. A project setting `terraform` reads only `.tf` and `.tf.json` even if the server default is OpenTofu. With OpenTofu effective, `required_version` is also read from `.tofu` and `.tofu.json`, and a `.tofu` file overrides a `.tf` file with the same basename.

Known limitation: `--autoplan-modules` indexing uses `terraform-config-inspect` and does not fully handle `.tofu` files, so module sources declared only there are not indexed. Workarounds: explicit `autoplan.when_modified` patterns or keep module sources in `.tf`.

Docker images no longer bundle Terraform or OpenTofu binaries; set `--default-tf-version` (and the distribution) so Atlantis knows what to download, or mount a binary into the image if downloads are blocked.

## Checked

2026-11-03. Prose and identifiers confirmed against the official Atlantis docs page(s): Terraform Versions. Removed or fixed: nothing needed removing.

Method: documentation only; no commands were run.
