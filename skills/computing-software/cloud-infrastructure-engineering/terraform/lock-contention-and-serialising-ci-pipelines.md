---
id: computing-software.cloud-infrastructure-engineering.terraform.lock-contention-and-serialising-ci-pipelines
name: lock-contention-and-serialising-ci-pipelines
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, lock-contention, state-locking, concurrency-group, ci-cd, lock-timeout]
level: practitioner
status: docs-checked
description: "Stop CI runs colliding on the same state: concurrency groups per state key, -lock-timeout, the risk of -lock=false, and splitting hot states."
sources: ["https://developer.hashicorp.com/terraform/language/state/locking", "https://developer.hashicorp.com/terraform/cli/commands/plan", "https://developer.hashicorp.com/terraform/cli/commands/apply", "https://docs.github.com/en/actions/using-jobs/using-concurrency", "https://docs.gitlab.com/ee/ci/resource_groups/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lock contention in CI

Terraform locks state for all operations that could write state, if the backend supports
locking. If acquiring the lock fails, Terraform does not continue. In CI that shows up as:
- PR plans failing randomly because another run holds the lock.
- Merge applies failing because a scheduled job holds the lock.
- Many PRs against one monolithic state colliding.

## Fixes, cheapest first
1. **Serialise per state in the CI system** so runs wait instead of fail.
GitHub Actions allows at most one running job per concurrency group. By default only one
run can be pending: a newer queued run replaces the older pending one. Set `queue: max` to
let up to 100 runs wait in FIFO order (it cannot be combined with `cancel-in-progress: true`).
```yaml
# GitHub Actions
concurrency:
  group: tf-${{ inputs.stack }}-${{ inputs.env }}
  queue: max
```
GitLab: put the apply job in a resource group so jobs run one at a time:
```yaml
apply:prod:
  resource_group: tf-payments-prod
```
The GitLab default process mode is `unordered`; `oldest_first` runs jobs in pipeline order
(the page calls it safer for continuous deployments) and is set through the API.
2. **Wait instead of fail**: `-lock-timeout=DURATION` on `terraform plan` and `terraform apply`
   retries acquiring the lock for that long before returning an error. Duration syntax is a
   number followed by a time unit letter, for example `3s`.
3. **`-lock=false`** means "don't hold a state lock during the operation". The plan and apply
   docs call this dangerous if others might concurrently run commands against the same
   workspace, and the locking docs do not recommend it. Do not use it on apply.
4. **Split hot states**: if many teams touch one state, split by ownership (network,
   platform, app) so locks are independent. The plan docs also recommend several smaller
   configurations over one very large one.

## Scheduled jobs
- Run drift checks outside merge windows, with `-lock-timeout`, and in the same concurrency
  group as applies so they queue rather than collide.
- `-refresh-only` is an alternative plan mode that only updates state and root outputs to match
  remote objects; `-detailed-exitcode` returns 0 for no changes, 1 for error, 2 for changes
  present.

## Gotchas
- `cancel-in-progress: true` cancels the running job. Do not set it on an apply job:
  Terraform is interrupted mid-operation. The locking docs cover `terraform force-unlock`
  for when automatic unlocking failed; it needs the lock ID Terraform prints, and should
  only unlock your own lock.
- GitHub group names are case insensitive and must be unique across workflows in the
  repository, otherwise unrelated runs cancel each other. Make them per state key, not per repo.
- After an apply error Terraform updates state, unlocks, and exits; it does not roll back a
  partially completed apply.

## Checked
Date: 2026-11-07. Read in full: Terraform "State Locking", `terraform plan` and `terraform apply` command pages, GitHub "Control the concurrency of workflows and jobs" and GitLab "Resource group". Confirmed: lock behaviour, `-lock=false` wording, `-lock-timeout=DURATION` on both plan and apply with the "3s" syntax, `-refresh-only`, `-detailed-exitcode` exit codes, force-unlock wording, GitHub default pending-replacement, `queue: max` (100, FIFO, incompatible with cancel-in-progress true), case-insensitive group names, `inputs` allowed in group expressions, GitLab `resource_group` and process modes (set via API). Corrections: the old "runs queue instead of failing" with `cancel-in-progress: false` was wrong by default (pending runs get replaced), so the example uses `queue: max`; removed `-lock-timeout=10m/15m` examples (only `3s` syntax is shown), the "plan never writes state / can read state mid-apply" claim, the HCP Terraform speculative-plan and queue claims, the claim that drift checks always lock, the invented error string, and the Verify steps. The GitLab page's job-ordering internals and the force-unlock command page were not needed beyond what the locking page states.
Method: documentation only; no commands were run.
