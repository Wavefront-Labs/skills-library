---
id: computing-software.cloud-infrastructure-engineering.terraform.provider-installation-block-direct-exclude-include
name: provider-installation-block-direct-exclude-include
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, provider-installation-block, direct-exclude, cli-config, terraformrc, filesystem-mirror, network-mirror, include-exclude, air-gapped, in-house-providers]
level: advanced
status: docs-checked
description: "Write the CLI-config provider_installation block: direct, filesystem_mirror and network_mirror ordering, include/exclude globs, in-house and air-gapped providers."
sources: ["https://developer.hashicorp.com/terraform/cli/config/config-file#provider-installation", "https://developer.hashicorp.com/terraform/cli/config/config-file#explicit-installation-method-configuration", "https://developer.hashicorp.com/terraform/internals/provider-network-mirror-protocol"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# `provider_installation` block: direct, exclude, include

**Goal:** tell Terraform exactly where each provider may come from (registry, local directory or internal mirror) with no surprises.

## 1. Syntax
```hcl
# .terraformrc (Unix, in the home directory) / terraform.rc in %APPDATA% (Windows) / file named by TF_CLI_CONFIG_FILE (*.tfrc)
provider_installation {
  filesystem_mirror {
    path    = "/opt/terraform/providers"
    include = ["example.com/*/*"]            # in-house providers only
  }
  network_mirror {
    url     = "https://mirror.internal/providers/"
    exclude = ["example.com/*/*"]
  }
  direct {
    exclude = ["example.com/*/*", "registry.terraform.io/hashicorp/aws"]
  }
}
```
Each nested block is one installation method: `direct` (origin registry), `filesystem_mirror` (needs `path`) or `network_mirror` (needs `url`). Terraform tries **all** methods whose include/exclude patterns match a provider and selects the **newest** version available across them that satisfies the version constraint. To make a mirror exclusive for a provider, remove `direct` or exclude that provider from it.

## 2. include / exclude
- Patterns match the full source address `hostname/namespace/type`. `registry.terraform.io/` may be omitted even with wildcards, so `registry.terraform.io/hashicorp/*` and `hashicorp/*` are equivalent; `*/*` is shorthand for `registry.terraform.io/*/*`, not `*/*/*`.
- If a method has both `include` and `exclude`, exclusions take priority.

## 3. Common configurations
**Air-gapped CI**:
```hcl
provider_installation {
  filesystem_mirror { path = "/mirror/providers" }
}
```
No `direct` block, so any provider not in the mirror cannot be installed. Populate the mirror with `terraform providers mirror -platform=linux_amd64 /mirror/providers`.

**Public providers only from an internal mirror**:
```hcl
provider_installation {
  network_mirror { url = "https://mirror.internal/tf/" }
  direct { exclude = ["registry.terraform.io/*/*"] }   # only non-public hosts go direct
}
```

**In-house provider during development**: use `dev_overrides` (a block inside `provider_installation`, Terraform 0.14+, must appear first). It forces Terraform to use a directory for the provider and disables version and checksum verification for it; other providers need a `direct {}` block. The docs recommend it only temporarily.

## 4. Filesystem mirror layout
- Packed: `HOSTNAME/NAMESPACE/TYPE/terraform-provider-TYPE_VERSION_TARGET.zip`
- Unpacked: `HOSTNAME/NAMESPACE/TYPE/VERSION/TARGET/` (a directory holding the extracted zip contents); Terraform symlinks it instead of copying.
- `VERSION` looks like `2.0.0`; `TARGET` like `linux_amd64`.

`terraform providers mirror` also generates `index.json` and per-version `<version>.json` files that, served from static hosting, are compatible with the network mirror protocol.

## Gotchas
- With no `provider_installation` block, Terraform builds an implied configuration from `filesystem_mirror` directories (for example `~/.terraform.d/plugins`, `terraform.d/plugins` in the working directory) plus an implied `direct` that excludes providers found there. An explicit block disables that: you must write the mirrors and exclusions yourself.
- A `network_mirror` URL must use the `https:` scheme and should end with a trailing slash. Only configure mirrors you trust: a mirror can serve modified provider copies.
- The config file is per user, not per project; in CI write it to a temp file and point `TF_CLI_CONFIG_FILE` at it.
- The plugin cache directory (`plugin_cache_dir` / `TF_PLUGIN_CACHE_DIR`) must not also be a filesystem mirror directory.

## Verify
- [ ] `terraform init` succeeds and installs the expected provider versions.
- [ ] Disconnecting the network (air-gapped case) still lets `init` succeed from the filesystem mirror.

## Checked
2026-10-28. Confirmed against the Terraform CLI configuration file page (provider installation, explicit installation method configuration, implied local mirror directories, dev_overrides, config file names, TF_CLI_CONFIG_FILE, plugin cache) and the provider network mirror protocol page (https scheme, trailing slash, index.json and version json files, `terraform providers mirror`).
Corrected: "methods are tried in order, first one wins" (the docs say all matching methods are consulted and the newest version wins); the unsupported `*` matches-one-segment rule.
Removed: the `h1:`-only lock-file claim and its cross-reference, the OpenTofu `.tofurc` / `registry.opentofu.org` note, the `TF_LOG=DEBUG` and "Installing ... from mirror" message claims, and the `provider not available for installation` error text (not in the fetched pages).
Method: documentation only; no commands were run.
