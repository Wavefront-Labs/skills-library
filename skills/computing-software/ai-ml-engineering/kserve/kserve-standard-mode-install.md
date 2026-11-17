---
id: computing-software.ai-ml-engineering.kserve.kserve-standard-mode-install
name: kserve-standard-mode-install
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [standard-mode, raw-deployment, gateway-api, kserve-ingress-gateway, gatewayclass, inferenceservice-config, enablegatewayapi, ingressclassname, kserve-controller-deploymentmode]
level: practitioner
status: docs-checked
description: "Install KServe in Standard (raw Kubernetes) mode: Gateway API 1.2.1 or Ingress setup, Helm values, and patching the inferenceservice-config ConfigMap."
sources: ["https://github.com/kserve/website/blob/main/docs/admin-guide/kubernetes-deployment.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Standard (raw Deployment) mode install

Needs Kubernetes 1.32+, cert-manager 1.15.0+ (or a self-signed cert script), and a network controller. Standard mode uses Deployment, Service, Ingress/Gateway API and HPA; KEDA optional for custom metrics. Scale from zero for HTTP is not supported. Recommended for generative inference.

## Gateway API (recommended, v1.2.1)
```bash
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.2.1/standard-install.yaml
```
Create a `GatewayClass` (for example controllerName `gateway.envoyproxy.io/gatewayclass-controller`) and a Gateway `kserve-ingress-gateway` in namespace `kserve` with HTTP 80 / HTTPS 443 listeners, `allowedRoutes.namespaces.from: All`, and label `serving.kserve.io/gateway: kserve-ingress-gateway`. Helm can create it with `kserve.controller.gateway.ingressGateway.createGateway=true`.

```bash
helm install kserve oci://ghcr.io/kserve/charts/kserve-resources --version v0.20.0 \
  --set kserve.controller.deploymentMode=Standard \
  --set kserve.controller.gateway.ingressGateway.enableGatewayApi=true \
  --set kserve.controller.gateway.ingressGateway.kserveGateway=kserve/kserve-ingress-gateway
```
Ingress variant: `--set kserve.controller.gateway.ingressGateway.className=istio` (Istio 1.22+ with an `IngressClass` whose controller is `istio.io/ingress-controller`).

## YAML install
`kubectl apply --server-side -f .../kserve.yaml` (server-side is required, the CRD is large), then `kserve-cluster-resources.yaml`, then patch the `inferenceservice-config` ConfigMap in namespace `kserve`:

```bash
kubectl patch configmap/inferenceservice-config -n kserve --type=strategic \
  -p '{"data": {"deploy": "{\"defaultDeploymentMode\": \"Standard\"}"}}'
kubectl patch configmap/inferenceservice-config -n kserve --type=strategic \
  -p '{"data": {"ingress": "{\"enableGatewayApi\": true, \"kserveIngressGateway\": \"kserve/kserve-ingress-gateway\"}"}}'
```
Ingress option: `{"ingressClassName": "istio"}`. The default mode otherwise stays Knative. Verify with `kubectl get pods -n kserve` and `kubectl get crd | grep serving.kserve.io`.

## Checked
Confirmed against the KServe Kubernetes deployment installation guide: minimum versions, Gateway API 1.2.1 install URL, GatewayClass and Gateway fields, createGateway Helm value, Helm and ConfigMap patch commands, Istio 1.22 minimum, scale-from-zero limitation. Nothing needed removing; the guide's mixed Helm and YAML steps are separate alternatives.

Method: docs-only read of cited pages, 2026-11-08
