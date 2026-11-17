---
id: computing-software.cloud-infrastructure-engineering.terraform.state-mv-into-modules-and-indexed-instances
name: state-mv-into-modules-and-indexed-instances
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, state-mv, move-into-module, state-mv-for-each, refactoring, dry-run]
level: practitioner
status: verified
description: "Use terraform state mv to move resources into modules and between count/for_each instances with -dry-run, scripting bulk moves, and when to prefer moved blocks."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/state/mv", "https://developer.hashicorp.com/terraform/language/modules/develop/refactoring"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `terraform state mv` into modules and indexed instances

Prefer `moved` blocks (reviewable in a plan, applied by every environment). Use
`state mv` when: the move crosses state files (`-state-out`), you need a one-off
fix in a single workspace, or you are on Terraform < 1.1.

## Moves
```bash
# resource -> module
terraform state mv -dry-run 'aws_instance.web' 'module.app.aws_instance.web'
terraform state mv 'aws_instance.web' 'module.app.aws_instance.web'

# whole module rename
terraform state mv 'module.old' 'module.new'

# count index -> for_each key
terraform state mv 'aws_subnet.private[0]' 'aws_subnet.private["eu-west-1a"]'

# module instance -> keyed module instance
terraform state mv 'module.db' 'module.db["primary"]'
```

## Bulk moves
```bash
terraform state list module.legacy | while read -r a; do
  terraform state mv "$a" "module.platform.${a#module.legacy.}"
done
```
Each `state mv` is a separate command that reads and writes the state and writes a timestamped backup (ran). For hundreds of moves,
generate `moved` blocks instead, or `state pull` > edit with jq > `state push`
(bump `serial`) in a maintenance window.

## Workflow
1. Update the code first (module call exists, resource removed from root).
2. `terraform plan` — it shows destroy+create pairs for each address you must move.
3. Run the moves (`-dry-run` first), then `terraform plan` again: expect **no changes**.
4. Commit the code change together with a note of the moves performed, because
   other workspaces/environments need the same moves.

## Gotchas
- Each environment's state needs the same moves; forgetting one causes a
  destroy/recreate there. This is the main reason `moved` blocks exist.
- Destination must not already exist — `state mv` refuses rather than overwrite (ran: `Invalid target address ... there is already a resource instance at that address`).
- A backup `terraform.tfstate.<timestamp>.backup` is written next to the local state (ran with the local backend: `terraform.tfstate.1792628473.backup`); keep it until the plan is clean.
- Quoting: in Git Bash single quotes around the address worked; in Windows PowerShell 5.1 `'terraform_data.private["a"]'` failed with `Index value required` and `'terraform_data.private[\"a\"]'` worked (ran).

## Verify
- [ ] `-dry-run` lists exactly the expected `Would move` lines.
- [ ] `terraform plan` after the moves reports `No changes`.

## Checked
- Terraform 1.17.0, local backend, `terraform_data`: `state mv -dry-run` printed `Would move "..." to "..."`; resource into a module, count index to `for_each` key, whole-module rename, `module.new` to `module.new["primary"]`, and the bulk `while read` loop with `${a#module.legacy.}` all printed `Successfully moved`; the plan after the moves said `No changes`; moving onto an existing address was refused.
- Not exercised: remote backends.
