---
id: computing-software.cloud-infrastructure-engineering.terraform.module-output-cycles-and-finding-cycles-in-graph-output
name: module-output-cycles-and-finding-cycles-in-graph-output
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, module-cycle, graph-cycle-detection, cycle-error, terraform-graph, draw-cycles, dependency-graph]
level: advanced
status: gated
description: "Diagnose 'Error: Cycle' involving module outputs: read the cycle list, render it with terraform graph -draw-cycles, and break module-to-module loops."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/graph", "https://developer.hashicorp.com/terraform/language/modules/develop/composition", "https://developer.hashicorp.com/terraform/internals/graph"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Module output cycles and finding cycles in the graph

## Reading the error
```
Error: Cycle: module.app.aws_security_group_rule.from_db, module.app.output.sg_id (expand),
  module.db.var.app_sg_id (expand), module.db.aws_security_group.db, module.db.output.sg_id (expand),
  module.app.var.db_sg_id (expand)
```
(That is the OpenTofu 1.13.2 single-line style; Terraform 1.17.0 prints `Error: Cycle:` followed by one address per line, for example `module.db.terraform_data.sg`, `module.db.var.app_sg_id (expand)`, `module.app.output.sg_id (expand)`, ...; the security-group names are illustrative (gated: unconfirmed, source is paywalled or blocked), the cycle itself reproduced with two local modules over `terraform_data`.)
Read it as a loop: app needs db's SG, db needs app's SG. Terraform evaluates per
object (not per module), so cross-module references are fine **unless** the
object-level chain loops.

## Typical module cycles and fixes
| Loop | Fix |
|---|---|
| Two modules' SG rules reference each other's SG | Create both SGs first (or in a shared module), create rules in the root or a third module that takes both IDs |
| Module A output depends on resource that consumes module B, B consumes A's output | Split the output: expose the early value (ID) separately from the late value |
| `depends_on = [module.x]` on a module that x itself references | Remove the module-level depends_on; use specific references |
| IAM role in module A references policy in B that references role ARN from A | Build ARNs from known names (`arn:aws:iam::${account}:role/${name}`) instead of resource attributes (gated: unconfirmed, source is paywalled or blocked) |

## Rendering the cycle
```bash
terraform graph -type=plan -draw-cycles | dot -Tsvg > graph.svg   # needs -type; see the note below
terraform graph -type=plan -draw-cycles > g.dot
# big graphs: filter around a node
grep -E 'module.db|module.app' g.dot > g-small.dot   # crude; keep the digraph header/footer
```
Ran on Terraform 1.17.0 and OpenTofu 1.13.2 with a real two-module cycle: the `Cycle:` error went to stderr, the DOT output contained no `red` edge, and `-draw-cycles` without `-type` is documented as unsupported ("supported only when selecting one of the real graph operation types"). The red-edge rendering did not reproduce, so use the node list in the error.

In current Terraform versions `terraform graph` defaults to a simplified resource-only
graph; use `-type=plan` (or `plan-destroy`) to see the full graph including `var`,
`output` and `(expand)` nodes that participate in cycles.

## Destroy-time cycles
If the cycle only appears in `plan -destroy` or with `create_before_destroy`, render
`-type=plan-destroy` and see the create-before-destroy skill.

## Verify
- [ ] `terraform validate` and `terraform plan` succeed with no `Cycle:` error.
- [ ] `terraform validate` reports no `Cycle:` error (the `-draw-cycles` red edges did not reproduce, so do not rely on them).

## Checked
- Terraform 1.17.0 / OpenTofu 1.13.2 with two local modules and a looped output/variable chain: error text for both tools; a non-circular cross-module reference (app rule uses db output, db SG uses app SG) planned fine, confirming per-object evaluation; `-draw-cycles` red edges absent; default vs `-type=plan` graph vocabulary checked (`var`, `output`, `(expand)`, `(close)` nodes). Docs: graph command page (hashicorp/web-unified-docs v1.17.x).
- Gated: AWS security-group and IAM rows.
