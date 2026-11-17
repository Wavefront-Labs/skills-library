---
id: computing-software.cloud-infrastructure-engineering.calico.install-operator-manifests-and-tigerastatus
name: install-operator-manifests-and-tigerastatus
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [install, tigera-operator, manifests, tigerastatus, kind, crds, custom-resources]
level: intro
status: docs-checked
description: "Install Calico on a kind cluster with the Tigera Operator manifests: create CRDs, the operator, then custom-resources.yaml, and watch tigerastatus until all are Available."
sources:
  - https://docs.tigera.io/calico/latest/getting-started/kubernetes/quickstart
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The quickstart uses `kind` with the default CNI disabled and the pod subnet set to the range Calico will use:

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
  - role: worker
  - role: worker
networking:
  disableDefaultCNI: true
  podSubnet: 192.168.0.0/16
```

Nodes stay `NotReady` until a CNI is installed; do not wait for them. Then install in this order, using the manifests location for your Calico release:

1. CRDs: `manifests/v3_projectcalico_org.yaml` for Kubernetes 1.36 or later, or `manifests/v3_projectcalico_org-v1beta1.yaml` for Kubernetes 1.34 or 1.35. Use `kubectl create -f`.
2. The operator: `kubectl create -f` on `manifests/tigera-operator.yaml`. This creates the `tigera-operator` namespace, service account, cluster roles and deployment.
3. The custom resources: `kubectl create -f` on `manifests/custom-resources.yaml`, which creates `Installation`, `APIServer`, `Goldmane` and `Whisker` resources named `default`.

Verify with `watch kubectl get tigerastatus`. After a few minutes `apiserver`, `calico`, `goldmane`, `ippools` and `whisker` all show `True` under `AVAILABLE`. Whisker is not reachable from outside by default; the guide uses `kubectl port-forward -n calico-system service/whisker 8443:8443` and opens `https://localhost:8443` (self-signed certificate).

Calico components run in the `calico-system` namespace for operator installs.

## Checked

2026-11-08. The Calico quickstart guide was read in full. The kind config, install order, CRD file choice by Kubernetes version, created resources, tigerastatus names and port-forward command were confirmed on the Calico quickstart guide.

Method: documentation only; no commands were run.
