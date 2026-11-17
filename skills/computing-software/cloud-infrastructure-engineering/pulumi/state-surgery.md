---
id: computing-software.cloud-infrastructure-engineering.pulumi.state-surgery
name: state-surgery
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, state-delete, pulumi-state, state-rename, state-move]
level: practitioner
status: docs-checked
description: "Edit Pulumi state safely with pulumi state delete/remove, rename, unprotect, move and repair, with export and import backups."
sources:
  - https://www.pulumi.com/docs/iac/cli/commands/pulumi_state/
  - https://www.pulumi.com/docs/iac/cli/commands/pulumi_state_remove/
  - https://www.pulumi.com/docs/iac/concepts/state-and-backends/editing-state-files/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# State surgery

Back up first:
```bash
pulumi stack export --file backup.json      # restore: pulumi stack import --file backup.json
```
The editing-state docs recommend keeping a second exported copy and preferring targeted `pulumi state` commands over hand-editing the JSON.

```bash
pulumi state delete <urn>                   # alias of: pulumi state remove <urn>
pulumi state delete <urn> --force           # needed when the resource is protected
pulumi state delete <urn> --target-dependents   # also remove its dependents
pulumi state delete --all                   # all resources in the stack
pulumi state rename <urn> <new-name>        # rename a resource in state
pulumi state unprotect <urn>                # or --all
pulumi state move --source orgA/proj/dev --dest orgA/proj/prod <urn>
pulumi state repair                         # fix an invalid state
pulumi state get <urn>                      # show a resource's state
pulumi state taint <urn>                    # mark for replacement
```
`-y` / `--yes` skips confirmation on remove, rename, unprotect, move and repair.

## Gotchas
- `state delete` / `remove` only forgets the resource: the cloud resource stays, and the next `pulumi up` may try to create it again.
- `--force` is for protected resources; `--target-dependents` is for resources that depend on the one removed.
- After `state rename`, update the program's resource name (or add an alias) so the next preview shows no changes.
- To adopt a resource that exists in the cloud, use `pulumi import`.

## Verify
`pulumi preview --diff` should show no unintended creates or deletes after the edit.

## Checked
2026-11-03. Confirmed against the Pulumi docs source (pulumi/docs, content/docs): the `pulumi state` index and its `remove` / `delete`, `rename`, `unprotect`, `move`, `repair`, `get`, `taint` references (flags above) and the Editing state files page (backup advice, targeted commands over hand edits). Removed: the claim that import validates checkpoint invariants, the misattributed `--force` description, and "confirm" markers.
Method: documentation only; no commands were run.
