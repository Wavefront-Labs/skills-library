---
id: computing-software.cloud-infrastructure-engineering.terraform.performance-at-scale
name: performance-at-scale
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, performance, parallelism, plugin-cache, large-state, plan-speed, apply-speed, graph-complexity, provider-rate-limiting, refresh-performance, state-size, root-module-splitting, terraform-plugin-cache-dir]
level: advanced
status: docs-checked
description: "Keep Terraform plan/apply fast as a state grows: diagnose with TF_LOG, tune -parallelism, use the plugin cache, trade refresh safety for speed, and split roots only for a reason."
sources:
  - https://developer.hashicorp.com/terraform/cli/commands/plan
  - https://developer.hashicorp.com/terraform/cli/config/config-file
  - https://developer.hashicorp.com/terraform/cli/config/environment-variables
  - https://developer.hashicorp.com/terraform/internals/debugging
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Terraform performance at scale

**Goal:** a root module holding thousands of resources still plans in a reasonable time. Find the bottleneck (refresh API calls, graph, or local I/O such as provider downloads) and fix that, instead of splitting every root.

## 1. Diagnose before fixing
```bash
export TF_LOG=trace TF_LOG_PATH=plan-trace.log
terraform plan
```
`TF_LOG` writes detailed logs to stderr (levels TRACE, DEBUG, INFO, WARN, ERROR); `TF_LOG_PATH` persists them but `TF_LOG` must also be set. Use the timestamps to see which phase dominates. Judgement, not from the docs: for large states the refresh (reading every managed resource) is usually the biggest cost, so confirm before assuming the graph is the problem.

## 2. `-parallelism`
`-parallelism=n` limits concurrent operations while walking the graph; the default is 10. A higher value can speed refresh and apply only if the target API tolerates the burst. Provider-side rate limits are a real ceiling (judgement): tune per root and watch for throttling errors in the trace.

## 3. Provider plugin cache
```hcl
# CLI configuration file (~/.terraformrc)
plugin_cache_dir = "$HOME/.terraform.d/plugin-cache"
```
or `export TF_PLUGIN_CACHE_DIR=...`.
- The directory must already exist. On Windows use forward slashes.
- `terraform init` checks the cache first; if the provider is missing it downloads it into the cache, then copies (or symlinks where possible) it into the working directory.
- This speeds `init`, not plan or apply.
- The cache is not guaranteed concurrency safe: parallel `init` calls have undefined behaviour. Terraform never deletes old plugins from it.
- The cache must not also be a filesystem mirror directory.

## 4. Refresh cost
- `-refresh=false` skips synchronising state with real objects. Faster, but ignores external changes and can give an incomplete or incorrect plan.
- `-minimal-refresh` refreshes only resource instances that have planned changes; it has the same drawback, and cannot be combined with `-refresh=false` or used in refresh-only mode.
- Avoid both when upgrading provider versions so state picks up schema changes.
- `-refresh-only` is a different mode (it only refreshes), and cannot be combined with `-refresh=false`.
- `TF_CLI_ARGS_plan="-refresh=false"` can set an option for plans only.
- `-target` is for exceptional circumstances only, not routine speed-ups; do not apply a targeted plan as your normal artifact.
- Judgement: expensive data sources instantiated inside a module that is called many times multiply their cost; compute once and pass the result down.

## 5. When to split a root
Split when the dependency graph or the blast radius is the real problem, not for speed alone (judgement). See `computing-software.cloud-infrastructure-engineering.terraform.large-scale-refactoring-and-state-surgery` for doing it safely.

## 6. CI
Caching the plugin cache directory between runs avoids repeated provider downloads (judgement; key it on the lock file). Saved plans (`-out`) are cleartext and sensitive; treat them as secrets.

## Gotchas
- Raising `-parallelism` on a shared cloud account can throttle other callers of the same API (judgement).
- Trace logs include sensitive data; do not share them unredacted.

## Verify
- [ ] A trace timeline identifies the dominant phase before any change.
- [ ] After each change, plan time is measured again and recorded.
- [ ] `-refresh=false` and `-minimal-refresh` are not used for plans you apply after provider upgrades.

## Checked
2026-11-09

Method: read the Terraform plan command page, CLI configuration file (plugin cache), environment variables and debugging pages (fetched as text). Removed as unsupported by those pages: the claim that 429 responses are retried by Terraform with backoff, the Stacks remark, the CI cache-key detail beyond judgement, and the "symlink vs copy differs by OS" assertion (docs say symlinks are used where possible). Statements marked judgement are experience-based, not from the sources.
