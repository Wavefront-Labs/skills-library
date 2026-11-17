---
id: computing-software.cloud-infrastructure-engineering.terraform.uploading-state-via-hcp-state-versions-api
name: uploading-state-via-hcp-state-versions-api
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, state-version-upload, hcp-terraform, migrate-to-hcp, state-migration, tfe-api]
level: practitioner
status: docs-checked
description: "Upload or migrate state into an HCP Terraform workspace with the state versions API: lock, serial, lineage, md5, base64 and separate upload."
sources: ["https://developer.hashicorp.com/terraform/cloud-docs/api-docs/state-versions#create-a-state-version", "https://developer.hashicorp.com/terraform/cloud-docs/migrate", "https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspaces#lock-a-workspace"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Uploading state via the HCP state versions API

HashiCorp documents three ways to migrate state into HCP Terraform or Terraform Enterprise: the Terraform CLI (add a `cloud` block, run `terraform init`), the API, and the `tf-migrate` tool (a separate download). The CLI route needs Terraform v1.1 or later for the `cloud` block. Use the API when migrating many workspaces by script or from tools other than the CLI.

Stop all Terraform operations on the old state first, and migrate only into workspaces that have never performed a run. Uploading state to a workspace that has already run can leave orphaned or duplicated infrastructure.

## Steps
```bash
TOKEN=...; WS=ws-abc123; F=terraform.tfstate
# 1. Lock the workspace
curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/vnd.api+json" \
  https://app.terraform.io/api/v2/workspaces/$WS/actions/lock -d '{"reason":"state upload"}'

# 2. Build payload
SERIAL=$(jq .serial $F); LINEAGE=$(jq -r .lineage $F)
MD5=$(md5sum $F | cut -d' ' -f1); B64=$(base64 -w0 $F)
jq -n --argjson s $SERIAL --arg l "$LINEAGE" --arg m "$MD5" --arg b "$B64" \
  '{data:{type:"state-versions",attributes:{serial:$s,md5:$m,lineage:$l,state:$b}}}' > payload.json

# 3. Create the state version
curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/vnd.api+json" \
  https://app.terraform.io/api/v2/workspaces/$WS/state-versions -d @payload.json | jq .data.id

# 4. Unlock
curl -s -X POST -H "Authorization: Bearer $TOKEN" \
  https://app.terraform.io/api/v2/workspaces/$WS/actions/unlock
```

## Rules in the API reference
- `POST /workspaces/:workspace_id/state-versions` creates a state version and makes it the current one; the workspace must be locked by the user creating it (locked via API or UI).
- Use a user token or team token; organization tokens cannot call this endpoint.
- Required attributes: `data.type` (`state-versions`), `serial` (must match the serial in the raw state file) and `md5` (MD5 of the raw state).
- Optional: `state` (Base64 raw state file), `lineage` (should match the state file; optional because early Terraform had no lineage), `json-state`, `json-state-outputs` (populates workspace outputs immediately), and a `run` relationship.
- If `state` is omitted, upload the content afterwards with `PUT` to the returned `hosted-state-upload-url`; the workspace cannot be unlocked normally until it is uploaded. HashiCorp strongly recommends uploading content separately rather than in the create request. The upload URL works once and is hidden afterwards.
- Responses: 201 created, 404 workspace not found or unauthorised, 409 conflict, 412 precondition failed, 422 malformed body.
- State version `status` is `pending`, `finalized` or `discarded`; only finalized versions show in the UI, and you cannot unlock until the latest is finalized.
- Resources, modules, providers and outputs are populated asynchronously; wait for `resources-processed` to become true before relying on them.

## Verify
- [ ] The state version status is `finalized` and the workspace States view shows the new version.
- [ ] A speculative plan in the workspace reports no changes.

## Checked
2026-11-08. Read in full: the HCP Terraform migrate page and the state versions API create/upload sections; the lock and unlock endpoints (`POST /workspaces/:workspace_id/actions/lock` with an optional `reason`, and `.../unlock`) in the workspaces API page (read by grep of those sections only). Removed: "serial must be greater than the current serial", "lineage must match the existing state", `terraform state push` equivalence and the tfe-provider statement, none of which the pages document.
Method: documentation only; no commands were run.
