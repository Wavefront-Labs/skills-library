---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-helmchart-crd
name: k3s-helmchart-crd
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, helm-controller, helmchart, helm-cattle-io]
level: practitioner
status: docs-checked
description: "Install and manage Helm charts declaratively with the K3s Helm Controller and the HelmChart custom resource."
sources:
  - https://docs.k3s.io/add-ons/helm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: deploy a Helm chart by dropping one manifest on a server.

K3s needs no special Helm configuration beyond a correct kubeconfig path. Its Helm Controller installs, upgrades, reconfigures and uninstalls charts from a HelmChart CRD (apiVersion helm.cattle.io/v1); combined with auto-deploying manifests, one file does it.

Key fields (Helm equivalents): metadata.name (NAME); spec.chart (chart name, or an HTTPS URL to a .tgz); spec.chartContent (base64 .tgz, overrides chart); spec.targetNamespace (--namespace, default default); spec.createNamespace (default false); spec.version; spec.repo; spec.repoCA and spec.repoCAConfigMap; spec.plainHTTP (default false); spec.insecureSkipTLSVerify (default false); spec.timeout (default 300s); spec.backOffLimit (default 1000); spec.failurePolicy (default reinstall, or abort); spec.authSecret (kubernetes.io/basic-auth); spec.dockerRegistrySecret; spec.jobImage; spec.bootstrap; spec.set; spec.valuesContent; spec.valuesSecrets. Only helmVersion v3 is supported.

Example: place in /var/lib/rancher/k3s/server/manifests

```
apiVersion: helm.cattle.io/v1
kind: HelmChart
metadata:
  name: apache
  namespace: kube-system
spec:
  repo: https://charts.bitnami.com/bitnami
  chart: apache
  targetNamespace: web
  valuesContent: |-
    service:
      type: ClusterIP
```

The HelmChart lives in kube-system while its resources deploy to the target namespace (create it in the same manifest if needed).

Chart tarballs placed in /var/lib/rancher/k3s/server/static/ are reachable anonymously inside the cluster; use %{KUBERNETES_API}% in spec.chart (packaged Traefik does this).

## Checked

2026-11-03: read docs.k3s.io add-ons/helm. Confirmed: the HelmChart apiVersion and field list with defaults, the example manifest and the static chart directory.

Method: documentation only; no commands were run.
