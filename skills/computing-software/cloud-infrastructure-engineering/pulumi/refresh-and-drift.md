---
id: computing-software.cloud-infrastructure-engineering.pulumi.refresh-and-drift
name: refresh-and-drift
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, pulumi-refresh, drift, refresh-state, run-program]
level: practitioner
status: docs-checked
description: "Detect and resolve Pulumi drift with pulumi refresh --preview-only, --expect-no-changes, up --refresh, and clearing pending creates."
sources:
  - https://www.pulumi.com/docs/iac/concepts/state-and-backends/
  - https://www.pulumi.com/docs/iac/cli/commands/pulumi_refresh/
  - https://www.pulumi.com/docs/iac/operations/troubleshooting/interrupted-updates/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Refresh and drift

Drift is a difference between Pulumi state and the real cloud resources.

```bash
pulumi refresh --preview-only                       # detect drift; state is not changed
pulumi refresh --preview-only --expect-no-changes   # CI check: fails if drift exists
pulumi refresh --diff                               # show property-level changes
pulumi refresh --yes                                # apply the refreshed values to state
pulumi refresh --target <urn>                       # one resource (or --exclude <urn>)
pulumi preview --refresh                            # preview after refreshing
pulumi up --refresh                                 # refresh, then update
pulumi refresh --run-program                        # also run the program during refresh
```
`--run-program` exists on refresh, up and preview; on up and preview it applies only together with `--refresh`.

In the preview, `~` marks a property that drifted and `-` marks a resource the provider says no longer exists.

## Two ways to resolve
- Remediate (cloud should match the program): `pulumi up --refresh`.
- Adopt (the cloud change is right): `pulumi refresh`, then edit the program to match; `pulumi preview` should then show no changes.
- Properties the cloud legitimately owns can be excluded with the `ignoreChanges` option.

## Pending creates
After an interrupted update, `pulumi refresh` (interactive) lets you clear pending creates. Non-interactive: `pulumi refresh --clear-pending-creates --yes`, or `--import-pending-creates "<urn>" --import-pending-creates "<physical id>" --yes`.

## Verify
`pulumi refresh --preview-only --expect-no-changes` succeeds when state matches the cloud.

## Checked
2026-11-03. Confirmed against the Pulumi docs source (pulumi/docs, content/docs): the drift section of State and backends (preview-only, expect-no-changes, remediate vs adopt, symbols), the `pulumi refresh` reference (all flags above) and the Interrupted updates page (pending creates). Removed: the expired-credentials explanation, "confirm flags" hedges and unsourced notes.
Method: documentation only; no commands were run.
