---
id: computing-software.cloud-infrastructure-engineering.terraform.caching-providers-and-modules-in-ci
name: caching-providers-and-modules-in-ci
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, ci-cache, plugin-cache-dir, terraform-init, github-actions, gitlab-ci]
level: practitioner
status: docs-checked
description: "Speed up terraform init in CI with the provider plugin cache directory keyed on the lock file, in GitHub Actions and GitLab CI, and the plugin cache rules that bite in pipelines."
sources: ["https://developer.hashicorp.com/terraform/cli/config/config-file", "https://developer.hashicorp.com/terraform/cli/config/environment-variables", "https://developer.hashicorp.com/terraform/cli/commands/init", "https://github.com/actions/cache", "https://docs.gitlab.com/ci/caching/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Caching providers in CI

By default `terraform init` downloads plugins into a subdirectory of the working directory, so every configuration (and every fresh CI job) downloads its own copy; providers can be hundreds of megabytes. A shared plugin cache lets each plugin binary be downloaded once.

## Terraform side
- Enable with `plugin_cache_dir` in the CLI configuration file, or with the `TF_PLUGIN_CACHE_DIR` environment variable (an alternative way to set the same setting; the variable can override an existing cache directory for a shell session).
- The directory must already exist; Terraform will not create it.
- On Windows use forward slashes in the config file value (a backslash starts an escape sequence).
- `init` still uses the configured or implied installation methods to learn which plugins exist; once a version is chosen it checks the cache first, otherwise downloads into the cache and copies (symlinks when possible) into the working directory.
- By default Terraform uses a cached package only if it matches at least one checksum recorded in the dependency lock file. Commit `.terraform.lock.hcl` so the cache is usable on later runs. `plugin_cache_may_break_dependency_lock_file = true` (or `TF_PLUGIN_CACHE_MAY_BREAK_DEPENDENCY_LOCK_FILE`) overrides this; the page calls it for exceptional situations only and warns that the resulting lock file may be invalid on another OS or CPU architecture.
- Terraform never deletes plugins from the cache; remove unused versions yourself.
- The cache is not guaranteed concurrency safe: the behaviour with several `terraform init` calls at once is undefined, so avoid sharing one cache directory between parallel jobs on the same machine.
- The cache directory must not also be a configured or implied filesystem mirror directory.
- `terraform init -lockfile=readonly` suppresses lock file changes but verifies checksums against what is recorded; it conflicts with `-upgrade`.

## GitHub Actions
`actions/cache` inputs are `key`, `path` and `restore-keys` (ordered prefix-matched fallbacks); the README shows `hashFiles('**/lockfiles')` in a key so a new cache is created when dependencies change.
```yaml
env:
  TF_PLUGIN_CACHE_DIR: ${{ github.workspace }}/.terraform.d/plugin-cache
steps:
  - run: mkdir -p "$TF_PLUGIN_CACHE_DIR"
  - uses: actions/cache@v6
    with:
      path: ${{ env.TF_PLUGIN_CACHE_DIR }}
      key: tf-plugins-${{ runner.os }}-${{ hashFiles('**/.terraform.lock.hcl') }}
      restore-keys: tf-plugins-${{ runner.os }}-
  - run: terraform init -input=false -lockfile=readonly
```
The cache is scoped to key, version and branch; the default branch cache is available to other branches.

## GitLab CI
`cache:key:files` generates a key from the content of the listed files; paths are relative to the project directory and cannot point outside it. A job can have at most four caches, and caching is off unless the job defines `cache`.
```yaml
variables:
  TF_PLUGIN_CACHE_DIR: $CI_PROJECT_DIR/.terraform.d/plugin-cache
cache:
  key:
    files: [.terraform.lock.hcl]
  paths: [.terraform.d/plugin-cache]
```
Create the directory in `before_script` (`mkdir -p "$TF_PLUGIN_CACHE_DIR"`). Distributed caching (S3) or a single/shared runner is needed for runners to share a cache; different projects cannot share one.

## What not to cache
Cache the plugin cache directory rather than `.terraform/`: `TF_DATA_DIR`'s default location, `.terraform`, holds per-working-directory data such as the current backend configuration.

## Checked
Date: 2026-11-07. Read in full: the `terraform init` command page, the CLI environment variables page, and the CLI configuration file page (Provider Plugin Cache section and the lock-file override section). Read: the GitLab CI caching page (first 60 lines, cache vs artifacts, multiple caches) and the `actions/cache` README up to Inputs/Outputs/Cache scopes, with a search for hashFiles examples; the rest of both pages was not read. Corrections: the invented "aws ~600 MB unpacked", "Since TF 1.4" lock rule, `terraform providers lock -platform` advice, module-cache paragraph, monorepo paragraph and both Verify items were removed; `actions/cache@v4` changed to `@v6` as shown in the README; GitLab URL changed from the `/ee/` path (it redirects) to `docs.gitlab.com/ci/caching/`.
Method: documentation only; no commands were run.
