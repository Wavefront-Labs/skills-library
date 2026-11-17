---
id: computing-software.cloud-infrastructure-engineering.crossplane.troubleshoot-debug-pause
name: troubleshoot-debug-pause
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [troubleshooting, logs, debug, finalizer, pause]
level: practitioner
status: docs-checked
description: "Debug Crossplane with describe, events and logs, pause Crossplane or a Provider, and clear stuck finalizers."
sources:
  - https://docs.crossplane.io/latest/guides/troubleshoot-crossplane/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Start with status and events:

```shell
kubectl describe cloudsqlinstance my-db
kubectl get events
```

Most resources set a `Ready` condition. Events for cluster-scoped resources go to the `default` namespace.

Logs:

```shell
kubectl -n crossplane-system logs -lapp=crossplane
kubectl -n crossplane-system logs <name-of-provider-pod>
```

Logs are minimal by default; restart with `--debug`. For a provider, create a `DeploymentRuntimeConfig` whose `package-runtime` container has `args: [--debug]` and reference it from the Provider through `runtimeConfigRef`.

Pause Crossplane by scaling it down:

```shell
kubectl -n crossplane-system scale --replicas=0 deployment/crossplane
```

Scale back to 1 to resume. To pause one Provider, point it at a DeploymentRuntimeConfig with `replicas: 0`.

A resource stuck deleting can be freed by removing its finalizer:

```shell
kubectl patch <resource-type> <resource-name> -p '{"metadata":{"finalizers": []}}' --type=merge
```

This does not delete the external resource; check your cloud console afterwards.

If installing a package with the CLI reports "the server could not find the requested resource", update the Crossplane CLI.

## Checked

Describe, events, log, debug flag, pause, finalizer and CLI-update guidance confirmed on the Troubleshoot Crossplane page.

Method: docs-checked 2026-11-09 against the raw Troubleshoot Crossplane page (docs repo, current content folder), read in full.
