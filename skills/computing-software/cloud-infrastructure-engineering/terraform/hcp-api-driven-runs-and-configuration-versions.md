---
id: computing-software.cloud-infrastructure-engineering.terraform.hcp-api-driven-runs-and-configuration-versions
name: hcp-api-driven-runs-and-configuration-versions
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, api-driven-runs, configuration-version, hcp-terraform, tfe-api, ci-cd]
level: practitioner
status: docs-checked
description: "Drive HCP Terraform runs from any CI via the API: create a configuration version, upload a tarball, queue a run, poll status and apply, with the tfci tool as a shortcut."
sources: ["https://developer.hashicorp.com/terraform/cloud-docs/run/api", "https://developer.hashicorp.com/terraform/cloud-docs/api-docs/configuration-versions", "https://github.com/hashicorp/tfc-workflows-tooling"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API-driven runs

For workspaces with the **API-driven** workflow (no VCS connection, no CLI
`cloud` block in CI).

## Steps
```bash
H=(-H "Authorization: Bearer $TFC_TOKEN" -H "Content-Type: application/vnd.api+json")
WS=$(curl -s "${H[@]}" https://app.terraform.io/api/v2/organizations/corp/workspaces/payments-prod | jq -r .data.id)

# 1. configuration version (auto-queue-runs false so we control the run)
CV=$(curl -s "${H[@]}" -X POST https://app.terraform.io/api/v2/workspaces/$WS/configuration-versions \
  -d '{"data":{"type":"configuration-versions","attributes":{"auto-queue-runs":false,"speculative":false}}}')
CV_ID=$(echo "$CV" | jq -r .data.id); UPLOAD=$(echo "$CV" | jq -r '.data.attributes."upload-url"')

# 2. upload tarball of the config directory
tar -czf config.tgz -C infra/payments .
curl -s -X PUT -H "Content-Type: application/octet-stream" --data-binary @config.tgz "$UPLOAD"

# 3. queue run
RUN=$(curl -s "${H[@]}" -X POST https://app.terraform.io/api/v2/runs -d '{"data":{"type":"runs",
 "attributes":{"message":"CI '"$GIT_SHA"'"},
 "relationships":{"workspace":{"data":{"type":"workspaces","id":"'$WS'"}},
 "configuration-version":{"data":{"type":"configuration-versions","id":"'$CV_ID'"}}}}}' | jq -r .data.id)

# 4. poll until planned / policy_checked / errored
curl -s "${H[@]}" https://app.terraform.io/api/v2/runs/$RUN | jq -r .data.attributes.status

# 5. apply (if not auto-apply)
curl -s "${H[@]}" -X POST https://app.terraform.io/api/v2/runs/$RUN/actions/apply -d '{"comment":"approved in CI"}'
```

## Shortcut: tfci / official actions
HashiCorp's HCP Terraform Workflows Tooling (`hashicorp/tfc-workflows-tooling`, a
containerized Go application) and the `hashicorp/tfc-workflows-github` actions wrap these
steps (`upload-configuration`, `create-run`, `apply-run`, `plan-output`); GitLab Pipelines
are also supported.

## Statuses to handle
`pending`, `planning`, `planned`, `cost_estimated`, `policy_checked`, `policy_override`
(a soft-failed Sentinel policy a user can override), `tf_policy_override` and
`tf_policy_checked` (Terraform policy evaluation), `confirmed`, `apply_queued`, `applying`,
`applied`. Final states: `planned_and_finished` (plan-only runs and plans with no changes),
`policy_soft_failed` (plan-only runs), `errored`, `discarded`; also `canceled` and
`force_canceled`.

## Gotchas
- The `upload-url` is returned only when the configuration version is created and is hidden
  afterwards; upload immediately. With `auto-queue-runs` omitted or true, uploading queues a
  run automatically; with false you must create the run yourself.
- The `.tar.gz` must have the configuration directory as its root, with no intermediate
  directories (`./main.tf`, not `./app/main.tf`), and at least one `.tf` file at the root.
- Speculative configuration versions cannot be applied.
- The apply endpoint (`POST /runs/:run_id/actions/apply`, optional `comment`) cannot be called
  with an organization token; use a user or team token. It returns 409 if the run is not
  paused for confirmation.

## Verify
- [ ] Run reaches `applied` or `planned_and_finished`; CI fails on `errored`/`policy_soft_failed`.

## Checked
2026-10-28. Confirmed against the HCP Terraform API-driven run workflow page, the configuration versions API page (`auto-queue-runs`, `speculative`, `upload-url`, PUT with `application/octet-stream`), the runs API page (`POST /runs` attributes and relationships, `message`, run states, apply endpoint, optional `comment`, token restriction) and the tfc-workflows-tooling and tfc-workflows-github READMEs (action names, GitLab support).
Corrected: the `tfci` name (the repository is HCP Terraform Workflows Tooling), the status list (added final states and policy states), and "upload URL is single-use and expires" (the docs say it is only returned at creation).
Removed: the "module paths it references" tarball note (not in the fetched pages).
Method: documentation only; no commands were run.
