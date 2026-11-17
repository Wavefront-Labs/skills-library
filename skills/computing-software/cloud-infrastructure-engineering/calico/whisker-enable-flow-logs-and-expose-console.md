---
id: computing-software.cloud-infrastructure-engineering.calico.whisker-enable-flow-logs-and-expose-console
name: whisker-enable-flow-logs-and-expose-console
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [whisker, goldmane, flow-logs, observability, tech-preview, port-forward, ingress-gateway, operator]
level: practitioner
status: docs-checked
description: "Enable Goldmane and Whisker with two operator resources, view by port-forward, or expose through Calico Ingress Gateway with a hostname."
sources:
  - https://docs.tigera.io/calico/latest/observability/enable-whisker
  - https://docs.tigera.io/calico/latest/observability/view-flow-logs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Flow logs are a tech preview feature. Two components: **Goldmane** (the flow logs API, aggregates logs and serves them over gRPC; usable without Whisker) and **Whisker** (the web console; needs Goldmane). Both are installed by default in new 3.30+ installs and not enabled if you upgraded. They need an operator or Helm install; manifest installs are unsupported.

**Enable:**

```bash
kubectl apply -f - <<EOF
apiVersion: operator.tigera.io/v1
kind: Goldmane
metadata:
  name: default
EOF
```

and the same with `kind: Whisker`.

**View by port-forward** (Whisker exposes nothing by default, and Calico creates policies denying ingress to it):

```bash
kubectl port-forward -n calico-system service/whisker 8443:8443
```

Open `https://localhost:8443`; the certificate is self-signed.

**Expose with Calico Ingress Gateway** (needs a `GatewayAPI` resource, and an IP pool for the load balancer address on bare metal):

```bash
kubectl patch whisker default --type merge -p '{"spec":{"ingressGateway":{"hostname":"whisker.example.com"}}}'
```

Optional fields: `gatewayNamespace` (created if missing) and `gatewayClassName` when several classes exist. Read the address with `kubectl get gateway -n calico-system calico-whisker-gateway` and point DNS at it. While `spec.ingressGateway` is set only that gateway's proxy pods may reach Whisker. Remove it with a JSON patch `remove` of `/spec/ingressGateway`.

**Warning from the page:** Whisker and Goldmane hold sensitive data, so put your own authentication in front before exposing them.

## Checked

Read in full on 2026-11-08: the Enable the flow logs API and Calico Whisker page and the View flow logs page. Both resources, the port-forward command, the self-signed certificate, the Ingress Gateway patch and its prerequisites, and the removal patch match them.

Method: documentation only; no commands were run.
