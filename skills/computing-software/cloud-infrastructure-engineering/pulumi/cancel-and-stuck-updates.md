---
id: computing-software.cloud-infrastructure-engineering.pulumi.cancel-and-stuck-updates
name: cancel-and-stuck-updates
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, pulumi-cancel, update-in-progress, pending-operations, stack-lock]
level: practitioner
status: docs-checked
description: "Handle Pulumi update conflicts and interrupted updates: pulumi cancel, pending operations, clearing pending creates, and DIY lock files."
sources:
  - https://www.pulumi.com/docs/iac/operations/troubleshooting/update-conflicts/
  - https://www.pulumi.com/docs/iac/operations/troubleshooting/interrupted-updates/
  - https://www.pulumi.com/docs/iac/cli/commands/pulumi_cancel/
  - https://www.pulumi.com/docs/iac/concepts/state-and-backends/using-a-diy-backend/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cancel and stuck updates

## Update conflict (Pulumi Cloud)
Pulumi Cloud allows one update per stack at a time using leases. A second update fails with a 409 conflict: "Another update is currently in progress".

```bash
pulumi cancel          # revokes the lease of the current update; -y / --yes skips the prompt
```
Cancelling someone else's running update makes that update fail. The error `[400] Bad Request: the update has already completed` is safe to ignore.

## Interrupted update
An update killed mid-way can leave pending operations in state (`pending_operations`). View resources with `pulumi stack --show-urns`, then:

```bash
pulumi refresh                      # interactive: choose how to clear pending creates
pulumi refresh --clear-pending-creates --yes
pulumi refresh --import-pending-creates "<urn>" --import-pending-creates "<physical id>" --yes
```
`--clear-pending-creates` forgets the pending resource; `--import-pending-creates` adopts the cloud resource into state.

## DIY backends
Locks are files under `.pulumi/locks/` (`locks/<org>/<project>/<stack>/$lock.json`) in the backend; see the DIY backend page.

## Gotchas
- Serialise CI runs per stack so two jobs never update the same stack at once.
- Run `pulumi refresh` after clearing a pending operation, then `pulumi preview`, before the next `pulumi up`.

## Verify
After cancelling or clearing, `pulumi preview` runs without the conflict error.

## Checked
2026-11-03. Confirmed against the Pulumi docs source (pulumi/docs, content/docs): the Update conflicts and Interrupted updates troubleshooting pages, the `pulumi cancel` reference and the DIY backend page (lock file location). Removed: a self-managed backend error string, the manual `aws s3 rm` lock deletion, the jq state-edit recipe and the Deployments tab claim.
Method: documentation only; no commands were run.
