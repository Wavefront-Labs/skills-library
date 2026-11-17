---
id: computing-software.cloud-infrastructure-engineering.terraform.opa-policies-in-hcp-terraform
name: opa-policies-in-hcp-terraform
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, hcp-opa, opa, rego, policy-set, hcp-terraform]
level: practitioner
status: docs-checked
description: "Run OPA Rego policies in HCP Terraform: the query contract, input.plan and input.run, advisory and mandatory enforcement, policy set runtime version and testing with opa test."
sources: ["https://developer.hashicorp.com/terraform/cloud-docs/policy-enforcement/define-policies/opa", "https://developer.hashicorp.com/terraform/cloud-docs/policy-enforcement/manage-policy-sets", "https://developer.hashicorp.com/terraform/cloud-docs/policy-enforcement/manage-policy-sets/configure"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OPA policies in HCP Terraform

## The query contract
A policy is identified by an OPA **query** you write, typically the package name plus rule name, such as `data.terraform.policies.public_ingress.deny`. The query may evaluate code from several Rego files. Its result must be an **array**; an empty array means the policy passed. In the policy UI the OPA-only **Query** field holds this value.

## Input document
HCP Terraform combines run and plan output into one JSON document and passes it to OPA:
- `input.plan`: the Terraform plan data (`format_version`, `planned_values`, `resource_changes`, `output_changes`, `terraform_version`).
- `input.run`: run and workspace data (for example `input.run.workspace.auto_apply`, `input.run.workspace.name`, `input.run.organization.name`, `is_destroy`, `speculative`, `target_addrs`).
Use the "Retrieve JSON Execution Plan" API endpoint to fetch plan output for testing.

## Example policy (from the HashiCorp page)
```rego
package terraform.policies.public_ingress

import input.plan as plan

deny[msg] {
  r := plan.resource_changes[_]
  r.type == "aws_security_group"
  r.change.after.ingress[_].cidr_blocks[_] == "0.0.0.0/0"
  msg := sprintf("%v has 0.0.0.0/0 as allowed ingress", [r.address])
}
```
Query: `data.terraform.policies.public_ingress.deny`.

## Testing
Mock the input in a Rego test and run it with the `opa test` CLI command. The page's example tests a workspace-level rule:
```rego
package terraform.tfc.block_auto_apply_runs

import future.keywords

test_run_workspace_auto_apply if {
    deny with input as {"run": {"workspace": {"auto_apply": true}}}
}
```
(The policy under test denies when `run.workspace.auto_apply != false`.) See the OPA documentation's Policy Testing page for test details; this skill does not cover it.

## Policy sets and enforcement
- A policy set only holds policies of one framework, chosen at creation and not changeable afterwards. OPA policy sets can only run as policy evaluations.
- Enforcement levels for OPA are **advisory** (failures never interrupt the run) and **mandatory** (failures stop the run, but any user with Manage Policy Overrides permission can override and let the run complete).
- OPA policy sets have a **Runtime version** drop-down and an option "This policy set can be overridden in the event of mandatory failures". Pin a specific runtime version for consistent behaviour; the `latest` tag is no longer supported and is pinned to the most recently supported version. To trial a newer runtime, use the policy set's **Evaluate** tab against a workspace.
- If you use OPA 1.4.x or later, the HCP Terraform agent must be 1.28.1 or later.
- A policy set can be connected to a VCS repository. If the repository holds multiple sets, give the relative path to the directory containing the `sentinel.hcl` or `policies.hcl` configuration file; the configuration file holds one or more `policy` blocks. The exact block layout for OPA is on the "OPA VCS Repositories" page, which was not readable here, so check it before writing `policies.hcl`.

## Checked
Date: 2026-11-07. Read in full: "Define Open Policy Agent policies for HCP Terraform" (query, input, examples, test section, run data schema), "Manage policies and policy sets" (framework rules, enforcement levels, policy evaluations) and "Configure connections to policy sets" (OPA runtime version, VCS path, latest tag note, Evaluate tab). The VCS page's OPA tab renders blank when fetched (only headings), so the `policies.hcl` block layout is unconfirmed. Removed: the `policies.hcl` example with `query` and `enforcement_level` arguments, `kind = "opa"` / `tfe_policy_set` argument, the `rego.v1` s3 example (replaced by the page's own example), the `terraform show -json | jq` wrapping, `opa eval`, "failures silently" and "messages shown in the run" claims, and the Verify line. Dropped the openpolicyagent.org source (not an HashiCorp page; not used).
Method: documentation only; no commands were run.
