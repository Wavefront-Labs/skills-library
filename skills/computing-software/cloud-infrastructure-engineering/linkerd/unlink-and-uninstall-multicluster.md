---
id: computing-software.cloud-infrastructure-engineering.linkerd.unlink-and-uninstall-multicluster
name: unlink-and-uninstall-multicluster
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, multicluster, unlink, uninstall, link]
level: advanced
status: docs-checked
description: "Unlink a target cluster and uninstall the multicluster extension, including the pre-2.18 unlink command."
sources:
  - https://linkerd.io/2.19/tasks/uninstall-multicluster/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
To unlink a target cluster:

1. Remove the `mirror.linkerd.io/exported=true` label from the mirrored services in the target clusters, so the controllers delete the mirror services in the local cluster.
2. Update the `linkerd-multicluster` chart, removing the matching entry from the `controllers` array in its values. This removes the controllers and their resources.
3. Delete the `Link` custom resource.
4. Delete the kubeconfig secrets `cluster-credentials-<target>` in both the `linkerd` and `linkerd-multicluster` namespaces.

Before version 2.18 the controllers were created with `linkerd multicluster link` and not managed by the extension. In that case unlink with:

```bash
linkerd multicluster unlink --cluster-name=target | kubectl delete -f -
```

Uninstalling removes all components associated with multicluster, including the gateway and service account. You must remove all existing links first; uninstalling while a Link CR remains results in an error. Then run:

```bash
linkerd multicluster uninstall | kubectl delete -f -
```

## Checked

2026-11-08. Confirmed against: https://linkerd.io/2.19/tasks/uninstall-multicluster/. The four unlink steps, the pre-2.18 unlink command, the uninstall command, the requirement to remove links first and the resulting error.

Removed or reworded: The gateway and service mirror wording, and the `kubectl get svc` verification advice (not on the cited page).

Method: documentation only; no commands were run.
