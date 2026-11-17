---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.hcp-terraform-run-tasks
name: hcp-terraform-run-tasks
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, plan-review, run-tasks, hcp-terraform, policy-gate]
level: advanced
status: docs-checked
description: "Configure HCP Terraform run tasks to call external services at pre-plan, post-plan, pre-apply and post-apply stages, and build the receiving service."
sources:
  - https://developer.hashicorp.com/terraform/cloud-docs/workspaces/settings/run-tasks
  - https://developer.hashicorp.com/terraform/cloud-docs/integrations/run-tasks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HCP Terraform run tasks

Run tasks send data about a run to an external service at specific run stages. The service evaluates whether the run passes or fails and responds to HCP Terraform, which uses the response and the enforcement level to decide whether the run proceeds. Uses named in the docs: validate configuration, analyse plans before apply, scan for security vulnerabilities, or other custom actions.

## Requirements
- Workspaces must use Terraform 1.1.9 or later. Downgrading a workspace with existing runs does not error, but run tasks stop triggering.
- Creating a run task needs the Manage Run Tasks permission; attaching one to a workspace needs Manage Workspace Run Tasks on that workspace.
- The Free edition includes one run task integration that can apply to up to ten workspaces.

## Stages
Pre-plan (before the plan is created), post-plan, pre-apply, post-apply.

## Enforcement levels
- **Advisory**: cannot block a run; a failure shows a warning and the run proceeds.
- **Mandatory**: a failure, including a timeout or unexpected remote error, stops the run and it errors.
- With several tasks the run ends according to the most restrictive level: a failed mandatory task fails the run even if an advisory task passes; a failed advisory task with a passing mandatory task lets the run proceed to apply.

## Setup
1. Organization settings, Run tasks, Create run task: name, endpoint URL (required), optional description and HMAC key. Source is Managed by default; Agent source (Premium) lets requests run through self-managed agents with request forwarding enabled, for private or on-premises services.
2. Associate it with a workspace under Settings, Run Tasks (pick the stage, task and enforcement level), or scope it to the organization or projects. Global scope needs the `global-run-task` entitlement.
3. A task still attached to a workspace cannot be deleted; remove it from workspaces first.

## Service contract (custom integrations)
- When you create the task HCP Terraform sends a test POST to the endpoint, which must answer 200 for the task to be created.
- At run time it POSTs a JSON payload including `stage`, `access_token`, `task_result_callback_url`, `plan_json_api_url`, run, workspace and VCS details. Respond `200 OK` or Terraform retries the trigger.
- Call back to `task_result_callback_url` with the `access_token` as the authentication header and a JSON:API body of type `task-results` with `status` (`running`, `passed` or `failed`), `message` and optional `url` and `outcomes`.
- The request errors if no progress update arrives within 10 minutes or the run goes over 60 minutes.
- If you set an HMAC key, HCP Terraform puts a sha512 HMAC of the payload body in the `X-Tfc-Task-Signature` header; verify it.
- Plan JSON parsing matters: make sure your system interprets it correctly.

## Verify
- [ ] A deliberately non-compliant change fails the mandatory task and the run does not proceed to apply.

## Checked
Method: docs-checked 2026-11-09 against the HCP Terraform "Run tasks" and "Set up run task integrations" pages (full text read).
Removed: typical integration table naming Wiz/Prisma/Infracost/AAP, the tfe provider HCL, "run tasks vs Sentinel/OPA" comparison, HCP IP-range note and the post-apply gating claim (not on pages read).
