---
id: computing-software.cloud-infrastructure-engineering.linkerd.uninstall-linkerd-in-order
name: uninstall-linkerd-in-order
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, uninstall, control-plane, extensions]
level: practitioner
status: docs-checked
description: "Remove Linkerd in the correct order: data plane proxies, extensions, then the control plane."
sources:
  - https://linkerd.io/2.19/tasks/uninstall/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Uninstall in three steps, data plane first and control plane last.

1. Data plane. Remove any `linkerd.io/inject` annotations and roll the deployments. When Kubernetes recreates the pods they have no proxy attached.

2. Extensions. Each extension has an `uninstall` subcommand whose output you pipe to `kubectl delete`:

```bash
linkerd viz uninstall | kubectl delete -f -
linkerd multicluster uninstall | kubectl delete -f -
```

3. Control plane, which needs cluster-wide permissions:

```bash
linkerd uninstall | kubectl delete -f -
```

`linkerd uninstall` prints the manifest for every control plane resource, including namespaces, service accounts and CRDs, and `kubectl delete` removes them.

The command also removes partially installed control planes. `kubectl delete` will complain about resources that were never created; those errors can be safely ignored.

## Checked

2026-11-08. Confirmed against: https://linkerd.io/2.19/tasks/uninstall/. The three steps and their order, the extension uninstall commands, the cluster-wide permission note, what `linkerd uninstall` outputs and the partial-install behaviour.

Removed or reworded: The explanation of what breaks if the order is not kept and the unlink advice (not on the cited page).

Method: documentation only; no commands were run.
