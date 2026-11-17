---
id: computing-software.cloud-infrastructure-engineering.terraform.policy-overrides-and-soft-mandatory-workflow
name: policy-overrides-and-soft-mandatory-workflow
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, policy-override, enforcement-levels, sentinel, policy-set, hcp-terraform]
level: practitioner
status: docs-checked
description: "HCP Terraform policy enforcement levels for Sentinel and OPA, how overrides work and who can use them, the policy-set override option, and reading policy outcomes through the API."
sources: ["https://developer.hashicorp.com/terraform/cloud-docs/policy-enforcement/manage-policy-sets#policy-enforcement-levels", "https://developer.hashicorp.com/terraform/cloud-docs/users-teams-organizations/permissions", "https://developer.hashicorp.com/terraform/cloud-docs/api-docs/policy-evaluations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Policy overrides in HCP Terraform

## Enforcement levels
| Engine | Level | On failure |
|---|---|---|
| Sentinel | Advisory | never interrupts the run; failures are shown in the UI |
| Sentinel | Soft mandatory | stops the run; organization admins can allow team members to override |
| Sentinel | Hard mandatory | stops the run; no apply until the cause is fixed, unless the policy set allows overrides |
| OPA | advisory | never interrupts the run |
| OPA | mandatory | stops the run; any user with Manage Policy Overrides permission can override |

The Terraform policy framework lists Advisory, Mandatory overridable (stops the
operation but a user with appropriate permissions can override) and Mandatory.

## Who can override
- For Sentinel soft mandatory failures, organization admins choose whether all team
  members may override or delegate the authority to specified teams.
- For OPA, any user with the Manage Policy Overrides permission.
- For Sentinel policy evaluations, the page says overrides for soft- and
  hard-mandatory policies let any user with Manage Policy Overrides permission
  proceed.
- Permissions are additive across organization, project and workspace scopes and the
  most permissive level wins. Follow least privilege and keep the set of people who
  can override small.

## Policy-set override option
When adding policies to a policy set you can enable "This policy set can be
overridden in the event of mandatory failures". Users with appropriate permissions,
such as admins or team owners, can then override any failed policy in that set, even
policies set to Hard mandatory. This setting takes precedence over the individual
policy's enforcement level, so enable it deliberately.

## Checks versus evaluations
- Only Sentinel policies run as policy checks; checks can use cost estimation data.
- OPA runs only as policy evaluations, and Sentinel policy sets can use evaluations
  by selecting the Agent policy set type. Evaluations cannot access cost estimation
  data, and for Sentinel they enable soft- and hard-mandatory overrides and runtime
  version pinning.
- Choose the engine and level to match the rule: use a level that allows
  overrides for rules with legitimate exceptions and a non-overridable level for
  non-negotiables (judgement, not from the docs).

## Reading outcomes through the API
`GET /task-stages/:task_stage_id/policy-evaluations` lists the evaluations of a task
stage; `GET /policy-evaluations/:policy_evaluation_id/policy-set-outcomes` lists the
policy set outcomes. Each outcome carries `enforcement_level`, `status`, `policy_name`
and an `overridable` flag, plus `result-count` with `advisory-failed`, `errored`,
`mandatory-failed` and `passed`. The outcomes list takes `filter[n][status]`
(`passed`, `failed`, `errored`) and `filter[n][enforcementLevel]` (`advisory`,
`mandatory`); a filter returns every policy-set outcome containing at least one
matching outcome, with all its outcomes, not only the matching ones.

## Gotchas
- Deleting a policy that applies to an active run makes that run's policy evaluation
  stage error.
- Integrations inherit power: anyone who can merge to a connected repository's main
  branch can indirectly queue plans, regardless of explicit permission.

## Checked
Date: 2026-11-07
Read in full: the Manage policies and policy sets page (checks versus evaluations,
enforcement levels, allow policy level overrides, publishing workflows), the
Permissions overview page and the Policy evaluations API reference.
Removed because the pages do not state them: the claim that workspace admins cannot
override, the `policy_override` run status and "Override & Continue" button, the
`POST /runs/<id>/actions/override` endpoint, audit-trail and monthly review advice,
CI pause-and-approve patterns, `tfrun` and `input.run` allow-list examples and the
Verify checklist. The Manage Policy Overrides permission is named on the policy
sets page; the permissions page does not list it.
Method: documentation only; no commands were run.
