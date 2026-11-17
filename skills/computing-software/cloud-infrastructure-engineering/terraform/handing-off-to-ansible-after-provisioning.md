---
id: computing-software.cloud-infrastructure-engineering.terraform.handing-off-to-ansible-after-provisioning
name: handing-off-to-ansible-after-provisioning
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, ansible-handoff, ansible, configuration-management, dynamic-inventory, provisioners, cloud-terraform]
level: practitioner
status: docs-checked
description: "Hand off from Terraform to Ansible: tag-based aws_ec2 dynamic inventory, the cloud.terraform collection, and why provisioners are a last resort for post-apply configuration."
sources: ["https://raw.githubusercontent.com/ansible-collections/cloud.terraform/main/README.md", "https://docs.ansible.com/ansible/latest/collections/amazon/aws/aws_ec2_inventory.html", "https://developer.hashicorp.com/terraform/language/resources/provisioners/syntax"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Terraform -> Ansible handoff

## Separation of concerns
Terraform creates infrastructure; Ansible configures hosts. HashiCorp's provisioners page
says Terraform is designed for immutable infrastructure, strongly recommends purpose-built
solutions for post-apply operations, and says to exhaust alternatives before using
provisioners, because Terraform cannot model provisioner behaviour and most provisioners
need direct network access and credentials. A failed creation-time provisioner marks the
resource tainted, so the next apply destroys and recreates it. Running `ansible-playbook`
from a `local-exec` therefore ties a long, retry-prone process to the apply. Prefer a
separate pipeline stage after `terraform apply`.

## Inventory options
**1. Cloud dynamic inventory by tags** (no Terraform coupling). The `amazon.aws.aws_ec2`
inventory plugin takes `regions`, `filters` (for example `tag:Environment`), `hostnames`
(including `private-ip-address`) and `keyed_groups` (with `key` and `prefix`):
```yaml
# inventory/aws_ec2.yml
plugin: amazon.aws.aws_ec2
regions: [eu-west-1]
filters:
  tag:ManagedBy: terraform
  tag:Stack: payments
keyed_groups:
  - key: tags.Role
    prefix: role
hostnames: [private-ip-address]
```
Terraform's job: tag instances consistently (`Role`, `Stack`, `Env`).

**2. cloud.terraform collection** (install with `ansible-galaxy collection install
cloud.terraform`; needs Ansible Core 2.15+). Per its README it includes:
- inventory plugins `cloud.terraform.terraform_provider` (builds an inventory from a
  Terraform state file) and `cloud.terraform.terraform_state` (builds an inventory from
  resources created by cloud providers, with `backend_type` and `backend_config` options);
- the `cloud.terraform.tf_output` lookup (reads state file outputs);
- modules `cloud.terraform.terraform`, `cloud.terraform.terraform_output` and
  `cloud.terraform.plan_stash` (base64 encode or decode a plan file; use `no_log: true`).
The README says the collection is not meant for direct state manipulation, workspace
management, or managing local Terraform installs. For plugin options, read the per-plugin
docs linked from the README before relying on them.

## Pipeline
```bash
terraform apply tfplan
ansible-playbook -i inventory/aws_ec2.yml site.yml
```
Keep apply and configuration as separate stages with separate logs.

## When a provisioner is acceptable
Only when no purpose-built option exists. To run provisioners not tied to a real
resource, the docs use a `terraform_data` resource with `triggers_replace` (for example
`aws_instance.cluster[*].id`) to say when it re-runs. Provisioner failure handling is
controlled with `on_failure = continue`; destroy-time ones need `when = destroy`.

## Verify
- [ ] The inventory lists the intended hosts (`ansible-inventory -i <file> --graph`).
- [ ] Apply and configuration run as separate stages with separate logs.

## Checked
Checked 2026-11-08 against the cloud.terraform README (GitHub), the Ansible aws_ec2 inventory page and HashiCorp's provisioners page.
Replaced the Galaxy source (a script-rendered page) with the README. Removed: the `terraform output | jq` hosts.ini recipe, the `ansible_host` resource example for `terraform_provider`, the `wait_for_connection` advice, `-auto-approve` and `--limit` in the pipeline, and "hides output", none of which the cited pages state.
Method: docs-only read of cited pages, 2026-11-08
