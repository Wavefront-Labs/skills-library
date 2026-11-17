---
id: computing-software.ai-ml-engineering.kserve.kserve-kourier-networking
name: kserve-kourier-networking
category: computing-software
field: ai-ml-engineering
product: kserve
tags: [kourier, disableistiovirtualhost, config-network, ingress-class, alternative-networking, net-kourier, kourier-gateway]
level: practitioner
status: docs-checked
description: "Run KServe on Knative with Kourier instead of Istio: install net-kourier, patch config-network, set disableIstioVirtualHost, and test through kourier-gateway."
sources: ["https://github.com/kserve/website/blob/main/docs/admin-guide/serverless/kourier-networking/index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# KServe with Kourier networking

KServe normally creates a top-level Istio VirtualService. To use another Knative networking layer such as Kourier, disable it. Kourier is lighter and simpler than Istio but lacks Istio's advanced traffic management.

```bash
# 1. install Kourier (instead of Istio, step 2 of the Knative install)
kubectl apply -f https://github.com/knative/net-kourier/releases/download/${KNATIVE_VERSION}/kourier.yaml
# 2. point Knative at it
kubectl patch configmap/config-network --namespace knative-serving --type merge \
  --patch '{"data":{"ingress-class":"kourier.ingress.networking.knative.dev"}}'
# 3. turn off the Istio virtual host in KServe
kubectl patch configmap/inferenceservice-config -n kserve --type=strategic \
  -p '{"data": {"ingress": "{ \"disableIstioVirtualHost\": true}"}}'
# 4. restart the controller
kubectl rollout restart deployment kserve-controller-manager -n kserve
```

Verify pods in `knative-serving` and `kourier-system` (the gateway pod is `3scale-kourier-gateway`).

## Testing
Use `kourier-gateway` wherever the first-isvc guide says `istio-ingressgateway`. For port-forwarding:

```bash
kubectl port-forward --namespace kourier-system \
  $(kubectl get pod -n kourier-system -l "app=3scale-kourier-gateway" --output=jsonpath="{.items[0].metadata.name}") 8080:8080
```
Then call `/v1/models/NAME:predict` on localhost:8080 with a `Host` header taken from `kubectl get inferenceservice NAME -o jsonpath='{.status.url}'` (hostname part only). The doc example serves a PMML iris model (`storageUri: gs://kfserving-examples/models/pmml`).

## Checked
Confirmed against KServe's alternative networking layer (Kourier) page: net-kourier install, `config-network` ingress-class patch, `disableIstioVirtualHost` in `inferenceservice-config`, controller restart, `kourier-gateway` port-forward test, PMML example, and the stated Kourier trade-offs (simpler, lighter, fewer advanced traffic-management features).
Method: docs-only read of cited pages, 2026-11-08
