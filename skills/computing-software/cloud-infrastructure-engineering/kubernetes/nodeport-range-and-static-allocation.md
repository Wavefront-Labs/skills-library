---
id: computing-software.cloud-infrastructure-engineering.kubernetes.nodeport-range-and-static-allocation
name: nodeport-range-and-static-allocation
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, service, nodeport, service-node-port-range, kube-apiserver]
level: practitioner
status: docs-checked
description: "Configure the NodePort range (--service-node-port-range), pick static NodePorts safely with the reserved static band, and open firewalls to match."
sources: ["https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport", "https://kubernetes.io/docs/reference/networking/virtual-ips/", "https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# NodePort range and static allocation

## Range
Default `30000-32767`, set by the kube-apiserver flag `--service-node-port-range`. With kubeadm
pass it as an API server extra argument:
```yaml
apiServer:
  extraArgs:
  - name: service-node-port-range
    value: "30000-32767"
```
Run every API server with the same range.

## Static vs dynamic
```yaml
spec:
  type: NodePort
  ports:
  - port: 80
    targetPort: 8080
    nodePort: 30080      # static; omit for dynamic allocation
```
The range is split into a lower static band and an upper dynamic band (feature gate
ServiceNodePortStaticSubrange: alpha 1.27, beta 1.28, stable 1.29). Dynamic allocation uses the
upper band by default and may use the lower band once the upper is exhausted, so choosing static
ports from the lower band lowers the chance of collisions. For the default range the documented
bands are static 30000-30085 and dynamic 30086-32767.

## Firewall and LB
- Every node can expose every NodePort, so firewalls and security groups must allow the range
  from your load balancer or clients.
- With `externalTrafficPolicy: Local`, load balancer health checks should fail on nodes without a
  ready local endpoint; the details depend on the cloud provider integration.
- Restrict which node addresses accept NodePort traffic with kube-proxy `--nodeport-addresses`
  (or `nodePortAddresses` in its configuration). Values can be CIDRs, `primary` (the node's
  primary IPv4/IPv6 addresses; the default in nftables mode), `localhost`, or `all` (the default
  for iptables and ipvs modes).

## Verify
```bash
kubectl get svc -A
```
and read the PORT(S) column for `NodePort` entries. `provided port is already allocated` on create
means a collision: choose another port.

## Checked

2026-10-23, Kubernetes documentation (kubernetes/website main, v1.36 docs) and kubernetes/kubernetes source. Confirmed against the Service concept page (default range, flag name, static and dynamic bands 30000-30085 and 30086-32767), the feature-gate reference (ServiceNodePortStaticSubrange stages) and the virtual-IPs page (nodeport-addresses values and per-mode defaults). Removed the band-size formula, the jq/grep and curl commands and the sentence about changing the range, none of which the pages state.

Method: documentation only; no commands were run.
