---
id: computing-software.cloud-infrastructure-engineering.contour.contour-gateway-api-quickstart-httproute
name: contour-gateway-api-quickstart-httproute
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [gateway-api, httproute, quickstart, port-forward, kind, gatewayclass]
level: practitioner
status: docs-checked
description: "Step-by-step Contour plus Gateway API quickstart: CRDs, GatewayClass, Gateway, config map gatewayRef, echo HTTPRoute, and testing via port-forward."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/guides/gateway-api.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gateway API quickstart with Contour

Static path:
1. `kubectl apply -f` the Gateway API CRDs (`examples/gateway/00-crds.yaml`).
2. GatewayClass `contour` with `controllerName: projectcontour.io/gateway-controller`.
3. Gateway `contour` in namespace `projectcontour`, one listener `http` on port 80 with `allowedRoutes.namespaces.from: All`.
4. Deploy Contour via `quickstart/contour.yaml` (creates namespace, CRDs, RBAC, Contour Deployment and Service, Envoy DaemonSet and Service, ConfigMap).
5. Patch the `contour` ConfigMap `contour.yaml` with `gateway.gatewayRef` (name `contour`, namespace `projectcontour`) and `kubectl -n projectcontour rollout restart deployment/contour`.

Dynamic path: apply `quickstart/contour-gateway-provisioner.yaml` (provisioner namespace, Contour CRDs, Gateway API CRDs, RBAC, provisioner Deployment), create the same GatewayClass and Gateway; the provisioner builds Contour and Envoy.

Route traffic: apply the echo workload (`examples/example-workload/gatewayapi/echo/echo.yaml`): a Deployment and Service named `echo` plus an HTTPRoute attached to the `contour` Gateway for `local.projectcontour.io`. Check with `kubectl get po,svc,httproute -l app=echo`.

Test through the Envoy Service:

```
kubectl -n projectcontour port-forward service/envoy 8888:80          # static
kubectl -n projectcontour port-forward service/envoy-contour 8888:80  # dynamic
curl -i http://local.projectcontour.io:8888
```

`local.projectcontour.io` is a public DNS record resolving to 127.0.0.1, so the forwarded port works. Expect a 200 and a JSON body describing the forwarded request.

## Checked

2026-11-08: read the Contour docs guides/gateway-api in full. Confirmed: static and dynamic steps, GatewayClass and Gateway values, the objects each manifest creates, the ConfigMap gatewayRef and rollout restart, the echo resources, the verification command, the two port-forward targets, and the local.projectcontour.io curl test.

Method: documentation only; no commands were run.
