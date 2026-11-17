---
id: computing-software.devops-ci-cd.packer.required-plugins-block
name: required-plugins-block
category: computing-software
field: devops-ci-cd
product: packer
tags: [required-plugins, packer-block, version, source, block-packer, plugins-install]
level: practitioner
status: docs-checked
description: "Declare plugins, sources and version constraints inside the packer block so packer init is reproducible."
sources:
  - https://developer.hashicorp.com/packer/docs/templates/hcl_templates/blocks/packer
  - https://developer.hashicorp.com/packer/docs/plugins/install
  - https://developer.hashicorp.com/packer/docs/commands/init
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The `required_plugins` block lives inside the `packer` block (Packer v1.7.0 and later) and maps a local plugin name to a source address and version constraint.

```hcl
packer {
  required_plugins {
    happycloud = {
      version = ">= 2.7.0"
      source  = "github.com/hashicorp/happycloud"
    }
  }
}
```

Source format: `<HOSTNAME>/[SUBFOLDER/]<NAMESPACE>/<TYPE>`.

- Hostname: `packer init` only supports `github.com`. Other addresses, such as an internal proxy or plugin binary store, are allowed, but Packer only pins the required version if you install the plugin with `packer plugins install -path`.
- Subfolder is optional; up to 13 total path segments are allowed.
- Namespace is usually the publishing organisation; type is the platform name.
- The repository must really be `packer-plugin-<type>`; the block omits the `packer-plugin-` prefix.

Inside a `packer` block only constant values are allowed: no named objects, variables or built-in functions.

The block records the source and the version (exact or minimum) of each plugin, which the page describes as ensuring consistent builds across hosts. When you build, Packer checks the plugin directory against `required_plugins`; manually installed plugins must still satisfy the constraints. `packer init -upgrade` upgrades installed plugins to the latest version allowed by the constraints.

## Checked

Method: documentation only; no commands were run. Checked 2026-11-09 against the Packer 1.15 `packer` block reference, "Installing plugins" and `init` command pages. Corrected: the hostname rule (the earlier text said any host serving an HTTPS directory structure works). Removed: the "pin a range, not latest" advice and "the build errors" wording, which the pages do not state in those words.
