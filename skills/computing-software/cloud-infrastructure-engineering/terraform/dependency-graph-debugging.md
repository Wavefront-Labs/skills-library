---
id: computing-software.cloud-infrastructure-engineering.terraform.dependency-graph-debugging
name: dependency-graph-debugging
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, terraform-graph, dependency-graph, dag, cyclic-dependency, depends-on, implicit-dependency, explicit-dependency, target-flag, graphviz, dot-format, apply-ordering, data-source-dependency, for-each-fan-out]
level: advanced
status: gated
description: "Debug Terraform's dependency graph: render it with terraform graph/Graphviz, find why something applies in the wrong order, break cycles, and fix over-broad depends_on fan-out."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/graph", "https://developer.hashicorp.com/terraform/internals/graph", "https://developer.hashicorp.com/terraform/language/meta-arguments/depends_on"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Terraform dependency graph debugging

**Goal:** when something applies in the wrong order, a plan errors with a cycle, or a
seemingly unrelated resource gets flagged for replacement alongside one you're
actually changing, read the actual dependency graph Terraform built instead of
guessing from the HCL — the graph is ground truth; your mental model of the code often
isn't.

## 1. Render it
```bash
terraform graph | dot -Tsvg > graph.svg      # needs graphviz installed
terraform graph -type=plan                   # graph for a specific operation type
```
On anything beyond a toy config the full graph is unreadable noise — filter before
rendering:
```bash
terraform graph | grep -E 'aws_lb|aws_instance|^digraph|^\}|rankdir|node \[' | dot -Tsvg > subset.svg
```
Keep the `digraph` header and the closing brace in the filter: without them `dot` stops with `syntax error in line 1` (ran). Since Terraform 1.17 (docs: "By default the result is a simplified graph") the default output is the resource-only graph with plain node names (`"terraform_data.a"`); `-type=plan` gives the full graph whose nodes read `"[root] terraform_data.a (expand)"`. Or narrow with `-type=plan-destroy` when debugging a destroy-order problem
specifically, since create and destroy orders aren't simply mirror images (destroy
respects reverse create order *unless* `create_before_destroy` changes it for a
specific resource).

## 2. Implicit vs explicit dependencies
Terraform infers edges from **expression references** — `aws_instance.web.id` used in
another resource creates an edge automatically. It cannot infer a dependency that
exists only in the real system (IAM eventual consistency, an API that needs a role to
exist before a policy attaches even though no Terraform expression reads the role's
output). That's what `depends_on` is for:
```hcl
resource "aws_iam_role_policy_attachment" "this" {
  depends_on = [aws_iam_role.this]   # no attribute of the role is actually used
}
```
A resource with no Terraform-visible reason to depend on another, applying before it's
ready, is the single most common cause of "it fails on the first apply but works on
the second" — the second apply has nothing left to create so the ordering issue never
manifests again, which makes it easy to miss in testing.

## 3. Breaking cycles
A cycle ("Error: Cycle: ...") means two resources each reference something that
depends, directly or transitively, on the other. Common causes:
- Two security groups each referencing the other's ID in their own ingress rules —
  fix by using a separate `aws_security_group_rule`/`aws_vpc_security_group_ingress_rule`
  resource for the cross-reference instead of inlining it in each group's `ingress`
  block, which breaks the hard coupling (gated: unconfirmed, source is paywalled or blocked) (no AWS provider here; a two-resource cycle on `terraform_data` printed `Error: Cycle:` followed by the two addresses, one per line).
- An output of a module that is also one of that module's own inputs (via variable
  defaults sourced from another call of the same module) — restructure so data flows
  one direction between the two module calls.
Read the cycle error's resource list in order; it names the actual loop, not just "a"
problem resource.

## 4. Over-broad `for_each`/`count` dependencies
Set and map keys, not positional index, drive per-element identity, so build collections with `toset()` or maps (ran: with `triggers_replace` set per element, inserting `x` in the middle of a three-item list replaced `c[1]` and `c[2]` and created `c[3]` under `count`, but only created `f["x"]` under `for_each`). A `count`-based resource is far more
exposed to this: inserting an element in the middle of a list shifts every subsequent
index and looks like N replacements instead of 1 insert. Switching `count` to
`for_each` keyed by a stable value is usually the fix, not a graph problem to route
around.

## 5. Scoping with `-target`
`terraform apply -target=aws_instance.web` runs only the graph nodes needed to produce
that resource — useful for diagnosis (does *this* resource alone apply cleanly?) but
not a substitute for fixing the ordering; `-target` applies are explicitly called out
by HashiCorp as a break-glass tool, and repeated reliance on it for routine applies
usually means the root module should be split instead (see
`computing-software.cloud-infrastructure-engineering.terraform.workspace-and-environment-strategy`
for root-splitting guidance).

## Gotchas
- `terraform graph` output reflects the **current configuration**, not necessarily
  what a `plan` against current state will actually execute — always cross-check
  against `terraform plan` output for the operation you're actually debugging.
- A `depends_on` pointed at a whole module (`depends_on = [module.network]`) creates a
  dependency on every resource inside that module, not just the one you care about —
  this is sometimes the over-broad fan-out causing unrelated resources to serialize
  behind each other; point at the specific output/resource instead where possible.
- Data source arguments that reference managed resources create implicit edges; when the resource has pending changes the read is deferred (`will be read during apply`), not an error and not a cycle (ran). Adding `depends_on` to the data source only changes when it is read.
- DOT node naming differs by graph type and has changed between Terraform versions (1.17.0 ran: default graph `"terraform_data.a"`, `-type=plan` `"[root] terraform_data.a (expand)"`, `-type=plan-destroy` `(destroy)` suffix); do not parse it by string-matching names without pinning the version.

## Verify
- [ ] Every cross-resource dependency with no Terraform-expression link has an explicit `depends_on` with a comment explaining why.
- [ ] No cycle errors; if one occurs, the fix separates the circular reference into its own resource rather than suppressing the error.
- [ ] `for_each`/`count` collections are keyed by stable values, not positional index, where element identity matters.
- [ ] `-target` applies are not part of the routine apply path — only used for diagnosis or documented break-glass cases.

## Checked
- Terraform 1.17.0 and Graphviz 16.1.0 on Windows with `terraform_data` resources and a local module: default, `-type=plan` and `-type=plan-destroy` output compared; the skill's `grep -E ... | dot` subset command failed with `syntax error in line 1` and the fixed filter rendered; `-type=plan-destroy` showed reversed edges; count-vs-for_each index shift measured; `-target` warns that it is not for routine use; an explicit `depends_on` on a whole resource accepted. Cycle error list read from a real cycle.
- Gated: AWS security-group and load-balancer examples, `terraform destroy`/provider behaviours beyond local providers, and the HashiCorp "break-glass" wording (CLI warning text only).
