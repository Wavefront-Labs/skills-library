---
id: computing-software.cloud-infrastructure-engineering.istio.istio-cni-plugin
name: istio-cni-plugin
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, istio-cni, cni, istio-init]
level: practitioner
status: docs-checked
description: "Enable the Istio CNI plugin so pods do not need NET_ADMIN init containers, and handle CNI chaining ordering and node readiness."
sources: ["https://istio.io/latest/docs/setup/additional-setup/cni/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Without CNI, each injected pod runs an `istio-init` container needing `NET_ADMIN`/`NET_RAW`, which many pod security policies reject. The CNI node agent configures traffic redirection from the node instead (and is required by ambient).

```yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  components:
    cni:
      namespace: istio-system
      enabled: true
```

Apply with `istioctl install -f istio-cni.yaml -y`, or with Helm install the `istio/cni` chart and install istiod with `--set pilot.cni.enabled=true` so injection omits `istio-init` (with revisioned control planes set `values.pilot.cni.enabled=true` for each revision).

Gotchas: the CNI agent installs a chained plugin layered on top of your primary CNI (for example Calico or the cloud provider CNI); it does not replace it. Between a node becoming schedulable and the agent being ready, a pod may start without redirection and bypass the sidecar. For sidecar mode this is mitigated by an `istio-validation` init container that blocks the pod when redirection is not set up, plus a detect-and-repair mechanism in the CNI DaemonSet (`values.cni.repair.enabled`, with `deletePods`, `labelPods` or `repairPods` choosing the action). The DaemonSet runs with the `system-node-critical` PriorityClass, so its namespace must allow such pods (GKE restricts this by default). Platforms with nonstandard paths may need `values.cni.cniBinDir`, `cniConfDir` or `cniConfFileName`.

Verify: injected pods carry `istio-validation` instead of `istio-init`, and the `istio-cni-node` DaemonSet pods are running on every node.

## Checked

2026-11-03. Confirmed in the Istio CNI node agent guide: the IstioOperator `components.cni` install, Helm `pilot.cni.enabled=true`, chained-plugin behaviour, the `istio-init`/`istio-validation` split and `NET_ADMIN`/`NET_RAW` requirement, the race condition and repair settings, `system-node-critical` and GKE, and the path settings. Removed: `--set components.cni.enabled=true --set values.cni.excludeNamespaces={kube-system}` (the page shows `excludeNamespaces` only as `istio-system` in a values block for upgrades), the silent-stop claim and the fail-open remark.

Method: documentation only; no commands were run.
