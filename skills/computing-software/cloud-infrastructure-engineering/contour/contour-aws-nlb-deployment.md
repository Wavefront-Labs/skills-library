---
id: computing-software.cloud-infrastructure-engineering.contour.contour-aws-nlb-deployment
name: contour-aws-nlb-deployment
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [aws, nlb, host-ports, source-ip, x-forwarded-for, envoy-service, examples-contour]
level: practitioner
status: docs-checked
description: "Deploying Contour on AWS behind a Network Load Balancer: change the Envoy Service annotation to type nlb, host ports 80/443, retained source IPs, retrieving the NLB hostname."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/guides/deploy-aws-nlb.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Contour on AWS with an NLB

NLBs are often cheaper (idle ones cost nothing), add no extra network hop (NLB to node to pod) and retain the source IP, which Envoy records in `X-Forwarded-For`.

Design: Envoy runs as a DaemonSet on host ports 80 and 443 so traffic hits it directly; Contour runs as a Deployment and binds 8001 for Envoy to Contour xDS traffic.

Steps:
1. Clone the Contour repository.
2. Edit the Envoy Service `02-service-envoy.yaml` under `examples/contour`:
   - remove `service.beta.kubernetes.io/aws-load-balancer-backend-protocol: tcp`
   - add `service.beta.kubernetes.io/aws-load-balancer-type: nlb`
3. `kubectl apply -f examples/contour`. This creates the `projectcontour` namespace, ServiceAccount, RBAC, the Contour Deployment, the Envoy DaemonSet and the NLB.

Find its address:

```sh
kubectl get service envoy --namespace=projectcontour -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
```

Test: install the echo workload from the deploy guide, then browse to the NLB DNS name. The response shows an `X-Forwarded-For` header filled by Envoy, because Envoy was the first hop to see the browser's address directly.

## Checked

2026-11-08: read the Contour docs guides/deploy-aws-nlb in full. Confirmed: the three advantages, Envoy DaemonSet on host ports 80 and 443, Contour binding 8001, the annotation removed and added in 02-service-envoy.yaml, the kubectl apply step and what it creates, the jsonpath command, and the X-Forwarded-For test. Removed: the closing PROXY protocol sentence, which is not in this guide.

Method: documentation only; no commands were run.
