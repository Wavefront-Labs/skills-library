---
id: computing-software.cloud-infrastructure-engineering.terraform.rolling-back-state-versions-in-hcp-terraform
name: rolling-back-state-versions-in-hcp-terraform
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, state-rollback, hcp-terraform, state-recovery, state-version-upload, disaster-recovery]
level: practitioner
status: docs-checked
description: "Roll back a workspace to an earlier state version in HCP Terraform: the UI Advanced toggle, the PATCH rollback API, locking and token rules, and reconciling afterwards."
sources: ["https://developer.hashicorp.com/terraform/cloud-docs/workspaces/state#roll-back-to-a-previous-state-version", "https://developer.hashicorp.com/terraform/cloud-docs/api-docs/state-versions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rolling back state in HCP Terraform

## When
- State was damaged by a bad upload or manual state surgery, or an operation such as a Terraform upgrade did not go as planned (the API page names this last case).
- Not for undoing infrastructure changes: rolling back replaces the workspace state record only. The docs warn that replacing state can result in orphaned or duplicated infrastructure resources, so understand the differences between versions first.

## UI
Rolling back is the one state operation that needs neither the CLI nor language constructs. It requires access to create new state and that you **lock the workspace**.
1. Lock the workspace.
2. Open the States tab, navigate to the known-good state version and click the **Advanced** toggle button to roll back to it.
3. HCP Terraform duplicates that state and makes the copy the workspace's current state version. **The workspace remains locked** after the rollback.
To undo a rollback, roll back to the state version that was previously the latest.

## API
List versions (the workspace is selected by name, not ID):
```bash
curl --header "Authorization: Bearer $TOKEN" \
  --header "Content-Type: application/vnd.api+json" \
  "https://app.terraform.io/api/v2/state-versions?filter%5Bworkspace%5D%5Bname%5D=my-workspace&filter%5Borganization%5D%5Bname%5D=my-organization"
```
`filter[workspace][name]` and `filter[organization][name]` are required; `page[size]` defaults to 20. Each entry in `data` has an `id` (such as `sv-...`) and `attributes` including `serial`, `created-at`, `status` and `hosted-state-download-url`.

Roll back (the workspace must already be locked by the user making the call):
```bash
# payload.json
# {"data": {"type": "state-versions",
#           "relationships": {"rollback-state-version": {"data": {"type": "state-versions", "id": "sv-bWfq4Y1YpRKW4mx7"}}}}}
curl --header "Authorization: Bearer $TOKEN" \
  --header "Content-Type: application/vnd.api+json" \
  --request PATCH --data @payload.json \
  https://app.terraform.io/api/v2/workspaces/ws-6fHMCom98SDXSQUv/state-versions
```
- `PATCH /workspaces/:workspace_id/state-versions` creates a new state version by duplicating the specified one and sets it as current.
- Needs permission to read and write state versions for the workspace. Organization tokens cannot call it; use a user or team token.
- Responses: 201 success, 404 workspace not found or unauthorized, 409 conflict, 422 malformed body.
- The ID values above are the API page's sample IDs.
- The alternative, `POST /workspaces/:workspace_id/state-versions` (create from a state file), also needs a locked workspace, a `serial` that matches the raw state file, and an `md5` of the raw state; upload the content separately to the returned `hosted-state-upload-url`. A pending state version blocks unlocking until it is finalized.

## Afterwards
- The rolled-back state may not match real infrastructure. The docs describe moved blocks, import blocks, the Replace resources option, `terraform import` or `terraform taint` as ways to bring state back in line with infrastructure.
- Unlock the workspace once you are satisfied, then plan and read the result before applying.

## Checked
Date: 2026-11-07. Read in full: the "Manage workspace state" page (state versions, "Update state to match your infrastructure", "Roll back to a previous state version") and, from the State versions API reference, the attributes and status tables, Create, Upload, List and Rollback sections (the Enterprise backing-data sections and the sample JSON response bodies were skimmed, not read in full). Corrections: the UI action is the **Advanced** toggle, not a "Roll back to this state version" button; the workspace stays locked after the rollback; the listing endpoint is `GET /state-versions` with required workspace and organization name filters, not `/workspaces/$WS/state-versions`; the API has a dedicated PATCH rollback endpoint. Removed: the jq pipeline, "Settings > Locking > Lock" menu path, "higher serial" and "bump serial above current" advice, "workspace admin" permission claim, the "deleted outside Terraform" plan text and Verify list, none of which the pages state.
Method: documentation only; no commands were run.
