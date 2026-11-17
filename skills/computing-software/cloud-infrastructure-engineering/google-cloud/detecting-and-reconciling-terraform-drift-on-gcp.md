---
id: computing-software.cloud-infrastructure-engineering.google-cloud.detecting-and-reconciling-terraform-drift-on-gcp
name: detecting-and-reconciling-terraform-drift-on-gcp
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, terraform, terraform-drift-detection, refresh-only, scheduled-plan, cloud-build, configuration-drift]
level: practitioner
status: docs-checked
description: "Detect Terraform drift on Google Cloud with scheduled plans and -detailed-exitcode, decide revert vs adopt, and use refresh-only correctly."
sources: ["https://developer.hashicorp.com/terraform/tutorials/state/resource-drift", "https://developer.hashicorp.com/terraform/cli/commands/plan#detailed-exitcode"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Detecting and reconciling Terraform drift on GCP

## Scheduled detection
Run a plan per stack on a schedule (for example Cloud Scheduler triggering a Cloud Build job) and alert on the exit code:
```bash
terraform init -input=false
terraform plan -input=false -detailed-exitcode -out=plan.out; rc=$?
if [ $rc -eq 2 ]; then terraform show -no-color plan.out > drift.txt; fi
exit $rc
```
`-detailed-exitcode` gives granular exit codes: 0 for no changes, 1 for an error, 2 for a plan that contains changes
(drift or un-applied code). Use a read-only service account for detection. `-lock=false` avoids holding a state lock
but is flagged by HashiCorp as dangerous if others may run commands against the same workspace, so prefer normal
locking unless the job must not block applies.

## Triage
1. Find who changed the resource in Cloud Audit Logs for that resource name.
2. Decide:
   - **Revert** (unauthorised console change): a normal `terraform plan` / `apply` attempts to revert the manual change.
   - **Adopt** (legitimate emergency fix): update the code to match reality; the plan then shows no changes.
   - **Expected external mutation** (autoscalers, attributes managed elsewhere): use `lifecycle { ignore_changes = [...] }`
     or stop managing the attribute.
3. `terraform plan -refresh-only` shows what would change in state without touching infrastructure;
   `terraform apply -refresh-only` records the drift in state. HashiCorp prefers it to the `terraform refresh`
   subcommand, which overwrites state without showing the updates. It needs Terraform v0.15.4 or later.

## Prevention
Restrict console write access in production and keep authoritative IAM resources in code so out-of-band edits are visible.

## Verify
- [ ] Nightly job exits 0 on all stacks for a week, or each drift has a ticket with a decision.

## Checked
2026-11-09: confirmed -detailed-exitcode, -lock=false warning, -refresh-only (plan and apply, v0.15.4, safer than
refresh) on the Terraform plan command page and the resource-drift tutorial. Removed unread items: the Cloud Build
YAML and image tag, audit-log filter text, GKE drift sources, and the cloud.google.com operations best-practices source.
Method: documentation only; no commands were run.
