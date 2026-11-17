---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.tagging-and-naming-standards
name: tagging-and-naming-standards
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, iac, tagging, naming-conventions, resource-tagging, tag-policy, default-tags, provider-default-tags, aws-tag-policies, azure-policy-tags, gcp-labels, cost-allocation-tags, mandatory-tags, tag-enforcement, scp, opa-tags, naming-standard, resource-naming, label-schema, ownership, cloud-custodian, finops]
level: practitioner
status: draft
description: "Define and enforce tagging and naming standards in IaC: mandatory keys, provider default_tags, naming patterns per resource type, enforcement via tag policies/SCPs/OPA, tag-driven cost reports."
sources: ["AWS Whitepaper - Tagging Best Practices and AWS Organizations Tag Policies", "Microsoft Cloud Adoption Framework - Naming and tagging strategy (https://learn.microsoft.com/azure/cloud-adoption-framework/ready/azure-best-practices/naming-and-tagging)", "Google Cloud - Best practices for labels", "Terraform AWS provider documentation - default_tags"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tagging and naming standards

**Goal:** every resource answers "who owns this, what is it for, which environment,
who pays, how sensitive" from its tags, names are predictable enough to grep, and a
resource without the mandatory tags cannot be created.

## 1. The minimum tag set
| Key | Values | Why |
|---|---|---|
| `owner` | team email/slack handle | who to page |
| `env` | `dev` / `stage` / `prod` | guard rails, inventories, promotion |
| `app` (or `service`) | short name | grouping, dashboards |
| `cost_centre` | finance code | chargeback |
| `managed_by` | `terraform` / `ansible` / `manual` | drift and ownership (see tool-selection skill) |
| `data_class` | `public` / `internal` / `confidential` / `restricted` | security scanning, backup policy |
| `repo` | git URL/path of the defining code | find the code from the console |
Optional: `tier`, `role` (used by Ansible inventory `keyed_groups`), `backup`, `schedule` (auto-stop), `expires` (sandbox cleanup).
Write the standard down with: key casing (lowercase snake_case), allowed values, which are mandatory per resource category, and what tags **must not** contain (secrets, PII, emails of people rather than teams). Cloud limits: AWS 50 tags, key ≤128 / value ≤256 chars; Azure 50 tags, value ≤256; GCP labels lowercase, ≤63 chars, 64 labels.

## 2. Apply from the IaC root, not per resource
```hcl
# Terraform AWS
provider "aws" {
  default_tags { tags = { owner = var.owner, env = var.env, app = var.app, cost_centre = var.cost_centre, managed_by = "terraform", repo = var.repo } }
}
# per-resource extras merge automatically; Auto Scaling groups and some resources need explicit tag blocks / propagate_at_launch
```
Azure: `tags = merge(local.common_tags, {...})` or policy inheritance from resource group (Azure Policy "inherit tag from RG" modify effect). GCP: `labels = local.common_labels` (labels, not tags; "tags" in GCP are a separate IAM-bound concept).
Pulumi: a stack transformation that injects tags into every taggable resource (`pulumi.runtime.registerStackTransformation`) — or the `pulumi-aws` provider `defaultTags`.
Ansible: `amazon.aws` modules take `tags:` + `purge_tags`; `module_defaults: group/aws: tags: ...` sets them once; `resource_tags` in inventory plugins become `tags.*` for `keyed_groups`.
Kubernetes: labels `app.kubernetes.io/name|instance|version|component|part-of|managed-by` (the recommended label schema) plus your `env`/`owner`.

## 3. Naming
Pattern per resource type, e.g. `<org>-<app>-<env>-<region>-<type>[-<n>]`: `acme-billing-prod-euw1-rds`,
`acme-billing-prod-euw1-sg-web`. Rules: lowercase, hyphens, no env-specific names inside shared
modules (take `name_prefix` as a variable), respect per-service limits (S3 buckets globally unique,
63 chars, no uppercase; IAM roles 64; ALB 32; Azure storage accounts 3-24 alnum no hyphens), and
avoid names that encode things that change (IP, owner's name). Let Terraform's `name_prefix` +
`create_before_destroy` handle resources that cannot be renamed in place.

## 4. Enforce
- **Pre-apply (CI)**: OPA/Conftest or Checkov custom policy on the plan JSON: deny any taggable resource missing a mandatory key or with an invalid `env`. Fast feedback, blocks the PR.
- **Cloud-side**: AWS Organizations **tag policies** (allowed keys/values, enforced for selected resource types) + SCP `aws:RequestTag`/`aws:TagKeys` conditions to deny `RunInstances` without `env`; Azure Policy `Require a tag and its value on resources` (deny) and `Inherit tag` (modify); GCP Organization Policy has no label enforcement — use IaC-side checks plus a periodic report.
- **Detect and clean**: Cloud Custodian / AWS Config rule `required-tags` / Azure Policy compliance; untagged sandbox resources get a `expires` tag and are deleted after notice.

## 5. Use the tags
- Cost: activate the keys as cost-allocation tags (AWS Billing → Cost allocation tags; takes ~24 h; untagged shows as "no tag"); Azure Cost Management groups by tag; GCP billing export has labels.
- Inventory: Ansible `aws_ec2` `keyed_groups: [{key: tags.role, prefix: role}, {key: tags.env, prefix: env}]`; Resource Explorer / Resource Graph queries by tag.
- Operations: auto-stop (`schedule` tag + Instance Scheduler), backup plans by `backup` tag (AWS Backup tag-based selection), scanning scope by `data_class`.

## Gotchas
- `default_tags` and explicit resource `tags` with the same key conflict in older provider versions (perpetual diff); keep keys disjoint or upgrade provider ≥ 5.x.
- Tags on ASGs do not propagate to volumes; EBS volumes created by instances need `volume_tags` or launch template `tag_specifications`.
- Tag policies only validate tags on *create/update* of supported resource types; existing non-compliant resources show in the compliance report but are not fixed.
- Case sensitivity: AWS tag keys are case-sensitive (`Env` ≠ `env`); Azure tag names are case-insensitive but values are not. Normalise in the standard and lint.
- Cost allocation tags are per payer account and must be re-activated when new keys appear.
- Renaming a resource in most clouds is a replace; naming mistakes in stateful resources (RDS, buckets) are permanent — review names in plan output before the first apply.

## Verify
- [ ] A PR adding an untagged `aws_instance` fails the plan policy check with a message naming the missing key.
- [ ] Creating a resource via the console without `env` is denied by the SCP/Azure Policy (test in a sandbox account).
- [ ] The cost report groups 95%+ of spend by `app` and `cost_centre`; the untagged bucket shrinks month over month.
- [ ] `ansible-inventory --graph` shows `role_*` and `env_*` groups built purely from tags.
