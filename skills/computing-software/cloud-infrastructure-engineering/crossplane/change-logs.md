---
id: computing-software.cloud-infrastructure-engineering.crossplane.change-logs
name: change-logs
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [change-logs, provider, sidecar, deploymentruntimeconfig, audit]
level: advanced
status: docs-checked
description: "Record what a provider changes with change logs, enabled via DeploymentRuntimeConfig and a sidecar."
sources:
  - https://docs.crossplane.io/latest/guides/change-logs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Change logs (alpha) record every create, update and delete a provider makes to managed resources, including silent drift corrections. The provider must support them.

Enable per provider with a `DeploymentRuntimeConfig` that:

1. Adds the `--enable-changelogs` argument to the provider container.
2. Adds the `changelogs-sidecar` container (from the crossplane/changelogs-sidecar project).
3. Declares a shared volume mounted in both containers for passing change events.

Install the provider with `runtimeConfigRef` pointing at it. The provider also needs permission to manage the resources you create.

Read the entries from the sidecar's logs:

```shell
kubectl -n crossplane-system logs -l pkg.crossplane.io/provider=provider-kubernetes -c changelogs-sidecar | jq
```

Each entry is structured JSON with `timestamp`, `provider`, `apiVersion`, `kind`, `name`, `externalName`, `operation` (such as `OPERATION_TYPE_CREATE`) and a `snapshot` of the resource. Filter with jq, for example `jq '.timestamp + " " + .kind + " " + .name + " " + .operation'`.

Updates and deletes produce their own entries.

## Checked

2026-11-08: read the whole Crossplane Change Logs guide (raw source of docs.crossplane.io/latest/guides/change-logs); the YAML manifests it pulls in by shortcode were not read. Confirmed alpha status, the three DeploymentRuntimeConfig requirements (`--enable-changelogs`, changelogs-sidecar container, shared volume), the provider support requirement, the log command, the entry fields and the `OPERATION_TYPE_CREATE`, `OPERATION_TYPE_UPDATE` and `OPERATION_TYPE_DELETE` values.
Method: documentation only; no commands were run.
