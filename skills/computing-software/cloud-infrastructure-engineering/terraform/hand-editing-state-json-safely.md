---
id: computing-software.cloud-infrastructure-engineering.terraform.hand-editing-state-json-safely
name: hand-editing-state-json-safely
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, manual-state-edit, state-push, state-recovery, state-surgery, lineage-mismatch]
level: practitioner
status: gated
description: "Hand-edit Terraform state JSON only when commands cannot: pull, edit with jq, bump serial, keep lineage, validate, push, and verify with a plan, plus what never to edit."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/state/push", "https://developer.hashicorp.com/terraform/cli/state/recover"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hand-editing state JSON

Last resort. First try: `state mv`, `state rm`, `state replace-provider`, `untaint`,
`moved`/`removed`/`import` blocks, provider upgrades.

## Legitimate cases
- A provider bug wrote an invalid attribute value that breaks every plan
  (`Error decoding ... from prior state`).
- Removing a stuck `deposed` object the provider cannot delete.
- Fixing a wrong `index_key` after a failed manual migration.

A deposed object is an extra entry in `instances` carrying a `"deposed": "<key>"` field. Deleting only the `deposed` key (`del(.deposed)`, the earlier version of this skill) leaves two current instances and `state push` fails with `Duplicate resource instance in state` (ran), so drop the whole entry instead. The `aws_lb` and `aws_s3_bucket` examples below use provider resources that were not run (gated: unconfirmed, source is paywalled or blocked).

## Procedure
```bash
# 0. freeze runs, then
terraform state pull > orig.tfstate
cp orig.tfstate edit.tfstate

# 1. edit with jq (repeatable, reviewable), e.g. drop a deposed object:
jq '(.resources[] | select(.type=="aws_lb" and .name=="main") | .instances) |= map(select(.deposed == null))' \
   edit.tfstate > tmp && mv tmp edit.tfstate
# or fix an attribute:
jq '(.resources[] | select(.type=="aws_s3_bucket" and .name=="logs") | .instances[0].attributes.acl) = "private"' \
   edit.tfstate > tmp && mv tmp edit.tfstate

# 2. bump serial, keep lineage
jq '.serial += 1' edit.tfstate > tmp && mv tmp edit.tfstate
diff <(jq -S . orig.tfstate) <(jq -S . edit.tfstate)

# 3. push and verify
terraform state push edit.tfstate
terraform plan
```

## Never edit
- `lineage` (push rejects mismatches: `cannot import state with lineage ... over unrelated state`; changing it hides real mistakes).
- `version` (state format) or `terraform_version` to "trick" an older binary.
- Attributes of `sensitive_attributes`/`private` blobs you do not understand
  (provider-private data is base64 and provider-specific).

## Validation
- `jq empty edit.tfstate` for JSON syntax.
- `terraform state list` against the local file: `terraform state list -state=edit.tfstate`
  (ran: lists the file's resources, including the `(deposed object ...)` entry).

## Rollback
`terraform state push -force orig.tfstate` (ran: a plain push of an older serial fails with `cannot import state with serial 0 over newer state with serial 5`; `-force` accepted it. A different state with the same serial is rejected even with the plain push).

## Verify
- [ ] Diff shows only the intended change and serial +1.
- [ ] Plan after push is clean or shows only the expected reconciliation.

## Checked
- Terraform 1.17.0 on a local `terraform_data` state: pull, jq edit, serial bump and `state push` worked; I synthesised a deposed entry (`terraform plan` then showed `(deposed object abcd1234) will be destroyed`), the old `del(.deposed)` jq produced a state that push rejected with `Duplicate resource instance`, and `map(select(.deposed == null))` removed the entry and pushed cleanly; lineage mismatch and lower serial rejected; `-force` accepted the older state. The `aws_*` jq paths were not run.
- Gated: the `aws_lb` and `aws_s3_bucket` attribute edits and real provider-written deposed objects (terraform_data cannot fail a destroy; the destroy provisioner is skipped under create_before_destroy).
