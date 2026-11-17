---
id: computing-software.cloud-infrastructure-engineering.terraform.reading-plan-output-and-diffs
name: reading-plan-output-and-diffs
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, plan-output, plan-review, reading-plans, saved-plan, terraform-plan, terraform-show, plan-json, replace, forces-replacement, known-after-apply, detailed-exitcode]
level: practitioner
status: docs-checked
description: "Read a terraform plan the way a reviewer does: action symbols, forces-replacement markers, saved plan files, terraform show -json change fields and -detailed-exitcode in CI."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/plan", "https://developer.hashicorp.com/terraform/cli/commands/show", "https://developer.hashicorp.com/terraform/internals/json-format"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading plan output and diffs safely

**Goal:** never approve an apply whose plan you have not read. The summary line (`Plan: 2 to add, 1 to change, 2 to destroy.`) is where reading starts, not ends.

## 1. The action symbols
The plan page documents four:
| Symbol | Action | Meaning |
|---|---|---|
| `+` | Create | resource does not exist; Terraform will create it |
| `-` | Destroy | Terraform will destroy it |
| `~` | In-place update | updated without destroying and recreating |
| `-/+` | Replace | destroyed, then recreated |

In the page's example, a replacement shows the cause on the attribute line, e.g. `~ ami = "ami-02c9..." -> "ami-0d7d..." # forces replacement`, and the block header reads `# aws_instance.web must be replaced`. A destroy shows `# (because aws_s3_bucket.old_bucket is not in configuration)`. The header legend also lists `-/+ destroy and then create replacement`.

## 2. Saved plans: review what will be applied
```bash
terraform plan -out=tfplan
terraform show tfplan
terraform show -json tfplan
terraform apply tfplan
```
- `-out=FILENAME` writes an opaque plan file you pass to `terraform apply`; the page says this two-step workflow is mainly for automation. Name it with a convention such as `tfplan`; a `.tf` suffix makes Terraform try to read it as configuration.
- The file contains your full configuration, all planned values and the input variables. Sensitive data, even if obscured in terminal output, is saved in cleartext: treat plan files as sensitive artifacts.
- Without `-out`, a plan is speculative. Other changes made meanwhile can alter the final effect, so re-check the final non-speculative plan before applying.
- `terraform show [file]` gives human-readable output of a state or plan file. `-json` for a plan file shows the plan, configuration and current state; sensitive values in state are shown in plain text with `-json`.
- To view a plan with `show -json`, it must have been created without `-refresh=false`.

## 3. Reading the JSON plan (`terraform show -json <planfile>`)
Per `resource_changes[]` element, `change` holds:
- `actions`: `["no-op"]`, `["create"]`, `["read"]`, `["update"]`, `["delete","create"]` (replace), `["create","delete"]` (the other replace order) or `["delete"]`. Scan for `"delete"` to catch all three situations where an object is deleted.
- `before` / `after`; `after_unknown` marks leaf values only known after apply (`true`); `before_sensitive` / `after_sensitive` mark sensitive leaves, to combine with `before`/`after` so you do not display secrets.
- `replace_paths`: arrays of paths naming the attributes that caused a replace; omitted if the action is not replace or no path caused it (for example a tainted resource).
- `importing`: present only when the object is being imported by this change.
- `action_reason` (on the resource change, optional display hint) gives codes such as `replace_because_tainted`, `replace_because_cannot_update`, `replace_by_request`, `delete_because_no_resource_config`, `delete_because_count_index`, `delete_because_each_key`, `read_because_config_unknown`, `read_because_dependency_pending`. Treat unknown codes as unspecified.
- `previous_address` appears only if the address changed, for example through a `moved` block.
- Top level: `applyable`, `complete` (false means at least one more plan/apply round is expected), `errored`, `resource_drift` (changes found comparing latest state to prior saved state), `output_changes` (actions only create/update/delete), `checks`.
- Ignore properties with unrecognised names, and reject an unsupported major `format_version` (currently "1.0").

## 4. CI exit codes
`terraform plan -detailed-exitcode` returns 0 for success with an empty diff, 1 for error and 2 for success with a non-empty diff. Use 2 to route a plan to approval.

## 5. Reading order
1. Summary line: does the destroy count match your intent?
2. Every `-` and `-/+` block and its `forces replacement` attribute: intended, or a typo?
3. `~` changes on security-relevant attributes.
4. Warnings and any output changes.
5. With JSON: `complete` and `applyable`, and `resource_drift` for edits made outside Terraform.

## Cautions
- `-refresh=false` skips synchronising state with remote objects: faster, but ignores external changes and can give an incomplete or incorrect plan. `-minimal-refresh` has the same caveat; avoid both when upgrading providers.
- `-target` is for exceptional circumstances only, as it can cause undetected drift.
- `-generate-config-out=PATH` (experimental) writes HCL for import blocks lacking configuration, into a file that must not already exist.

## Checked
Date: 2026-11-07. Read in full: `terraform plan`, `terraform show` and the JSON output format page. Removed because none of the three states them: the `+/-` and `<=` symbols, "Saved plan is stale", the grep and jq commands, the "(N unchanged attributes hidden)" claim, the "typical causes" list, the "Objects have changed outside of Terraform" message wording and the Verify list. Added from the pages: the confirmed symbol table, plan-file sensitivity, the JSON change fields and exit codes.
Method: documentation only; no commands were run.
