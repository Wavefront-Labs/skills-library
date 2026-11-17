---
id: computing-software.cloud-infrastructure-engineering.terraform.terraform-modules-directory-and-modules-json
name: terraform-modules-directory-and-modules-json
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, modules-json, terraform-get, module-installation, terraform-init, troubleshooting]
level: practitioner
status: docs-checked
description: "Understand .terraform/modules and modules.json: what init records per module, when init -upgrade or terraform get -update is needed, and what is safe to delete."
sources:
  - "https://developer.hashicorp.com/terraform/cli/commands/init#child-module-installation"
  - "https://developer.hashicorp.com/terraform/cli/commands/get"
  - "https://raw.githubusercontent.com/hashicorp/terraform/main/internal/modsdir/manifest.go"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `.terraform/modules` and `modules.json`

## What init does with modules
During `terraform init`, Terraform searches the configuration for `module` blocks and
retrieves the source code of each module from the location in its `source` argument.
Re-running init installs modules added since the last init but does not change any
module that is already installed. `-upgrade` overrides that and updates all modules to
the latest available source code. `-get=false` skips child module installation.

## The manifest (`modules.json`)
Terraform keeps a manifest of installed modules in a JSON file with a top-level
`Modules` array. In the Terraform source (`internal/modsdir/manifest.go`) each record has:

| Field | Meaning |
|---|---|
| `Key` | unique identifier from the module's position in the static module tree; nested keys are joined with `.` (the root module is the empty string) |
| `Source` | the source address given in configuration, normalised; used to detect that the source changed since the module was last installed, which forces a re-install |
| `Version` | the exact installed version; omitted for unversioned modules |
| `Dir` | the local directory where the module is installed (written with forward slashes so Linux and Windows can both read it) |

A missing manifest file is treated as empty. A manifest with two records for the same
`Key` is rejected as an error ("snapshot file contains two records"), which is why hand
editing it is a bad idea.

## Commands
```bash
terraform init                 # install modules added since last init, keep installed ones
terraform init -upgrade        # update modules (and plugins) to the latest allowed
terraform get -update          # modules only: check already-downloaded modules for updates
```
`terraform get` downloads and updates the modules declared in the root module into a
`.terraform` subdirectory. `-update` checks modules that are already downloaded for updates and
downloads them if present. The get page says not to commit that directory to version control.

## Inspect what is installed
Read `.terraform/modules/modules.json` with any JSON tool and look at `Key`, `Version`
and `Source` per record.

## Variables in module sources
Input variables are evaluated at plan time, so they are not available during `init` or
`get`. A variable referenced in a module block's `source` or `version` argument must
declare `const = true` (per the init and get pages).

## Gotchas
- Keep `.terraform/` out of version control.
- Changes made by hand inside the installed module directories are not something Terraform
  preserves across a re-install; fork the module or use a local path instead.
- Which error text appears when a module is missing or changed varies by Terraform
  version; run `terraform init` as the first response to any module-install complaint.

## Verify
- [ ] After `init -upgrade`, each `Version` in the manifest matches what the PR intends.

## Checked
Checked 2026-11-08 against the `terraform init` page (Child Module Installation, General
Options), the `terraform get` page and the Terraform `internal/modsdir/manifest.go` source
on GitHub. Removed: the example directory tree and JSON lines, the error/cause/fix table,
the claim that local modules are not copied, the `jq | column` command, and the `rm -rf
.terraform/modules` and backend-cache advice, none of which those pages state.
Method: docs-only read of cited pages, 2026-11-08
