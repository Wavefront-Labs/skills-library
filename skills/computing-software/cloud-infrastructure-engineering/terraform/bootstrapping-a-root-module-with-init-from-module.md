---
id: computing-software.cloud-infrastructure-engineering.terraform.bootstrapping-a-root-module-with-init-from-module
name: bootstrapping-a-root-module-with-init-from-module
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, init-from-module, from-module, terraform-init, scaffolding, module-template, example-copy, bootstrap]
level: intro
status: docs-checked
description: "Use terraform init -from-module to copy a module or example configuration into an empty directory as a starting point, and how it differs from a module block."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/init#copy-a-source-module", "https://developer.hashicorp.com/terraform/language/modules/sources"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bootstrapping a root module with `init -from-module`

**Goal:** start a new configuration from a version-control source or an example
configuration in one command, instead of copy-pasting files.

## 1. Command
```bash
mkdir new-stack && cd new-stack
terraform init -from-module="git::https://example.com/vpc.git?ref=v1.2.0"
```
- By default `terraform init` assumes the working directory already holds a configuration.
  With `-from-module=MODULE-SOURCE`, `init` can be run against an **empty** directory: the
  given module is copied into the target directory before any other initialization
  steps are run.
- The init docs name two use-cases: a shorthand for checking out a configuration from
  version control and then initialising the working directory; and copying an example
  configuration into a local directory as the basis for a new configuration.
- For routine use the docs recommend checking out the configuration with the version
  control system's own commands instead, so you can pass extra flags to it and do
  other preparation (configuration generation, activating credentials) before
  `terraform init`.

## 2. Module sources and versions
- A module `source` can point to the public or a private Terraform registry, Git
  repositories, object storage services, or the local file system.
- For Git sources, Terraform clones the default branch (HEAD) unless the source has a
  `ref` query parameter; `ref` accepts anything `git checkout` accepts: a branch, SHA-1
  hash or tag, for example `git::https://example.com/vpc.git?ref=v1.2.0`. Pin a tag or
  hash when you want a reproducible copy.
- The `-from-module` copy is a snapshot of those files. A `module` block, by contrast,
  installs the module with `terraform init` and keeps it as a dependency, and re-running
  init with `-upgrade` updates already-installed modules to the latest source allowed by
  the version constraint.

## Checked
Date: 2026-11-07

Read in full (stripped text): the `terraform init` page (Copy a Source Module section and the rest) and the module-sources link's destination page, "Use modules in your configuration" (the old `modules/sources` URL redirects there; it describes `source`, `ref`, `version` and `-upgrade` but no longer lists every source address type). No code tabs present.

Trimmed as unconfirmed: the Terraform registry `//examples/complete` and `//subdir` examples; the claim that `version` cannot be given and registry sources use the latest version; S3/GCS/HTTP archive lists; "errors if the directory already contains .tf files" (the page only says to use an empty directory); "golden template" advice; the shell steps in "After the copy" (`rm -rf .terraform`, `sed`); the four Gotchas (nested `.git`, `.terraform` copied, relative `source` in examples, no HCP remote runs, no `terraform get` equivalent); both Verify steps.

Method: documentation only; no commands were run.
