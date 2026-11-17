---
id: computing-software.cloud-infrastructure-engineering.terraform.test-state-key-and-parallel-run-blocks
name: test-state-key-and-parallel-run-blocks
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, test-state-key, parallel-run-blocks, terraform-test, run-block]
level: practitioner
status: verified
description: "Control how terraform test shares state between run blocks with state_key, and run independent run blocks in parallel (Terraform 1.12+) without them colliding."
sources: ["https://developer.hashicorp.com/terraform/language/tests#state-key", "https://developer.hashicorp.com/terraform/language/tests#parallel", "https://developer.hashicorp.com/terraform/cli/commands/test"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# `state_key` and parallel runs

## Default state sharing
`terraform test` keeps one in-memory state **per module source**: every run block
against the main module shares a state; each helper module (`module { source = ... }`)
gets its own. So run 2 sees the resources run 1 created and plans changes against
them (run: a `plan` run with a new `name` showed `local_file.f must be replaced`).

## state_key (TF 1.11+)
Give runs explicit state buckets:
```hcl
run "blue" {
  state_key = "blue"
  variables { name = "blue" }
}
run "green" {
  state_key = "green"            # separate state: creates its own copy of the module
  variables { name = "green" }
}
run "blue_update" {
  state_key = "blue"             # continues from the "blue" state
  variables {
    name = "blue"
    size = "large"
  }
}
```
Use it to test two independent instances of the same module, or to keep an update
test isolated from a create test. Ran with `hashicorp/local`: `green` started from
an empty state (`will be created`) and `blue_update` changed `blue`'s content in
place. `state_key` is in the v1.11 changelog.

## Parallel runs (TF 1.12+)
```hcl
test {
  parallel = true                # file-level default
}
run "a" { state_key = "a" }
run "b" { state_key = "b" }
run "c" {
  parallel = false               # opt out for this run
}
```
Per the 1.12 changelog runs can be annotated for parallel execution. Observed: with
`parallel = true` and separate keys the runs finished out of order (`b` reported
before `a`); two runs without `state_key` in a `parallel = true` file simply ran
(sequentially, no error); a run that referenced `run.a.name` still passed.
`terraform test -parallelism=N` limits concurrent operations (1.12 changelog).

## Cleanup order
Destroy happens in reverse run block order (v1.7 changelog); the 1.13 changelog adds
parallel execution of teardown operations.

## Gotchas
- Parallel states that manage the same real object (a fixed bucket or file name) can
  fight over it; give each state its own name, for example from a setup run's output.
- Terraform 1.9.8 rejects both: `Unsupported block type` for `test {}` and
  `Unsupported argument` for `state_key`; set `required_version` accordingly.

## Verify
- [ ] `terraform test -verbose` shows a `will be created` plan for the first run of each new key and an update (not a create) for a repeated key.

## Checked
- Terraform 1.17.0 with `hashicorp/local`: ran `state_key` blue/green/blue_update (verbose output), a `test { parallel = true }` file with per-run `parallel = false` and a dependent `run.a.name` reference, a parallel file without keys, and a non-keyed file showing shared state (`must be replaced`) against a `state_key = "other"` run (`will be created`). Terraform 1.9.8 rejected `test {}` and `state_key`.
- Changelogs v1.7, v1.11, v1.12, v1.13. Real parallel timing was not measured (only out-of-order completion was observed).
