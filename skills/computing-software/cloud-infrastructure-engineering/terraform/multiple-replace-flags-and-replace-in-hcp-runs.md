---
id: computing-software.cloud-infrastructure-engineering.terraform.multiple-replace-flags-and-replace-in-hcp-runs
name: multiple-replace-flags-and-replace-in-hcp-runs
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, multiple-replace, replace-hcp-run, forced-replacement, hcp-terraform]
level: practitioner
status: docs-checked
description: "Force replacement of several resource instances in one run with repeated -replace flags, and do the same in HCP Terraform via the CLI, the run UI and the API replace-addrs."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/plan#replace-address", "https://developer.hashicorp.com/terraform/cloud-docs/api-docs/run#create-a-run", "https://developer.hashicorp.com/terraform/cloud-docs/run/modes-and-options#replacing-selected-resources"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiple `-replace` and replace in HCP Terraform

## CLI
`-replace=ADDRESS` tells Terraform to plan to replace the resource instance at that
address, using a "replace" action when the resource would otherwise be updated or left
alone. Include the option several times to replace several objects at once:
```bash
terraform plan -out=tfplan \
  -replace='aws_instance.web["a"]' \
  -replace='aws_instance.web["b"]'
terraform apply tfplan
```
- It is useful when remote objects are degraded and you want replacements with the same
  configuration (immutable infrastructure style).
- Requires Terraform v0.15.2 or later (earlier versions used `terraform taint`).
- Cannot be combined with `-destroy`.
- `terraform apply -replace=ADDRESS` also works when applying without a saved plan.
- Quote addresses containing brackets and quotes for your shell.

## HCP Terraform (replace option, workspace needs Terraform CLI v0.15.2+)
- CLI: `terraform plan -replace=ADDRESS` or `terraform apply -replace=ADDRESS`.
- UI: workspace > **+ New run**, run type **Plan and apply (standard)**, then
  **Additional planning options** reveals **Replace resources**. Type an address; you can
  replace multiple resources.
- API: `POST /runs` with `data.attributes.replace-addrs`, an array of resource
  addresses passed to the `-replace` flag:
```json
{
  "data": {
    "type": "runs",
    "attributes": {
      "message": "replace web a,b",
      "replace-addrs": ["aws_instance.web[\"a\"]", "aws_instance.web[\"b\"]"]
    },
    "relationships": {
      "workspace": { "data": { "type": "workspaces", "id": "ws-LLGHCr4SWy28wyGN" } }
    }
  }
}
```
  Creating a run needs permission to queue plans for the workspace, and the endpoint
  cannot be used with organization tokens (use a user or team token). Responses: 201 on
  success; 404 for unknown workspace or no permission; 422 for a malformed body.
  `replace-addrs` can be combined with the other plan options listed in the request body
  table; `is-destroy` and `refresh-only` are mutually exclusive with each other.

## Checked
Date: 2026-11-07
Read in full: terraform plan command (cli/commands/plan, including -replace), Run modes and options (cloud-docs/run/modes-and-options, Replacing Selected Resources and the rest of the page) and the runs API (cloud-docs/api-docs/run, Create a Run and its request body table).
Confirmed: repeatable -replace, replace action semantics, v0.15.2 requirement and taint note, -destroy restriction; HCP CLI/UI/API options and UI path; replace-addrs attribute and the rest of the request details above.
Removed: the "state list | sed | xargs" pipeline, "each address must be a resource instance, not a module" (the page says instance but does not forbid others), `create_before_destroy` honoured, VCS-driven workspaces cannot express replace, `replace_triggered_by` advice, "non-matching address does not fail" gotcha, "-replace is ignored with -refresh-only", the curl command shape, and the Verify checklist (the "will be replaced, as requested" wording is not on these pages).
Not opened: the Resource Targeting and `taint` pages.
Method: documentation only; no commands were run.
