---
id: computing-software.cloud-infrastructure-engineering.terraform.terraform-plan-visualisation-tools
name: terraform-plan-visualisation-tools
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, plan-visualisation, tf-summarize, terraform-show-json, rover, plan-review]
level: practitioner
status: docs-checked
description: "Make Terraform plans reviewable: use terraform show -json as the source, summarise with tf-summarize, graph with rover or terraform graph, and surface destroys and replacements."
sources:
  - https://developer.hashicorp.com/terraform/internals/json-format
  - https://developer.hashicorp.com/terraform/cli/commands/show
  - https://developer.hashicorp.com/terraform/cli/commands/graph
  - https://github.com/dineshba/tf-summarize/blob/main/README.md
  - https://github.com/im2nguyen/rover/blob/main/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Plan visualisation tools

Raw `terraform plan` output for hundreds of resources hides the two things a reviewer must catch: destroys or replacements, and changes to sensitive resources.

## Plan JSON is the source
```bash
terraform plan -out=tfplan
terraform show -json tfplan > plan.json
jq -r '.resource_changes[] | select(.change.actions != ["no-op"]) | "\(.change.actions|join(",")) \(.address)"' plan.json
jq -r '.resource_changes[] | select(.change.actions | index("delete")) | .address' plan.json
jq -r '.resource_changes[] | select(.change.replace_paths) | "\(.address) <- \(.change.replace_paths)"' plan.json
```
- Valid `actions` values are `["no-op"]`, `["create"]`, `["read"]`, `["update"]`, `["delete","create"]`, `["create","delete"]` and `["delete"]`. The two replace forms are ordered lists so scanning for `"delete"` finds all three situations where the object is deleted.
- `replace_paths` lists the attribute paths that caused a replacement; it is omitted when the action is not replace or when no path caused it (for example a tainted resource).
- `before_sensitive` and `after_sensitive` mark sensitive leaves; combine them with `before`/`after` before displaying values in a UI.
- `terraform show -json` on a state file prints sensitive values in plain text. A plan to be viewed must not have been created with `-refresh=false`.
- `format_version` identifies the JSON format version; check it in your tooling.

## tf-summarize
```bash
tf-summarize tfplan                    # table
tf-summarize -tree tfplan              # tree
tf-summarize -tree -draw tfplan        # 2D tree (-draw works only with -tree or -separate-tree)
tf-summarize -md tfplan                # markdown table (-md works only with the table view)
tf-summarize -json-sum tfplan          # summary as JSON
tf-summarize -out=summary.md tfplan    # write to a file
```
It accepts a plan file or the JSON from `terraform show -json tfplan`. The Docker image has no Terraform binary, so it only works with JSON files. With `hashicorp/setup-terraform` set `terraform_wrapper` to false.

## Graphs
- Rover (`im2nguyen/rover`) generates an interactive visualisation served on port 9000; `-planJSONPath plan.json` visualises an existing plan JSON (Unix LF, UTF-8); `-standalone true` writes a `rover.zip` of static assets; `-genImage true` saves an SVG.
- `terraform graph` prints DOT of the dependency ordering of `resource` and `data` blocks. `-type=plan`, `plan-refresh-only`, `plan-destroy` or `apply` give more detailed graphs; `-draw-cycles` highlights cycles when diagnosing cycle errors. Render with Graphviz: `terraform graph -type=plan | dot -Tpng > graph.png`. Judgement: the raw graph is useful for cycles but too noisy for review.

## Make danger obvious
- Fail or require extra approval when the plan JSON deletes protected resource types: select `resource_changes` entries by `.type` and an `actions` list containing `"delete"` (the jq above is a start); feed the same JSON to a policy engine (see `computing-software.cloud-infrastructure-engineering.terraform.policy-as-code-with-sentinel-and-opa`).
- Judgement: post a short summary in the PR with deletes and replacements listed first, and link the full plan artifact rather than pasting it (hosting platforms limit comment size).

## Verify
- [ ] Every Terraform PR has a summary listing deletes and replacements first.
- [ ] A plan that deletes a protected resource is blocked or escalated by policy.
- [ ] Plan JSON artifacts are treated as sensitive.

## Checked
2026-11-09

Method: read the Terraform JSON output format, show and graph command pages (fetched as text) and the tf-summarize and rover READMEs (raw GitHub). Removed as unsupported by those sources: the tfcmt, inframap and Pluralith recommendations, the GitHub 65,536 character limit, the Rego example, and the `-lock=false` flag. Corrected: `tf-summarize -draw` needs `-tree`, and rover's binary form is `rover -planJSONPath` (the README shows the Docker form).
