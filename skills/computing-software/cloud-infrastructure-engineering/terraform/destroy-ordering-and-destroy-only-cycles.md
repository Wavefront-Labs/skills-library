---
id: computing-software.cloud-infrastructure-engineering.terraform.destroy-ordering-and-destroy-only-cycles
name: destroy-ordering-and-destroy-only-cycles
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, destroy-order-reversal, destroy-cycle, cycle-error, create-before-destroy, destroy]
level: practitioner
status: gated
description: "Understand how Terraform reverses dependencies on destroy, why cycles appear only during destroy or replace, and how to break them with create_before_destroy or staged removals."
sources: ["https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle#create_before_destroy", "https://developer.hashicorp.com/terraform/internals/graph", "https://developer.hashicorp.com/terraform/cli/commands/destroy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Destroy ordering and destroy-only cycles

## Ordering rule
Create/update follows dependencies (VPC before subnet). **Destroy reverses them**
(subnet destroyed before VPC; ran with two `terraform_data` objects: vpc created first, subnet destroyed first). For a replace (`-/+`), the default is destroy-then-create;
the old object's destroy happens before the new object's create, and dependents of
the old object must be handled first.

## How destroy-only cycles arise
```
Error: Cycle: aws_lb_target_group.app (destroy deposed ...), aws_lb_listener.https, aws_lb_target_group.app
```
This AWS error text was not reproduced (gated: unconfirmed, source is paywalled or blocked). On `terraform_data` objects, replacing A with B updated in place was planned without a cycle (destroy then create, B updated afterwards).
Typical recipe: resource A is being **replaced**, B depends on A and is **updated in
place**. Terraform needs B updated to point at new-A before old-A can be destroyed,
but with destroy-before-create new-A does not exist yet.

Another: mixing `create_before_destroy = true` on one resource with a dependency that
does not have it. Terraform propagates CBD to the dependencies automatically (ran: the dependency showed `+/- create replacement and then destroy`); an explicit `create_before_destroy = false` on a dependent produced no error or cycle in 1.17.0 on `terraform_data`.

## Fixes
1. **create_before_destroy on the replaced resource** (with `name_prefix` so names do
   not collide). New-A is created, B updated, old-A destroyed:
```hcl
resource "aws_lb_target_group" "app" {
  name_prefix = "app-"
  lifecycle { create_before_destroy = true }
}
```
2. **Stage it**: first apply changes B to not depend on A (or on a temporary resource),
   second apply replaces A.
3. **Removing a whole module**: if destroy order across modules fails (e.g. provider
   config inside the module), remove resources first, apply, then remove the module block (gated: unconfirmed, source is paywalled or blocked).
4. `terraform destroy` cycles usually come from provider configuration depending on
   managed resources (e.g. kubernetes provider using cluster outputs): destroy the
   Kubernetes resources with `-target` first, then the cluster (gated: unconfirmed, source is paywalled or blocked).

## Diagnose
```bash
terraform graph -type=plan-destroy | dot -Tsvg > destroy.svg
```
Edges point from dependent to dependency with a `(destroy)` suffix on nodes. `-draw-cycles` needs an explicit `-type` and, in Terraform 1.17.0 and OpenTofu 1.13.2, produced no red edges on a config with a real cycle (the error goes to stderr), so read the node list in the `Cycle:` error instead.

## Verify
- [ ] Plan succeeds without a cycle error; replace happens in the intended order.
- [ ] `terraform destroy` in a sandbox completes for the same configuration.

## Checked
- Terraform 1.17.0 / Graphviz 16.1.0 with `terraform_data`: destroy order reversed; CBD propagation and explicit `false` dependents; `plan-destroy` graph output; `-draw-cycles` red edges not produced on a two-module cycle.
- Gated: the AWS load-balancer cycle, module-removal and kubernetes-provider destroy recipes (no AWS or Kubernetes available).
