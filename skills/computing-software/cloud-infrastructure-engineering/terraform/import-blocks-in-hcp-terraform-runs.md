---
id: computing-software.cloud-infrastructure-engineering.terraform.import-blocks-in-hcp-terraform-runs
name: import-blocks-in-hcp-terraform-runs
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, import-hcp-run, import-block, hcp-terraform, vcs-driven-runs]
level: practitioner
status: docs-checked
description: "Use import blocks in a VCS-driven HCP Terraform workflow: speculative plans on pull requests, applying after merge, generated configuration, and the documented import limitations."
sources: ["https://developer.hashicorp.com/terraform/language/import", "https://developer.hashicorp.com/terraform/cloud-docs/run/ui", "https://developer.hashicorp.com/terraform/tutorials/state/state-import"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `import` blocks with HCP Terraform VCS-driven runs

As of Terraform 1.5 configuration-driven import brings existing resources into state
through the plan-and-apply workflow. The tutorial says it is safer than the
`terraform import` command, works with CI/CD pipelines and lets you preview the
import before state is modified.

## Workflow in a VCS-driven workspace
1. In a pull request, add the resource block and an `import` block. The `import`
   block needs `id` (the provider-specific identifier of the infrastructure) and
   `to` (the address Terraform gives the resource in state), and the configuration
   needs a matching destination `resource` block:
```hcl
import {
  to = aws_s3_bucket.legacy_logs
  id = "corp-legacy-logs"
}
resource "aws_s3_bucket" "legacy_logs" {
  bucket = "corp-legacy-logs"
}
```
2. HCP Terraform runs a speculative plan when the pull request is opened against the
   workspace's branch, posts a link to it in the pull request and re-runs it when
   the pull request is updated. A plan that imports reports a summary such as
   `Plan: 1 to import, 0 to add, 0 to change, 0 to destroy.` Review it for planned
   destroys before merging.
3. When the change is merged to the linked branch, HCP Terraform queues a run. By
   default, plans need confirmation ("Confirm & Apply"), unless auto apply is
   enabled on the workspace.

## Rules to remember
- The `id` format is resource-specific; find it in the provider documentation for
  the resource.
- Speculative plans run only for pull requests from within the same repository, not
  from forks, and only in workspaces connected to the destination branch (and, if
  configured, with matching trigger directories). Terraform Enterprise
  administrators can allow fork pull requests.
- A new VCS-driven workspace needs an initial run queued manually; a workspace with
  no runs does not accept runs from the VCS webhook.
- Speculative plans use the head branch and compare against the workspace's current
  state at plan time, so the result can differ if the destination branch has moved.

## Generating configuration
The tutorial runs `terraform plan -generate-config-out=generated.tf` to produce
resource blocks for the import blocks, then prunes the output to required arguments
and arguments whose values differ from defaults. It also shows generated values that
needed fixing (an `env = null` that planned a replacement). The tutorial ran with
local execution in HCP Terraform; it does not describe running the flag through a
VCS-driven workspace, so generate configuration in a separate CLI session and
commit the reviewed result.

## Limitations from the tutorial
- Import uses the provider-reported state; it cannot determine health, intent or
  changes outside Terraform's control.
- Import does not detect relationships between infrastructure or which default
  attributes can be skipped; not all providers and resources support import.
- Aim for a first operation that is a no-op; limit destructive changes. Importing
  also modifies state at apply, so consider a backup first.
- Once imported, Terraform manages the whole lifecycle of the resource, including
  destruction.

## Checked
Date: 2026-11-07
Read in full: the Import resources overview, the UI and VCS-driven run workflow page
(summary, automatic and manual runs, confirming plans, speculative plan rules) and
the Import Terraform configuration tutorial (workflow, generation, limitations).
Removed because none of the pages state them: the `Cannot import non-existent remote
object` error, the claim that the legacy command needs local credentials, workspace
credentials needing read access, `for_each` import blocks needing Terraform 1.7,
double-ownership advice, removing the import block in a follow-up commit and the
Verify list. The tutorial's HCP Terraform instructions were read; the bulk import
and import block reference pages were not opened.
Method: documentation only; no commands were run.
