---
id: computing-software.devops-ci-cd.flagger.flagger-install-flagger-helm
name: flagger-install-flagger-helm
category: computing-software
field: devops-ci-cd
product: flagger
tags: [install, helm, meshprovider, crd]
level: intro
status: docs-checked
description: "Install Flagger with Helm for Istio or Linkerd, set the metrics server, and understand CRD removal on uninstall."
sources:
  - https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/install/flagger-install-on-kubernetes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Install the CRD first, then the chart:

```bash
helm repo add flagger https://flagger.app
kubectl apply -f https://raw.githubusercontent.com/fluxcd/flagger/main/artifacts/flagger/crd.yaml
helm upgrade -i flagger flagger/flagger \
  --namespace=istio-system \
  --set crd.create=false \
  --set meshProvider=istio \
  --set metricsServer=http://prometheus:9090
```

For Linkerd use namespace `linkerd`, `meshProvider=linkerd` and `metricsServer=http://linkerd-prometheus:9090`. Flagger depends on mesh telemetry and Prometheus; for Istio installed with istioctl use the default profile. It can run in any namespace that reaches Prometheus on port 9090. For Istio multi-cluster shared control plane, install on each remote cluster with `controlplane.kubeconfig.secretName` and `.key` (the secret needs a data key named `kubeconfig`). Add labels with `podLabels.<name>` and `deploymentLabels.<name>`.

Uninstall: `helm delete flagger` does not remove the Canary CRD. Deleting the CRD (`kubectl delete crd canaries.flagger.app`) makes Kubernetes remove all objects Flagger owns, such as Istio virtual services, deployments and ClusterIP services. The Kustomize alternative is `kubectl apply -k https://github.com/fluxcd/flagger/kustomize/kubernetes?ref=main`, which installs Flagger and Prometheus.

## Checked

2026-11-03. Confirmed against the Flagger documentation: https://raw.githubusercontent.com/fluxcd/flagger/main/docs/gitbook/install/flagger-install-on-kubernetes.md.

No wrong claims found; nothing needed removing.

Method: documentation only; no commands were run.
