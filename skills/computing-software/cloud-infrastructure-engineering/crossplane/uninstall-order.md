---
id: computing-software.cloud-infrastructure-engineering.crossplane.uninstall-order
name: uninstall-order
category: computing-software
field: cloud-infrastructure-engineering
product: crossplane
tags: [uninstall, deletion-order, managed-resources, xrd]
level: practitioner
status: docs-checked
description: "Uninstall Crossplane in the right order so external cloud resources are deleted, not orphaned."
sources:
  - https://docs.crossplane.io/latest/guides/uninstall-crossplane/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Deleting Crossplane out of order can leave cloud resources running that you then must delete by hand.

Order:

1. Remove all composite resource definitions.
2. Remove all remaining managed resources.
3. Remove all providers.

Most Crossplane resources depend on others (a managed resource depends on its provider), so deleting out of order may stop Crossplane deleting the external resources. Deleting the Crossplane pod then removes the remaining components; with Helm use `helm uninstall crossplane --namespace crossplane-system`. Helm leaves the `crossplane-system` namespace (delete with `kubectl delete namespace crossplane-system`) and the `*.crossplane.io` CRDs; deleting a CRD removes all custom resources of that type.

Take inventory first:

```shell
kubectl get managed
```

It can take minutes on a large API server. Keep the output to compare against your cloud afterwards.

Deleting an XRD removes the composite resources it defines and the managed resources they created. List XRDs with `kubectl get xrd`.

Then delete any remaining manually created managed resources with `kubectl delete`; `kubectl get managed` lists what is left. Finally remove providers with `kubectl get providers` and `kubectl delete provider <name>`.

## Checked

2026-11-08: read the whole Crossplane Uninstall page (raw source of docs.crossplane.io/latest/guides/uninstall-crossplane). Confirmed the deletion order (XRDs, managed resources, providers), the dependency rationale, `kubectl get managed` inventory and its slow-on-large-clusters note, XRD deletion removing composite and managed resources, `helm uninstall`, the namespace and `*.crossplane.io` CRDs left behind. Removed unsourced claims about manual finalizer removal, cloud console cleanup, provider deletion protection and rerunning until empty.
Method: documentation only; no commands were run.
