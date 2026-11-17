---
id: computing-software.cloud-infrastructure-engineering.terraform.digger-and-terramate-orchestration
name: digger-and-terramate-orchestration
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, digger, terramate, pr-automation, change-detection, monorepo, stacks, code-generation, github-actions]
level: advanced
status: docs-checked
description: "Orchestrate many Terraform roots in your own CI: Digger for PR plan/apply comments and locks, Terramate for stacks, change detection, ordering and code generation."
sources:
  - https://github.com/diggerhq/digger
  - https://docs.opentaco.dev/ce/reference/digger.yml
  - https://docs.opentaco.dev/ce/features/commentops
  - https://docs.opentaco.dev/ce/features/pr-level-locks
  - https://docs.opentaco.dev/onboarding/configuring-github-actions-workflow
  - https://github.com/terramate-io/terramate
  - https://terramate.io/docs/cli/stacks/configuration
  - https://terramate.io/docs/cli/change-detection/
  - https://terramate.io/docs/cli/code-generation/
  - https://terramate.io/docs/cli/orchestration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Digger and Terramate

Both run Terraform or OpenTofu inside your existing CI instead of a separate SaaS runner. **Terramate CLI** splits code into stacks, selects the changed ones, orders runs and generates files. **Digger** (the project is now branded OpenTaco; the docs live at docs.opentaco.dev) runs plan and apply from pull request comments, with PR-level locks, inside your CI.

## Terramate

A stack is a directory containing a `stack {}` block (the file name does not matter; `stack.tm.hcl` is conventional). One block per stack. Metadata and ordering attributes:
```hcl
stack {
  id          = "7b5f4d89-70a7-42f0-972f-3be8550e65df"
  name        = "My Awesome Stack Name"
  tags        = ["aws", "vpc"]
  after       = ["tag:prod:networking", "/prod/apps/auth"]
  watch       = ["/policies/mypolicy.json"]
}
```
- `id`: alphanumerics, dashes and underscores, at most 64 bytes, case-insensitive, unique in the project. `terramate create` defaults to a lowercase UUIDv4; `terramate create --ensure-stack-ids` adds ids to stacks missing one.
- `tags`: lowercase alphanumerics plus dashes, dots, slashes and underscores. The docs recommend tags rather than paths in `before` and `after`.
- `after` / `before`: stack paths, directory paths or `tag:` filters; they only set run order.
- `watch`: files whose changes mark the stack as changed.
- `wants` / `wanted_by`: force other stacks to run with this one. The docs call this an anti-pattern that widens the blast radius, and it does not alter run order.

Default run order: parent stacks run before their child stacks; sibling stacks that do not depend on each other can run in parallel. `terramate list --run-order` shows the order.

Commands (all documented):
```bash
terramate create path/to/stack            # new stack; --all-terraform adopts existing Terraform directories
terramate list --changed                  # stacks containing changes
terramate run --changed -- terraform init
terramate run --changed --parallel 5 -- terraform plan
terramate run --tags k8s:prd -- kubectl diff
terramate run --reverse terraform destroy # reverse order of execution
```

### Change detection
`--changed` uses Git. From v0.11.0, untracked and uncommitted files also count; configure this under `terramate { config { change_detection { git { untracked = "off" uncommitted = "off" } } } }` or with `--enable-change-detection` and `--disable-change-detection`. The Terraform integration marks a stack as changed when it references a changed local module outside the stack directory. `--git-change-base` sets the reference (for example `HEAD~2`).

Dependency filters widen or narrow the selection using data dependencies only (output sharing via `input.from_stack_id`, Terragrunt `dependency` blocks), not `before`/`after`/`wants`: for example `--include-all-dependencies`, `--only-all-dependents`, `--exclude-all-dependencies`. Only one `--only-*` flag can be used at a time.

### Code generation
`terramate generate` creates files from `generate_hcl` and `generate_file` blocks defined at the root or any directory above stacks; blocks inherit down the tree unless `inherit = false`. Typical use is backend and provider configuration:
```hcl
generate_hcl "_terramate_generated_backend.tf" {
  condition = tm_contains(terramate.stack.tags, "terraform")
  content {
    terraform {
      backend "s3" {
        bucket = global.terraform.backend.s3.bucket
        key    = "terraform/stacks/by-id/${terramate.stack.id}/terraform.tfstate"
        region = global.terraform.backend.s3.region
      }
    }
  }
}
```
Same-label blocks defined at different levels fail generation (no merging). The docs recommend committing generated files, prefixing them with `_terramate_generated_`, and note each file carries a "do not edit" header because edits are overwritten.

## Digger

Config is a `digger.yml` at the repository root (a different name can be set with the `digger-filename` action input):
```yaml
projects:
  - name: network-prod
    dir: stacks/prod/network
  - name: app-prod
    dir: stacks/prod/app
    depends_on: [network-prod]
auto_merge: false
```
- A project is a directory of Terraform; projects have their own locks, and Digger does not stop plans or applies in different projects running at the same time.
- `depends_on` lists projects that must complete first; it does not force a run, it affects the order for projects changed in the PR.
- `generate_projects` builds projects from directory globs (`include`, `exclude`, `blocks`). `apply_after_merge` runs apply after merge. `apply_requirements` accepts `approved`, `mergeable`, `undiverged` (default `mergeable`).
- `workflow_configuration` maps events to commands (defaults: `on_pull_request_pushed: [digger plan]`, `on_pull_request_closed: [digger unlock]`, `on_commit_to_default: [digger unlock]`).

PR comment commands: `digger plan`, `digger apply`, `digger lock`, `digger unlock`; `-p <project>` targets one project. `plan` locks and checks PR locks; `apply` checks locks, runs apply and unlocks when needed.

PR-level locks (`pr_locks`, default true) stop concurrent operations from different PRs on the same project. With the orchestrator backend they are stored in its database; in backendless mode (`no-backend: true`) you configure DynamoDB on AWS, a bucket on GCP or Storage Tables on Azure.

GitHub Actions step (inputs per the OpenTaco workflow page):
```yaml
- uses: diggerhq/digger@vLatest
  with:
    digger-spec: ${{ inputs.spec }}
    setup-aws: true
    aws-role-to-assume: arn:aws:iam::<ACCOUNT_ID>:role/<ROLE_NAME>
    aws-region: <REGION>
  env:
    GITHUB_CONTEXT: ${{ toJson(github) }}
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
Use either OIDC role assumption or static keys, not both; other `setup-*` inputs install OpenTofu, Terraform or Terragrunt.

## Choosing
- Many roots in a monorepo: Terramate for stacks, change detection, ordering and generation; run it from plain CI jobs or alongside Digger.
- Atlantis-style PR comments without hosting a server: Digger. Its README lists OPA-based RBAC, drift detection and apply-after-merge workflows.
- Digger's PR locks are "on top of" Terraform's native state locks, per its README, so keep backend locking.

## Gotchas
- Pick apply-before-merge or apply-after-merge (`apply_after_merge`) once per repository.

## Verify
- [ ] Editing a shared local module lists every consuming stack in `terramate list --changed`.
- [ ] A PR comment `digger plan` runs only the projects affected by the PR.
- [ ] A second PR touching a locked project is refused until the first is applied and merged or unlocked.

## Checked

Method: documentation only; no commands were run. Checked 2026-11-09 against the Terramate README and docs pages (stack configuration, change detection, code generation, orchestration, `terramate create`, `terramate run`) and against the Digger README and the OpenTaco docs (digger.yml reference, CommentOps, PR-level locks, GitHub Actions workflow page). Removed as not found in those pages: the claim that Digger reads Terramate stacks directly, the workflow permissions list, the `fetch-depth: 0` instruction, the Terramate "compare to main on PR branches and previous commit on main" detail, the claim that change detection never sees non-stack inputs such as `file()` reads (only `watch` is documented), and the earlier backend example (hard-coded bucket and key layout), replaced by the documented tag-conditional example. The `docs.digger.dev` host returned 404, so Digger claims come from docs.opentaco.dev.
