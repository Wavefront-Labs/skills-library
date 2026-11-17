---
id: computing-software.cloud-infrastructure-engineering.istio.istio-canary-control-plane-upgrade
name: istio-canary-control-plane-upgrade
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, canary-upgrade, revisions, istio-rev]
level: practitioner
status: docs-checked
description: "Run a canary istiod revision beside the old one, migrate namespaces by label, then remove the old revision, instead of in-place upgrades."
sources: ["https://istio.io/latest/docs/setup/upgrade/canary/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Istio's canary upgrade (the recommended method) installs the new control plane beside the old one with a different `revision`; each revision is a full control plane with its own Deployment and Service.

```sh
istioctl x precheck
istioctl install --set revision=1-31-3
kubectl get pods -n istio-system -l app=istiod
kubectl label namespace test-ns istio-injection- istio.io/rev=1-31-3
kubectl rollout restart deployment -n test-ns
istioctl proxy-status | grep "\.test-ns "
istioctl uninstall --revision 1-30-1 -y
```

Gotchas from the guide: revision names cannot contain `.`, so use `1-31-3` for 1.31.3. Remove the `istio-injection` label because it takes precedence over `istio.io/rev` for backward compatibility. Installing a revision does not change existing sidecars; pods must be restarted to be re-injected against the new revision. With the default profile gateways are not revision-specific and are upgraded in place. Revision-based upgrades support jumping two minor versions (for example 1.15 to 1.17), unlike in-place upgrades, which must step through every minor release. Uninstalling a revision does not remove cluster-scoped resources shared with other control planes. To roll back, reinstall the previous revision's gateways before `istioctl uninstall --revision=canary -y`.

## Checked

2026-11-03. Confirmed against the Istio Canary Upgrades guide: precheck, revision naming, label procedure, restart, `proxy-status`, `uninstall --revision`, version-skip statement and rollback caveat. Real error fixed: the draft said revision upgrades may skip "a minor version (confirm)"; the guide supports two. Removed: the unsourced soak-and-order advice.
Method: documentation only; no commands were run.
