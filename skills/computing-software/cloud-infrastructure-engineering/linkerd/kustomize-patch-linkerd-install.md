---
id: computing-software.cloud-infrastructure-engineering.linkerd.kustomize-patch-linkerd-install
name: kustomize-patch-linkerd-install
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, kustomize, install, customization, priorityclass]
level: advanced
status: docs-checked
description: "Customize the output of linkerd install with Kustomize patches, for example adding a PriorityClass, without forking the install."
sources:
  - https://linkerd.io/2.19/tasks/customize-install/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Instead of forking the install process, patch the rendered manifest with Kustomize. Save the output as the base:

```bash
linkerd install > linkerd.yaml
```

When upgrading, repopulate this file from `linkerd upgrade`. Create `kustomization.yaml` listing the base:

```yaml
resources:
  - linkerd.yaml
```

Example: giving critical control plane pods a PriorityClass, which is not a flag of `linkerd install`. Add a resource file:

```yaml
apiVersion: scheduling.k8s.io/v1
description:
  Used for critical linkerd pods that must run in the cluster, but can be moved
  to another node if necessary.
kind: PriorityClass
metadata:
  name: linkerd-critical
value: 1000000000
```

`1000000000` is the maximum allowed user-defined priority; adjust it as needed. Then write an overlay patch file that sets `priorityClassName: linkerd-critical` on the relevant Deployments, list both in `kustomization.yaml`, and apply the result.

Kustomize accepts any number of patches, transforms and generators in one `kustomization.yaml`, so you can stack customizations. Using a recent kustomize, regeneration from `linkerd upgrade` can be automated with an exec plugin.

## Checked

2026-11-03. Confirmed against: https://linkerd.io/2.19/tasks/customize-install/.

Removed or reworded: The `kubectl apply -k` command, which the page does not show.

Method: documentation only; no commands were run.
