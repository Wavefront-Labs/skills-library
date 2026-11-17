---
id: computing-software.devops-ci-cd.nomad.job-plan
name: job-plan
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, job-plan, plan, dry-run, check-index, exit-codes, diff, scheduler, policy-override, var-file, cli]
level: practitioner
status: docs-checked
description: "Dry-run a Nomad job change with nomad job plan, read the diff and scheduler output, use exit codes 0 1 255, and pass the job modify index to job run -check-index."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/commands/job/plan.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nomad job plan

Alias: `nomad plan`. Invokes the scheduler in dry-run mode for a new or updated job and reports what would happen; it changes nothing.

```
nomad job plan [options] <path>
```
`<path>` is an HCL (or `-json`) job file, `-` for stdin, or a URL fetched with go-getter. If the job specifies a region, that overrides `-region` and `NOMAD_REGION`. With ACLs enabled you need `submit-job` in the job's namespace.

## Output
A structured diff of local versus remote job (`+` create, `-` destroy, `+/-` update, "forces create" / "forces create/destroy update" flags), a **Scheduler dry-run** section (for example `WARNING: Failed to place all allocations` with `Resources exhausted on 1 nodes` or `Dimension "cpu" exhausted`, or `Rolling update, next evaluation will be in 10s`), and a **Job Modify Index**.

## Safe submit flow
```
nomad job plan example.nomad.hcl
nomad job run -check-index 15 example.nomad.hcl
```
`-check-index` makes the run fail if someone modified the job after your plan, so the plan's conclusions still hold (`computing-software.devops-ci-cd.nomad.job-run`).

## Exit codes
- `0` no allocations created or destroyed
- `1` allocations created or destroyed
- `255` error determining the plan

Use these in CI to gate on whether the plan changes anything.

## Options
`-diff` (default true), `-verbose` (full diff of every field, including defaults like `LogConfig`), `-json`, `-hcl2-strict` (default true; error on `-var` not declared in the file), `-var key=value` (repeatable), `-var-file=<path>`, `-policy-override` (override soft-mandatory Sentinel policies), `-vault-namespace`.

## Gotcha
A plan that shows `(forces create/destroy update)` on a count change means resource-heavy rollouts; check the scheduler section for placement failures before running.

## Checked

2026-11-03. Confirmed against the commands/job/plan page (HashiCorp web-unified-docs, Nomad v1.10.x): parameters, defaults, option and flag names, exit codes and examples. Removed: a paraphrase of the exit-code use in CI.

Method: documentation only; no commands were run.
