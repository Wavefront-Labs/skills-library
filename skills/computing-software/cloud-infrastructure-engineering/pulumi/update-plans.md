---
id: computing-software.cloud-infrastructure-engineering.pulumi.update-plans
name: update-plans
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, update-plan, plan-flag, constraint-update, up-plan]
level: practitioner
status: docs-checked
description: "Constrain a Pulumi update to a saved plan with preview --save-plan and up --plan, and know the experimental limits."
sources:
  - https://www.pulumi.com/docs/iac/operations/stack-management/update-plans/
  - https://www.pulumi.com/docs/iac/operations/stack-management/targeted-updates/
  - https://www.pulumi.com/docs/iac/cli/commands/pulumi_preview/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Update plans

```bash
pulumi preview --save-plan=plan.json
pulumi up --plan=plan.json
```
The plan constrains the update to the planned operations. Operations are evaluated in batches, and any discrepancy fails `pulumi up` immediately.

## Limitations
- Unknown outputs are recorded as `unknown` in the plan.
- Resources created inside an `apply` with unknown values are not recorded and error at update time.
- Explicit providers with unknown inputs are limited.
- Workaround: split into separate stacks and connect them with stack references.
- The plan format is experimental and may change.
- Update plans appear in `--help` output only when `PULUMI_EXPERIMENTAL=true` is set.

## Gotchas
- A plan saved from a targeted preview describes only the targeted resources and fails on a full `pulumi up`.
- Regenerate the plan after the program or state changes.

## Verify
`pulumi up --plan=plan.json` completes with only the operations the saved preview showed.

## Checked
2026-11-03. Confirmed against the Pulumi docs source (pulumi/docs, content/docs): the Update plans page (commands, batch evaluation, limitations, workaround, experimental format), the Targeted updates page and the `pulumi preview` reference. Fixed: `PULUMI_EXPERIMENTAL` only controls help visibility. Removed: claims about secrets in plans, destroy and refresh not using plans, provider-surface specifics and "confirm" hedges.
Method: documentation only; no commands were run.
