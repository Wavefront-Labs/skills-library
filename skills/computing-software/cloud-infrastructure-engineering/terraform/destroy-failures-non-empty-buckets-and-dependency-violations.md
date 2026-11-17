---
id: computing-software.cloud-infrastructure-engineering.terraform.destroy-failures-non-empty-buckets-and-dependency-violations
name: destroy-failures-non-empty-buckets-and-dependency-violations
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, force-destroy, dependency-violation, destroy, troubleshooting, deletion-protection]
level: practitioner
status: docs-checked
description: "Fix destroys that fail: non-empty S3 buckets and force_destroy, VPC DependencyViolation from out-of-band resources, RDS deletion protection and final snapshots."
sources: ["https://raw.githubusercontent.com/hashicorp/terraform-provider-aws/main/website/docs/r/s3_bucket.html.markdown", "https://raw.githubusercontent.com/hashicorp/terraform-provider-aws/main/website/docs/r/db_instance.html.markdown", "https://repost.aws/knowledge-center/troubleshoot-dependency-error-delete-vpc", "https://developer.hashicorp.com/terraform/cli/commands/destroy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Destroy failures

| Symptom | Cause | Fix |
|---|---|---|
| S3 bucket will not delete because it is not empty | objects present | Set `force_destroy = true` on `aws_s3_bucket`, run a successful **apply**, then destroy. The objects, including locked objects, are not recoverable |
| `DependencyViolation` deleting a VPC | subnets, security groups, network ACLs, route tables, internet gateways, NAT gateways, endpoints, peering connections, instances or network interfaces still present, often created outside Terraform | list dependents (script below), delete them, then delete the VPC |
| RDS instance will not delete | `deletion_protection = true` ("the database can't be deleted when this value is set to true") | set `deletion_protection = false`, apply, then destroy |
| RDS destroy needs a final snapshot | `skip_final_snapshot` defaults to `false`, and `final_snapshot_identifier` must then be provided | set `final_snapshot_identifier`, or `skip_final_snapshot = true` (sandboxes only: no snapshot is created) |

## force_destroy needs an apply first
Per the AWS provider docs, `force_destroy` only deletes objects when the bucket is destroyed, and once you set it to `true` there must be a successful `terraform apply` before a destroy so the value is in state; without that apply the flag has no effect. It also does not work if set in the same operation that would replace or destroy the bucket, and an imported bucket needs an apply before it takes effect.

## Finding what blocks a VPC delete
The AWS re:Post article on VPC dependency errors says to delete the VPC's dependent resources first (subnets, security groups, network ACLs, route tables, internet gateways, DHCP options) and gives per-resource `aws ec2 describe-*` commands filtered by VPC ID, for example:
```bash
aws ec2 describe-network-interfaces --filters 'Name=vpc-id,Values=<VPC_ID>'
```
For a network interface that is in use, its Details tab in the EC2 console shows what it is attached to; delete the AWS service that created it.

## Previewing and retrying
`terraform destroy` is an alias for `terraform apply -destroy`; `terraform plan -destroy` shows the proposed destroy without executing it. `-target` destroys one resource and its dependencies. After fixing a blocker, run the destroy again.

## Verify
- [ ] `terraform destroy` completes; `terraform state list` is empty.
- [ ] No leftover network interfaces or load balancers remain in the VPC.

## Checked
2026-11-08. Confirmed against the AWS provider docs for aws_s3_bucket (force_destroy semantics) and aws_db_instance (deletion_protection, skip_final_snapshot, final_snapshot_identifier), the AWS re:Post VPC dependency article, and the terraform destroy page. The registry pages are empty stubs, so the provider repository docs were read. Removed as unconfirmed: the Lambda ENI release time, quoted error strings, Azure ScopeLocked and Key Vault soft-delete rows, the timeouts row, the Kubernetes controller section and the aws s3 rm command.
Method: documentation only; no commands were run.
