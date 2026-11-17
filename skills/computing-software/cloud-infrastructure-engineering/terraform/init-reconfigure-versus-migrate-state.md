---
id: computing-software.cloud-infrastructure-engineering.terraform.init-reconfigure-versus-migrate-state
name: init-reconfigure-versus-migrate-state
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, init-reconfigure, init-migrate-state, terraform-init, backend-change, backend-migration, force-copy, backend-configuration-changed]
level: practitioner
status: gated
description: "Pick -reconfigure or -migrate-state when init says the backend configuration changed: which one copies state, which one abandons it, and how to not lose state either way."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/init#backend-initialization", "https://developer.hashicorp.com/terraform/language/backend#change-configuration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `init -reconfigure` vs `init -migrate-state`

**Goal:** answer the "Backend configuration changed" error with the right flag,
every time.

## 1. The error
```
Error: Backend configuration changed
A change in the backend configuration has been detected, which may require
migrating existing state.
If you wish to attempt automatic migration of the state, run "terraform init
-migrate-state".
If you wish to store the current configuration with no changes to the state,
run "terraform init -reconfigure".
```
Terraform compares the `backend` block (or `cloud` block, or `-backend-config`
values) with what is cached in `.terraform/terraform.tfstate`. Any difference —
bucket, key, region, a new `-backend-config` value, even workspace prefix — triggers
it.

## 2. Decide
| You changed | State should | Flag |
|---|---|---|
| Where state lives (new bucket/key/backend type) and the old location still holds the real state | be **copied** to the new location | `-migrate-state` |
| Only an irrelevant setting (profile, role_arn, endpoint, `use_lockfile`) and the state object is the same | stay where it is; just re-record the config | `-reconfigure` |
| Pointed at a location that already contains the right state (e.g. a colleague migrated it already) | not be copied (would be a conflict) | `-reconfigure` |
| Switching to the `cloud` block | be copied to HCP Terraform | `-migrate-state` (interactive prompt; `-force-copy` to skip) |

Rule of thumb: `-reconfigure` says "trust the new config, forget the old"; the docs say it
"disregards any existing configuration, preventing migration of any existing state". (Edge case seen on 1.17.0: with
the local backend and a leftover default `terraform.tfstate` file in the working directory, `-reconfigure`
still asked whether to copy that file, so remove stray local state files first.) `-migrate-state` says "pull from old, push to new".

## 3. Migration run
```bash
terraform state pull > pre-migration.tfstate     # backup from the OLD backend first
# edit backend block
terraform init -migrate-state
# answer "yes" to "Do you want to copy existing state to the new backend?"
terraform state list                              # same resources as before
terraform plan                                    # must be no changes
```
Non-interactive: `terraform init -migrate-state -force-copy -input=false`.
If the destination already has a state with a different lineage Terraform asks
whether to overwrite; say **no** and investigate.

## 4. Workspaces
With multiple CLI workspaces, `-migrate-state` offers to migrate all of them
(backend→backend) or asks for a new workspace name when going from a
multi-workspace backend to a single-workspace one. Check `terraform workspace list`
on both sides afterwards.

## Gotchas
- `-reconfigure` after accidentally editing the `key` points Terraform at an
  **empty** state; the next plan wants to create everything. If the plan shows
  mass creation, stop — you reconfigured when you should have migrated (or the key
  is wrong).
- Both flags are mutually exclusive: `init -reconfigure -migrate-state` fails with `Error: Invalid init options` ("The -migrate-state and -reconfigure options are mutually-exclusive").
- `-backend-config` values are part of the comparison: passing different values
  per environment on the same working directory requires `-reconfigure` each
  switch (common in CI with one checkout, many envs). Use separate directories or
  `TF_DATA_DIR` per env to avoid thrash.
- `.terraform/terraform.tfstate` is the cache (not real state); deleting
  `.terraform/` also clears the error but loses the module/provider cache.

## Verify
- [ ] `terraform plan` right after init shows `No changes` (migration) — or exactly the expected diff.
- [ ] `terraform state pull | jq .lineage` matches the pre-migration backup.
- [ ] Old backend location is emptied or marked read-only only after the new one has been applied against at least once.

## Checked
- Terraform 1.17.0, local backend with `-backend-config="path=..."`: changing the path gave `Error: Backend configuration changed` with the `run "terraform init -migrate-state"` wording shown; `-reconfigure` to a new empty path then `plan` proposed `Plan: 1 to add` (empty state), so the "mass creation" gotcha is real; `-migrate-state -force-copy -input=false` copied the state (new file created, `plan` showed `No changes`) and the lineage and serial in `state pull` were unchanged; without `-force-copy` it asked `Do you want to copy existing state to the new backend?`; both flags together errored.
- Docs fetched (init command page) for the `-reconfigure` wording.
- The cloud-block migration row and `-force-copy` for the `cloud` block, the S3 examples (`profile`, `role_arn`, `use_lockfile`), multi-workspace backend-to-backend migration prompts and the "different lineage, say no" prompt were not run (gated: unconfirmed, source is paywalled or blocked). The reason is that no HCP or S3 access was available.
