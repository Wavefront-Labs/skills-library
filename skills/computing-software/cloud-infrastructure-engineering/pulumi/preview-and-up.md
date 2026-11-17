---
id: computing-software.cloud-infrastructure-engineering.pulumi.preview-and-up
name: preview-and-up
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, pulumi-preview, pulumi-up, pulumi-destroy, expect-no-changes]
level: practitioner
status: docs-checked
description: "Run pulumi preview and up safely: --diff, --target, --replace, --yes, --expect-no-changes, and reading the plan output."
sources:
  - https://www.pulumi.com/docs/iac/cli/commands/pulumi_up/
  - https://www.pulumi.com/docs/iac/cli/commands/pulumi_preview/
  - https://www.pulumi.com/docs/iac/operations/stack-management/targeted-updates/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Preview and up

```bash
pulumi preview --diff                    # property-level diff, no changes made
pulumi preview --expect-no-changes       # error if the preview proposes any change
pulumi up                                # preview then prompt
pulumi up --yes --skip-preview           # no prompt, no preview; risky
pulumi up --target urn:pulumi:dev::web::aws:s3/bucket:Bucket::site --target-dependents
pulumi up --replace urn:pulumi:...       # force replacement of one resource
pulumi up --refresh                      # refresh state first
pulumi destroy --yes
pulumi preview --json > preview.json
```

Operations: `+` create, `~` update, `-` delete, `+-` replace (create the new resource, then delete the old), `++` create-replacement, `--` delete-replaced.

## Gotchas
- Targeted operations are an escape hatch: the stack can drift from what the program describes, and a targeted resource may see stale input values from state. Use them for one-off interventions and return to whole-stack updates; `--target-dependents` includes dependents.
- A replace on a stateful resource (database, bucket with data) deletes the old one; read the `+-` lines before `--yes`.
- `--exclude` is the denylist counterpart of `--target`.
- `pulumi up --expect-no-changes` checks after the update is applied; `pulumi preview --expect-no-changes` errors if the preview proposes changes.
- `--yes` automatically approves the update after previewing it.

## Verify
Re-run `pulumi preview --expect-no-changes`; it should succeed right after a successful `pulumi up`.

## Checked
2026-11-03. Confirmed against the Pulumi docs source (pulumi/docs, content/docs): the `pulumi up` and `pulumi preview` CLI references (every flag shown above, including `--target`, `--target-dependents`, `--replace`, `--refresh`, `--skip-preview`, `--expect-no-changes`, `--json`, `--yes`), the "How Pulumi works" operation-symbol table and the Targeted updates page (risks). Removed: the `-+` delete-before-replace and `*` read symbols (not in the table), the claim that `--yes` is required in non-TTY CI, and the `[unknown]` preview note; renamed the output file so it is not confused with an update plan.
Method: documentation only; no commands were run.
