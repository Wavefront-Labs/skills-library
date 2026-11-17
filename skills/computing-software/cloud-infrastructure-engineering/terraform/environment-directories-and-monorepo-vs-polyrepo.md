---
id: computing-software.cloud-infrastructure-engineering.terraform.environment-directories-and-monorepo-vs-polyrepo
name: environment-directories-and-monorepo-vs-polyrepo
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, env-directories, per-environment-dirs, monorepo, polyrepo, repository-layout, root-modules]
level: advanced
status: docs-checked
description: "Lay out root modules as per-environment directories and choose monorepo vs polyrepo for modules and live config, with the CI and versioning consequences of each."
sources: ["https://developer.hashicorp.com/terraform/language/modules/develop/structure", "https://developer.hashicorp.com/terraform/language/state/workspaces", "https://developer.hashicorp.com/terraform/language/modules/sources", "https://developer.hashicorp.com/terraform/registry/modules/publish"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Environment directories; monorepo vs polyrepo

## Per-environment directories
```
live/
  prod/
    network/   backend.tf main.tf terraform.tfvars
    app/
  staging/
    network/
    app/
modules/
  network/  app/
```
- Each leaf is a root module with its own backend configuration and state key, so state, credentials and blast radius are separate per environment.
- Differences between envs are explicit (tfvars, module versions). Prod can pin an older module release while staging tests a newer one, using a git source with a `ref`: `source = "git::https://example.com/app.git?ref=v1.8.0"`.
- Duplication of `main.tf` across envs is the cost; keep leaves thin (one or two module calls).

Versus CLI workspaces for environments: the Terraform docs state that workspaces are not appropriate for system decomposition or for deployments requiring separate credentials and access controls. Workspaces give several states under one backend configuration, so they suit multiple instances of one configuration, not prod versus dev isolation.

## Monorepo
Modules and live config in one repo.
- Pro: atomic changes across module and usage, one CI, easy discovery.
- Con: a module referenced by local path has no release version of its own, so a change reaches every consumer at once unless consumers pin a git ref; CI must work out which roots changed.

## Polyrepo
One repo per module, live config separate.
- Pro: modules published to a registry get version numbers from git tags. The public Registry needs the repo named `terraform-<PROVIDER>-<NAME>` and release tags that are semantic versions (optionally `v`-prefixed, for example `v1.0.1`).
- Con: cross-repo changes need multiple PRs and consumers must bump version pins.

## Common hybrid
- Shared modules in their own repos (or a modules monorepo consumed through pinned git refs).
- Live config: one repo of env directories pinning module versions.

## Gotchas
- Never have two roots share a backend state key.
- Copy-pasting a whole env directory to create a new env carries the old backend key; change it before `terraform init`.
- Keep a predictable `live/<env>/<stack>` pattern so CI path filters stay simple.

## Verify
- [ ] No state key is shared by two roots (`grep -rh 'key *=' live/ | sort | uniq -d` prints nothing).
- [ ] CI runs plan only for roots whose files (or referenced local modules) changed.

## Checked

Method: docs-checked 2026-11-09 against the module structure page, CLI workspaces page, module sources page (git `ref` pinning) and the registry publish page (naming and semver tags), downloaded, converted to text and read. Dropped unconfirmed claims: the Terragrunt, Terramate, Atlantis `autoplan.when_modified` and Renovate references, the `vpc/v1.2.0` per-module tag scheme, and the recommended-practices source (not read).
