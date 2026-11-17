---
id: computing-software.cloud-infrastructure-engineering.terraform.moved-block-limitations-and-cross-type-moves
name: moved-block-limitations-and-cross-type-moves
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, moved-limitations, cross-package-move, cross-type-move, moved-block, removed-block, import-block]
level: advanced
status: verified
description: "Know what moved blocks cannot do: cross-state, data sources, external module packages, most type changes; and the removed+import pattern that replaces them."
sources: ["https://developer.hashicorp.com/terraform/language/modules/develop/refactoring", "https://developer.hashicorp.com/terraform/language/block/moved", "https://developer.hashicorp.com/terraform/plugin/framework/resources/state-move"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Limits of `moved` and what to do instead

| You want to | `moved`? | Do instead |
|---|---|---|
| Rename resource / module call | yes | — |
| Move into/out of local child module | yes | — |
| Move to a different **state** (another root module) | no | `removed {destroy=false}` in source + `import` in target |
| Rename a resource **inside** a child module you call, from the root | yes (a root `moved` with `from = module.m.x.a`, `to = module.m.x.b` planned as a move in a local-module test); a module published by someone else may later ship its own moved blocks, which can conflict | `state mv` is the alternative |
| Change resource **type** (`null_resource` → `terraform_data`) | only if the target resource implements move-state support in its provider | otherwise `removed` + `import` |
| Change a `resource` into a `data` block | no (documented) | recreate |
| Move between workspaces | no | `state mv -state-out` (a legacy local-state option, per `state mv -help`) or removed+import |

## Cross-type moves
```hcl
moved {
  from = null_resource.trigger
  to   = terraform_data.trigger
}
```
Works only when the **target** resource implements move-state support for that source type
(`terraform_data` accepts `null_resource`: the plan printed `null_resource.trigger has moved to
terraform_data.trigger` and applying it changed nothing else). The reverse direction fails at plan
time: `terraform_data.kept` to `null_resource.x` gave `Error: Unable to Move Resource State` ("The target
resource implementation does not include move resource state support"). The docs say to check each
provider's documentation for which resources can change type.

## Where a moved block may point
The refactoring docs say a module's own moved blocks resolve addresses relative to that module instance, and
that moves between modules assume they are distributed together. Tested on 1.17.0 with a local child module:
a root-module moved block can move a root resource into the child (`terraform_data.main` to
`module.m.terraform_data.b`) and can rename inside it (`module.m.terraform_data.a` to `module.m.terraform_data.b`);
both planned as `has moved` with no destroy. If the child module's author later changes its addresses, their
shipped moved blocks and yours may conflict, so prefer letting the module author ship the moves.

## The removed + import pattern (cross-state)
```hcl
# old root
removed {
  from = terraform_data.main
  lifecycle { destroy = false }
}
# new root
import {
  to = terraform_data.main
  id = "42350d25-0d38-10be-f9b6-3fc3dcf15320"   # the object's id from the old state
}
resource "terraform_data" "main" { input = "prod" }
```
Run with `terraform_data` on 1.17.0: the old root planned `will no longer be managed by Terraform, but will not be
destroyed` and applying left 0 resources in state; the new root planned an import (`imported from "..."`).
Apply the import side first if you want zero unmanaged time, then the removed side;
never apply a plan that destroys in between.

## Other limits
- `from`/`to` take only static references: a template such as `null_resource.${var.n}` fails with
  `Invalid expression` ("A single static variable reference is required"). There is no `for_each` on `moved`; one block per mapping.
- Moving a single-instance resource to one instance key (`null_resource.kept` → `null_resource.kept["a"]`) is fine;
  mapping a counted resource as a whole (`two`) to one keyed address (`one["a"]`) did nothing useful: the plan
  created `one["a"]` and destroyed `two[0]` and `two[1]`.
- Two blocks moving different sources to the same `to` fail with `Error: Ambiguous move statements`; a block whose `from`
  is still declared fails with `Moved object still exists`.

## Verify
- [ ] Plan contains no `Unable to Move Resource State`, `Ambiguous move statements` or `Moved object still exists` errors.
- [ ] Cross-state moves: both plans show `0 to destroy`.

## Checked
- Terraform 1.17.0 with null provider, `terraform_data` and a local child module: cross-type `null_resource` to `terraform_data` plans as a move and applies with no change; the reverse errors `Unable to Move Resource State` (the old text `Unsupported cross-type move` is not the message); instance-key moves, `Ambiguous move statements`, `Moved object still exists`, and the template `Invalid expression` all reproduced; the removed-then-import pattern ran across two separate working directories and states (`terraform_data` supports import by id).
- Docs fetched (developer.hashicorp.com/terraform/language/modules/develop/refactoring): providers decide which types can move, and a resource cannot become a data block. The version label "Terraform 1.8+" was not confirmed in the fetched pages and is removed; the claim that a root cannot rename inside a child module was contradicted by the run; `state mv -help` lists `-state-out` as a legacy local-state option.
- Data sources: a moved block naming a data source did not error and changed nothing (so the original row was reworded away).
