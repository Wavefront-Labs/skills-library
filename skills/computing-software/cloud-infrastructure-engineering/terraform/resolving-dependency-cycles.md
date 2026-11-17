---
id: computing-software.cloud-infrastructure-engineering.terraform.resolving-dependency-cycles
name: resolving-dependency-cycles
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, cycle, cycle-error, dependency-cycle, terraform-graph, security-group-rules, self-reference, create-before-destroy, depends-on, graph]
level: advanced
status: verified
description: "Diagnose 'Error: Cycle' with terraform graph -type=plan -draw-cycles, spot classic causes (mutual SG rules, module depends_on, self-references) and break them without -target."
sources: ["https://developer.hashicorp.com/terraform/internals/graph", "https://developer.hashicorp.com/terraform/cli/commands/graph", "https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle#create_before_destroy", "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/vpc_security_group_ingress_rule"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Resolving dependency cycles

**Goal:** when Terraform says `Error: Cycle: aws_security_group.a, aws_security_group.b`,
find the actual edge that closes the loop and restructure the config so the graph is
acyclic — permanently, not by targeting around it.

## 1. Read the error, then the graph
The error lists every node in the cycle, one per line (`Error: Cycle:` then
`terraform_data.db` / `terraform_data.app`); the last -> first edge is implied. Confirm with a
graph type (`-draw-cycles` only works together with `-type=`; plain `terraform graph` prints a
resource-only summary with no cycle colouring):
```bash
terraform graph -type=plan -draw-cycles | dot -Tsvg > graph.svg   # cycle edges in red
terraform graph -type=plan -draw-cycles | grep -v '^$' | head
```
Cycle edges carry `[color = "red", penwidth = "2.0"]` in the DOT text, so without Graphviz
`grep red` finds them. Every edge comes from an expression reference (`x.id` in an argument),
`depends_on`, or a module input/output chain.

## 2. Classic cycles and their fixes
**Mutual security-group references (most common)**
```hcl
# broken: each SG's ingress references the other's id
resource "aws_security_group" "app" {
  ingress {
    security_groups = [aws_security_group.db.id]
  }
}
resource "aws_security_group" "db" {
  ingress {
    security_groups = [aws_security_group.app.id]
  }
}
```
Fix: create the groups with no inline rules and express rules as separate resources
(`aws_vpc_security_group_ingress_rule`, `aws_security_group_rule`, Azure
`azurerm_network_security_rule`, GCP firewall rules). Rules depend on both groups;
groups depend on nothing.

**Resource referencing itself**
`tags = { Name = aws_instance.x.id }` fails with `Error: Self-referential block ... may not
refer to itself` - use `self` only inside provisioners/`postcondition`; otherwise assign a
name from inputs.

**Output feeding a variable of the same module**
`module.a` output → `module.b` input → `module.b` output → `module.a` input. Lift the
shared value to the root (a local or a third module), or split one module.

**`depends_on` on a module (0.13+)**
`module "b" { depends_on = [module.a] }` makes every resource inside `module.b` wait for
everything in `module.a`; if `module.a` consumes an output of `module.b` (or of anything
that waits for it), that is a cycle (the local test printed `module.a (close)`,
`module.a.terraform_data.r`, `module.a.var.in (expand)`, ... `module.b (expand)`). Replace the
`depends_on` with a reference to the specific output you need.

**`create_before_destroy` mixing**
When resource A has `create_before_destroy = true` and B (which A depends on) does not,
Terraform 1.17.0 propagated create-before-destroy to B: replacing both planned `+/-` for A
and B even when B set `create_before_destroy = false`, with no cycle error. If you do meet
a cycle that appears only when replacing, set `create_before_destroy` consistently on the
chain or replace in two applies.

**Data source reading a resource in the same config that depends on the data**
`data.aws_iam_policy_document` referencing `aws_iam_role.x.arn` while the role's
`assume_role_policy` uses that document (the same shape gave `Error: Cycle:` between a
resource and a data source in the local test). Build the ARN string from
`data.aws_caller_identity` + the role name instead.

**IAM role + instance profile + policy referencing instance**
Compute ARNs from known names (`arn:aws:iam::${account}:role/${name}`) instead of
resource attributes to break the loop; the value is deterministic.

## 3. Techniques
- Break the edge with a **known value**: names, ARNs assembled from account/region
  and a name are plan-time constants; IDs are not.
- Split resources: inline blocks (SG rules, route table routes, NACL rules, bucket
  policies) are a common source of cycles; the standalone resources (`aws_security_group_rule`,
  `aws_vpc_security_group_ingress_rule`, `aws_route`, `aws_network_acl_rule`,
  `aws_s3_bucket_policy`, `azurerm_network_security_rule`, `google_compute_firewall`) exist in the
  provider docs. Do not mix inline and standalone for the same parent (the AWS provider docs
  warn that mixing leads to conflicts).
- Two-phase apply as a **last resort**: `terraform apply -target=<leaf>` once, then
  full apply — and then fix the config so the next fresh deploy does not need it.
- `terraform_data` with `triggers_replace` can carry a dependency without a value
  reference when you need ordering but not data.

## Gotchas
- Run `terraform plan -destroy` as well as `terraform plan` after introducing lifecycle
  rules; destroy ordering is a separate graph (`terraform graph -type=plan-destroy`).
- `terraform graph` with no `-type` prints a resource summary, not the plan graph; the types
  are `plan`, `plan-refresh-only`, `plan-destroy` and `apply`, and `-draw-cycles` needs one of
  them.
- Removing a cycle by deleting a reference can create a *missing* dependency; after
  the fix, `terraform apply` from scratch in a sandbox proves ordering is still right.

## Verify
- [ ] `terraform graph -type=plan -draw-cycles | grep -c red` prints 0.
- [ ] `terraform plan` and `terraform plan -destroy` both succeed.
- [ ] A fresh `apply` in an empty workspace succeeds without `-target`.

## Checked
- Terraform 1.17.0 with `terraform_data` standing in for the cloud resources: mutual references printed `Error: Cycle:` with the two nodes; `-type=plan -draw-cycles` marked both edges red while plain `-draw-cycles` and `-type=plan-destroy` showed none; a self-referencing argument gave `Self-referential block`; `module.a` input from `module.b.out` plus `depends_on = [module.a]` on `module.b` gave the module cycle quoted; a resource/data-source pair gave `Error: Cycle:`; `create_before_destroy` on a dependent with the dependency explicitly `false` still planned `+/-` for both with no cycle; breaking the edge with a split local or removing the back reference let `plan` and `plan -destroy` succeed; the `triggers_replace` dependency carried no value flow.
- Provider docs source (no account used): `aws_security_group_rule`, `aws_vpc_security_group_ingress_rule`, `aws_route`, `aws_network_acl_rule`, `aws_s3_bucket_policy`, `aws_iam_role`, `aws_iam_instance_profile`, `aws_iam_policy_document`, `azurerm_network_security_rule` and `google_compute_firewall` all exist; the aws `aws_iam_role` page warns that mixing policy-management methods leads to resource cycling. Graphviz `dot -T<format>` is the documented flag (`dot` itself was not installed here, so the SVG step was replaced by reading the DOT text). Dropped as unconfirmable: destroy-only cycles and the EKS/kubernetes provider-configuration cycle.
