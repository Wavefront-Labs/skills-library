---
id: computing-software.cloud-infrastructure-engineering.terraform.hcp-terraform-run-logs-and-structured-output
name: hcp-terraform-run-logs-and-structured-output
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, run-logs, structured-run-output, hcp-terraform, terraform-cloud, debugging]
level: practitioner
status: docs-checked
description: "Find plan and apply output for HCP Terraform runs in the UI and read it through the plans and applies APIs, including log-read-url, JSON plan output and errored state recovery."
sources: ["https://developer.hashicorp.com/terraform/cloud-docs/run/manage", "https://developer.hashicorp.com/terraform/cloud-docs/api-docs/plans", "https://developer.hashicorp.com/terraform/cloud-docs/api-docs/applies"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HCP Terraform run output and logs

## In the UI
Workspace > Runs tab > click a run. The details page shows the run status, the commit,
how the run started and by whom, a timeline, and the output of `terraform plan` and
`terraform apply`. That output is visible by default while the command is running and
hidden once it has finished, so expand it for finished runs.

Run buttons at the bottom of the page depend on run state: Add Comment, Confirm & Apply,
Override & Continue, Discard Run, Cancel Run, Force Cancel Run (needs workspace admin),
Retry Run (after a plan-only run).

Cancel Run is roughly Ctrl+C on the CLI: Terraform gets an INT signal, updates state for
resources already changed and wraps up. Force cancel is only for a canceled run that
will not end; it kills the process, can lose state or orphan resources, and the button
appears only after Cancel Run has had time to work.

## Plans and applies API
- `GET /plans/:id` and `GET /applies/:id` return the object. There is no list endpoint
  for either; the id is in the `relationships.plan` or `relationships.apply` property
  of the run object.
- `data.attributes.status` is one of `pending`, `managed_queued`/`queued`, `running`,
  `errored`, `canceled`, `finished`, `unreachable`. The last four are final.
- The attributes include `log-read-url` (an archivist.terraform.io URL),
  `status-timestamps`, `resource-additions`, `resource-changes`, `resource-destructions`,
  `resource-imports`, `action-invocations` and `execution-details`. With agent
  execution, `execution-details` also holds `agent-id`, `agent-name`, `agent-pool-id`,
  `agent-pool-name` and `mode: "agent"`.
- Request shape from the page:
```bash
curl \
  --header "Authorization: Bearer $TOKEN" \
  --header "Content-Type: application/vnd.api+json" \
  https://app.terraform.io/api/v2/plans/plan-8F5JFydVYAmtTjET
```
A 404 means plan not found or the user is not authorized.

## JSON plan
`GET /plans/:id/json-output` or `GET /runs/:id/plan/json-output` responds with a
temporary redirect to the JSON execution plan; use `--location` to follow it.
- 204: plan JSON supported but the plan has not finished. 307: URL generated. 422:
  Terraform older than 0.12.
- The temporary URL lives 1 minute; call the endpoint again for a new one.
- Organization tokens cannot call it; use a user or team token with admin access to the
  workspace.

Workspaces using hold your own key (HYOK) encryption have a sanitized plan with sensitive
data omitted: `GET /plans/:id/sanitized-plan` (or `/runs/:id/plan/sanitized-plan`), same
status codes and 1-minute URL; 422 means Terraform older than 1.3.0.

## Recover state after a failed upload
`GET /applies/:id/errored-state` returns 307 with the raw state file URL in the
`Location` header (1-minute expiry, new URL per request). Needs permission to read state;
404 if the apply is unknown, no errored state was uploaded, or not authorized. The agent
fallback that uploads the state requires HCP Terraform agent versions above 1.12.0.

## Checked
Date: 2026-11-07
Read in full: Manage and view runs (cloud-docs/run/manage), Plans API reference and Applies API reference (cloud-docs/api-docs/plans and applies), including every sample request and response.
Confirmed: run details page contents and default output visibility; run buttons and cancel/force cancel behaviour; plan and apply states; no list endpoints and where to find ids; log-read-url attribute; json-output and sanitized-plan status codes, redirect, 1-minute life, token restriction, version limits; errored-state endpoint.
Removed: the "structured run output" toggle and "View raw log" (not on these pages), the curl/jq pipeline that used `GET /runs/:id` (Runs API not read), "pre-signed, no auth header" and "log-read-url expires in about a minute" (the 1-minute life is documented only for json-output, sanitized-plan and errored-state URLs), the `TF_LOG=DEBUG` workspace variable advice, `tfc-agent` logging, policy check and run task gotchas, and the Verify checklist.
Not opened: the Runs API page, and pages on workspace variables and agents.
Method: documentation only; no commands were run.
