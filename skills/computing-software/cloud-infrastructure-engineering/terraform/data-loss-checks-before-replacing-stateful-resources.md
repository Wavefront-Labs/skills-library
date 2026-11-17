---
id: computing-software.cloud-infrastructure-engineering.terraform.data-loss-checks-before-replacing-stateful-resources
name: data-loss-checks-before-replacing-stateful-resources
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, replace-data-loss, forces-replacement, stateful-resources, prevent-destroy, backups]
level: practitioner
status: docs-checked
description: "Before approving a replace on databases, volumes, buckets or keys: identify the forcing attribute, snapshot, check final_snapshot and protection flags, or avoid the replace."
sources: ["https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle", "https://raw.githubusercontent.com/hashicorp/terraform-provider-aws/main/website/docs/r/db_instance.html.markdown", "https://raw.githubusercontent.com/hashicorp/terraform-provider-aws/main/website/docs/r/s3_bucket.html.markdown", "https://developer.hashicorp.com/terraform/internals/json-format", "https://developer.hashicorp.com/terraform/language/block/moved"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data-loss checks before replacing stateful resources

## Which resources count
Databases (RDS, Cloud SQL, Azure SQL, Cosmos), disks/volumes (EBS, managed disks,
PDs), buckets with data, file systems (EFS), queues with messages, KMS keys (data
encrypted under them), DNS zones (NS delegation changes), static IPs.

## 1. Why is it replacing?
```bash
terraform show -json tfplan | jq -r '.resource_changes[]
  | select(.change.actions == ["delete","create"] or .change.actions == ["create","delete"])
  | "\(.address) replace_paths=\(.change.replace_paths|tostring)"'
```
In the plan JSON, a replace shows `change.actions` of `["delete","create"]` (or create-then-delete) and `replace_paths` lists the attribute paths that forced it. Which attributes force replacement differs per resource and provider version, so read the plan rather than a remembered list: the provider docs mark such arguments "Forces new resource" (for example `bucket` on `aws_s3_bucket`). Note that `identifier`, `engine`, `storage_encrypted` and `availability_zone` are not marked that way on `aws_db_instance`.

## 2. Can it be avoided?
- Revert the forcing change, or use `ignore_changes` for an attribute changed outside Terraform (it applies when planning updates, not creates).
- Rename via a `moved` block if only the address changed.
- Check the provider docs for an in-place route to the same end.
- Blue/green: create the new resource beside the old, migrate data, then remove the old.

## 3. If replacement is truly needed
- Take and verify a snapshot or backup outside Terraform.
- RDS: `skip_final_snapshot` defaults to `false`, in which case `final_snapshot_identifier` must be provided; `deletion_protection = true` means the database can't be deleted, so disable it deliberately in a separate change.
- Buckets: `force_destroy` defaults to `false`; when `true` all objects are deleted with the bucket and are not recoverable.
- Plan a maintenance window; replacement means new endpoints/IDs; update consumers.

## Guardrails
- `lifecycle { prevent_destroy = true }` on data stores: Terraform rejects plans that would destroy the object, but it does not stop destruction if you remove the resource's configuration, and it blocks `terraform destroy`; HashiCorp says to use it sparingly.
- Provider `deletion_protection` arguments.
- Policy-as-code: deny `delete` actions on tagged stateful types without an approval label.

## Verify
- [ ] Forcing attribute identified and replacement confirmed necessary.
- [ ] Restorable backup taken and tested before apply.

## Checked
2026-11-08. Confirmed against the Terraform lifecycle page (prevent_destroy, ignore_changes), the plan JSON format page (actions, replace_paths), the moved block page, and the AWS provider docs for aws_db_instance and aws_s3_bucket (read from the provider repository because the registry pages are empty stubs). Removed: the remembered list of forcing attributes (contradicted for aws_db_instance), the EBS and Cloud SQL attribute claims, the engine-version in-place claim and the aws rds create-db-snapshot command (not on the cited pages).
Method: documentation only; no commands were run.
