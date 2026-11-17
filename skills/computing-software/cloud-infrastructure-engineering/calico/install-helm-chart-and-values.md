---
id: computing-software.cloud-infrastructure-engineering.calico.install-helm-chart-and-values
name: install-helm-chart-and-values
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [install, helm, tigera-operator, values, eks, aks, gke, kubernetesprovider]
level: practitioner
status: docs-checked
description: "Install Calico with Helm 3: add the repo, apply the v3 CRD chart per Kubernetes version, install tigera-operator, and set kubernetesProvider for EKS, GKE, AKS or MKE."
sources:
  - https://docs.tigera.io/calico/latest/getting-started/kubernetes/helm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Prerequisites from the Helm guide: Helm 3, a cluster with no CNI (or a compatible CNI for policy-only mode), a working kubeconfig, and hosts where Calico can manage `cali` and `tunl` interfaces (configure NetworkManager if present).

```bash
helm repo add projectcalico https://docs.tigera.io/calico/charts
kubectl create namespace tigera-operator
```

Install the CRDs from the chart, choosing the API version to match your cluster. For Kubernetes 1.36 or later:

```bash
helm template calico-crds projectcalico/projectcalico.org.v3 --version <release> --api-versions admissionregistration.k8s.io/v1/MutatingAdmissionPolicy | kubectl apply --server-side -f -
```

For 1.34 or 1.35 use `--api-versions admissionregistration.k8s.io/v1beta1/MutatingAdmissionPolicy`. Then install the operator chart with `helm install <name> projectcalico/tigera-operator --version <release> --namespace tigera-operator`, adding `-f values.yaml` if you have one. Confirm with `watch kubectl get pods -n calico-system`.

**When values.yaml is mandatory.** On EKS, GKE, AKS or Mirantis Kubernetes Engine, or if you need custom TLS certificates, you must set `installation.kubernetesProvider`. The page's AKS example for a cluster with no pre-installed CNI:

```yaml
installation:
  kubernetesProvider: AKS
  cni:
    type: Calico
  calicoNetwork:
    bgp: Disabled
    ipPools:
    - cidr: 10.244.0.0/16
      encapsulation: VXLAN
```

For EKS the page shows the one-line form `{ installation: {kubernetesProvider: EKS }}`. After install, install calicoctl (listed as required next step).

## Checked

2026-11-08. The Install using Helm page was read in full. Repo URL, commands, provider note and AKS values were confirmed on the Helm installation page. The release placeholder stands for the version shown in the docs.

Method: documentation only; no commands were run.
