---
id: computing-software.cloud-infrastructure-engineering.istio.istio-uninstall-and-rollback
name: istio-uninstall-and-rollback
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, istio-uninstall, istioctl-uninstall, rollback]
level: practitioner
status: docs-checked
description: "Remove one Istio control plane revision, roll back a canary, or purge the whole mesh with istioctl uninstall, with the documented gateway caveat."
sources: ["https://istio.io/latest/docs/setup/install/istioctl/", "https://istio.io/latest/docs/setup/upgrade/canary/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Remove the narrowest thing that fixes your problem.

```sh
istioctl uninstall --revision 1-30-1 -y     # remove one old control plane revision
istioctl uninstall --revision=canary -y     # roll back: remove the canary revision
istioctl uninstall --purge                  # remove all Istio resources
kubectl delete namespace istio-system       # namespace is not removed by default
```

A revision uninstall removes only that revision's resources, not cluster-scoped resources shared with other control planes. `--purge` removes all Istio resources, including cluster-scoped ones that other control planes may share, so do not use it when another revision should survive. If the old control plane has no revision label, uninstall it with its original install options (for example `istioctl uninstall -f manifests/profiles/default.yaml -y`). An alternative to `istioctl uninstall <original options>` is piping `istioctl manifest generate <original options>` into `kubectl delete --ignore-not-found=true -f -`.

Rollback gotcha (canary guide): with the default profile gateways are upgraded in place to the new revision, and `istioctl uninstall --revision=canary` does not revert them. Reinstall the previous revision's gateways first, using the istioctl version that matches the old control plane, and make sure the old gateways are running before the canary uninstall, to avoid downtime. After removing the old revision, `kubectl get pods -n istio-system -l app=istiod` should show only the one you kept.

## Checked

2026-11-03. Confirmed against the Istio istioctl install guide (uninstall, `--purge`, namespace left in place, manifest generate alternative) and the canary upgrade guide (revision uninstall, canary rollback, gateway reinstall). Removed: unsourced advice to strip injection labels before uninstall, the claim about 24-hour workload certificate lifetime ("confirm"), and the CRD and namespace-label verify steps.
Method: documentation only; no commands were run.
