---
id: computing-software.devops-ci-cd.packer.hashicorp-release-site-plugins
name: hashicorp-release-site-plugins
category: computing-software
field: devops-ci-cd
product: packer
tags: [releases-hashicorp-com, official-plugins, packer-1-14, upgrade, plugins-install]
level: practitioner
status: docs-checked
description: "From August 2025 official HashiCorp plugins ship from releases.hashicorp.com; Packer 1.14.0 installs them automatically."
sources:
  - "https://developer.hashicorp.com/packer/docs/plugins/install-plugins/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Starting August 1st, 2025, many official HashiCorp-maintained plugins moved from GitHub releases to releases.hashicorp.com. The affected plugins listed in the docs are Amazon, Ansible, Azure, Docker, Google Cloud Platform, QEMU, Vagrant and VirtualBox.

Packer 1.14.0 and newer install these from the new source automatically, with no change to your templates. To keep receiving updates, upgrade to Packer 1.14.0 or newer. If you cannot upgrade, you can still install new versions manually with `packer plugins install`.

Your `required_plugins` block keeps the same form:

```hcl
packer {
  required_plugins {
    amazon = {
      version = ">= 1.3.0"
      source  = "github.com/hashicorp/amazon"
    }
  }
}
```

The `source` stays a `github.com/hashicorp/...` address; the change is where Packer fetches the binaries.

## Checked
2026-11-03. Confirmed against the Install plugins page: the 1 August 2025 move, the eight listed plugins, Packer 1.14.0 automatic install and manual install otherwise. Removed unsourced practical checks and a verification claim.
Method: documentation only; no commands were run.
