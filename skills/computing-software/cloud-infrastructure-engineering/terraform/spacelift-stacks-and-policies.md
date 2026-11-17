---
id: computing-software.cloud-infrastructure-engineering.terraform.spacelift-stacks-and-policies
name: spacelift-stacks-and-policies
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, spacelift, spacelift-stacks, spacelift-policies, rego, policy-as-code, stack-dependencies, opentofu]
level: advanced
status: docs-checked
description: "Run Terraform/OpenTofu on Spacelift: stacks managed as code, contexts, stack dependencies, and Rego plan, approval, push and trigger policies attached by label."
sources: ["https://docs.spacelift.io/concepts/policy", "https://docs.spacelift.io/concepts/policy/terraform-plan-policy", "https://docs.spacelift.io/concepts/policy/push-policy", "https://docs.spacelift.io/concepts/stack/stack-dependencies", "https://docs.spacelift.io/concepts/stack/stack-settings", "https://docs.spacelift.io/concepts/configuration/context", "https://raw.githubusercontent.com/spacelift-io/terraform-provider-spacelift/main/docs/resources/stack.md", "https://raw.githubusercontent.com/spacelift-io/terraform-provider-spacelift/main/docs/resources/policy.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spacelift stacks and policies

A Spacelift **stack** points at a repository, a tracked branch and optionally a project root.
**Policies** are Rego rules evaluated at fixed decision points. Both can be managed with the
`spacelift` Terraform provider so the platform config is reviewed like any other Terraform.
Note: the old per-stack `administrative` flag is deprecated and, per the stack settings page,
was replaced on 1 June 2026 by a Space Admin role attachment on each stack's own space; it is
now ineffective, so give the managing stack the role instead of setting the flag.

## 1. Stacks as code
```hcl
resource "spacelift_stack" "network_prod" {
  name                    = "network-prod"
  space_id                = "<SPACE_SLUG>"          # ID (slug) of the space
  repository              = "infra"                 # repo name without the owner part
  branch                  = "main"
  project_root            = "network/prod"
  terraform_workflow_tool = "OPEN_TOFU"             # OPEN_TOFU, TERRAFORM_FOSS (default) or CUSTOM
  terraform_version       = "<VERSION>"
  autodeploy              = false                   # default false
  labels                  = ["prod", "network"]
}
resource "spacelift_aws_integration_attachment" "net" {  # attach an AWS integration to the stack
  integration_id = spacelift_aws_integration.prod.id
  stack_id       = spacelift_stack.network_prod.id
  read  = true
  write = true
}
```
- Name must be unique in the account; `space_id` defaults to `legacy` if it exists, otherwise
  `root`.
- With Autodeploy on, a change to the tracked branch is applied automatically if planning
  succeeds and there are no plan policy warnings, so a single `warn` flags the run for a human.
- A role must exist before the AWS attachment, because role assumption is tested at attach time
  (the provider docs put `depends_on = [aws_iam_role...]` on the attachment).
- A context holds shared environment config. Give a context the label `autoattach:<label>` to
  attach it to every stack or module carrying `<label>`; `autoattach:*` attaches to all
  projects (within its space and child spaces if the context is in a space). AWS and Azure
  integrations attached this way get read-write permissions unless you use `autoattach_read:`
  or `autoattach_write:` labels.

## 2. Stack dependencies
```hcl
resource "spacelift_stack_dependency" "app_on_net" {
  stack_id            = spacelift_stack.app_prod.id
  depends_on_stack_id = spacelift_stack.network_prod.id
}
resource "spacelift_stack_dependency_reference" "vpc" {
  stack_dependency_id = spacelift_stack_dependency.app_on_net.id
  output_name         = "vpc_id"
  input_name          = "TF_VAR_vpc_id"
}
```
- Tracked runs of the dependent stack do not start until the stack it depends on finishes
  successfully, and changes to the dependency trigger the dependent.
- A reference maps an output of the upstream stack to an environment variable on the
  downstream one; for Terraform use the `TF_VAR_` prefix. By default the downstream stack is
  triggered only if the referenced output was created or changed; `trigger_always = true`
  triggers it on every successful upstream run.
- Spacelift only uses outputs of a successful run, so the upstream stack must already have a
  tracked run with an apply phase that produced the output, otherwise the downstream job fails
  with a missing-inputs error. A retry of a failed run does not trigger dependents.
- Sensitive outputs are masked in the UI and logs, and are only transferred across
  dependencies if enabled at both stack and worker-pool level.

## 3. Policies
Policy types in the docs: login, access (replaced by space access control), approval,
initialization and task (both replaced by approval policies), notification, plan, push, trigger
(mostly replaced by stack dependencies) and intent. Login policies are global; every other type
attaches to stacks and can be reused across them. Several policies of one type on a stack are
evaluated separately and combined, so one denial wins.

Plan policies use `deny` (blocks the run) and `warn` (does not fail the plan; helps a human
reviewer). The docs' general rule for plan policies as code review: deny when the run type is
PROPOSED and warn when it is TRACKED. Example (Rego v1 syntax):
```rego
package spacelift

deny contains sprintf("%s: deletes are not allowed in prod", [rc.address]) if {
  some rc in input.terraform.resource_changes
  "delete" in rc.change.actions
  "prod" in input.spacelift.stack.labels
}
warn contains sprintf("%s: instance type %s", [rc.address, rc.change.after.instance_type]) if {
  some rc in input.terraform.resource_changes
  rc.type == "aws_instance"
  not startswith(rc.change.after.instance_type, "t3.")
}
sample := true   # capture inputs for the policy workbench
```
Plan input has `terraform.resource_changes[]` with `address`, `type` and `change.actions`
(create, update, delete or no-op), and `spacelift.stack` with fields such as `labels` and
`branch`.

Push policies decide, per stack, between `track` (tracked, applicable run), `propose`
(proposed run) and `ignore`. They are available to paid accounts only. Example that only runs
for changes under the stack's project root:
```rego
package spacelift

track if { input.push.branch == input.stack.branch; affected }
propose if { not track; affected }
affected if { some f in input.push.affected_files; startswith(f, input.stack.project_root) }
```
The push input carries `push.affected_files` (files for all commits in the push, not only the
head commit) and `stack.project_root`.

Create policies with `spacelift_policy` (`type` one of `ACCESS`, `APPROVAL`, `GIT_PUSH`,
`INITIALIZATION`, `INTENT`, `LOGIN`, `PLAN`, `TASK`, `TRIGGER`, `NOTIFICATION`) and attach
with `spacelift_policy_attachment` (a policy can be attached to a stack once; `LOGIN`
policies cannot be attached). Or label the policy `autoattach:<label>` (any type except login;
`autoattach:*` attaches to everything). `engine_type` is `REGO_V0` by default or `REGO_V1`;
Spacelift supports both and recommends v1 for new policies.

Policies are restricted: `http.send`, `net.lookup_ip_addr`, `opa.runtime`,
`rego.parse_module`, `time.now_ns` and `trace` are disabled, and a policy cannot read external
files. Use `spacelift.request.timestamp_ns` from plan input for the current time.

## 4. Testing
Returning true from the `sample` rule captures the input, the policy body and the result so
you can iterate in the policy workbench (account administrators only). For unit tests, Rego
has built-in testing: mock the input with `with input as {...}` in `test_` rules, for example
`deny with input as {"session": {"member": false}}`. The docs advise creating policies through
the Terraform provider because it allows proper unit testing.

## Gotchas
- Without a push policy, a push to the tracked branch that changes a file in the project root
  triggers a tracked run (default behaviour). Push policy changes replace that logic entirely.
- When a push policy does not track a push, the stack's head commit is not advanced; use the
  stack's sync button to sync it.
- New rules start as `warn`: denying tracked runs unconditionally can make life difficult.

## Verify
- [ ] The managing stack's plan shows stacks, contexts and policies with no manual drift.
- [ ] A test PR that deletes a prod resource is denied by the plan policy.
- [ ] Commits outside a stack's project root do not trigger it.

## Checked
Checked 2026-11-08 against the Spacelift policy, plan policy, push policy, stack dependencies, stack settings and context docs, and the spacelift provider docs for stack, policy, policy attachment, AWS integration attachment and stack dependency (references).
Removed: the `spacectl stack local-preview` command, the `opa test .` CI claim, the "replaces terraform_remote_state" framing, the claim that moving stacks between spaces changes policies and contexts, and the pinned Terraform version number, none of which the pages state. Corrected the "every commit triggers every stack" gotcha (docs: only pushes changing a file in the project root) and the administrative-stack wording.
Method: docs-only read of cited pages, 2026-11-08
