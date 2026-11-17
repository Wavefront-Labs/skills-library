---
id: computing-software.cloud-infrastructure-engineering.kubernetes.dual-stack-ipv4-ipv6-clusters
name: dual-stack-ipv4-ipv6-clusters
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, ipv6, ipv4, dual-stack, networking, service-cidr, pod-cidr, ipfamilypolicy, cni, cloud-provider]
level: advanced
status: docs-checked
description: "Run and debug dual-stack IPv4/IPv6 clusters: PodCIDR/ServiceCIDR sizing, IPFamilyPolicy on Services, and the CNI/cloud-LB gaps that make dual-stack harder than flipping a flag."
sources: ["https://kubernetes.io/docs/concepts/services-networking/dual-stack/", "https://kubernetes.io/docs/tasks/network/validate-dual-stack/", "https://kubernetes.io/docs/concepts/services-networking/network-policies/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dual-stack IPv4/IPv6 Kubernetes: what to configure and what to check

**Goal:** stand up and operate a dual-stack cluster, and know which parts depend on your cloud
provider and CNI.

## 1. What dual-stack turns on
- Pods and Services can receive both IPv4 and IPv6 addresses. Dual-stack is enabled by default
  from Kubernetes 1.21 (the feature is stable since 1.23) once the components are configured.
- Services use `spec.ipFamilyPolicy` (`SingleStack`, `PreferDualStack`, `RequireDualStack`) and
  `spec.ipFamilies`. The first family listed is used for the legacy `spec.clusterIP` field.
  The address family of a Service defaults to the family of the first service cluster IP range.
- Required configuration, from the Dual-stack page:
  - kube-apiserver: `--service-cluster-ip-range=<IPv4 CIDR>,<IPv6 CIDR>`
  - kube-controller-manager: `--cluster-cidr=<IPv4 CIDR>,<IPv6 CIDR>` and
    `--service-cluster-ip-range=<IPv4 CIDR>,<IPv6 CIDR>`
    (`--node-cidr-mask-size-ipv4` / `--node-cidr-mask-size-ipv6` default to /24 and /64)
  - kube-proxy: `--cluster-cidr=<IPv4 CIDR>,<IPv6 CIDR>`
  - kubelet: `--node-ip=<IPv4 IP>,<IPv6 IP>`, required for bare-metal dual-stack nodes; the
    legacy built-in cloud providers do not support dual-stack `--node-ip`.
- Your provider (cloud or otherwise) must be able to supply routable IPv4 and IPv6 addresses
  to nodes, and your CNI plugin must support IPv6.

## 2. Practical failure points
1. **LoadBalancer Services.** A dual-stack load balancer needs `type: LoadBalancer` with
   `ipFamilyPolicy` of `PreferDualStack` or `RequireDualStack`, and a cloud provider that supports
   IPv4 and IPv6 load balancers. Check the actual cloud resource.
2. **Egress.** Pods with non-publicly-routable IPv6 addresses need a publicly routed IPv6 address
   for off-cluster destinations, through transparent proxying or masquerading; the
   `ip-masq-agent` project supports masquerading on dual-stack clusters.
3. **Applications.** Anything that assumes one address per Service must read `spec.clusterIPs`
   (plural) rather than `spec.clusterIP`.

## 3. NetworkPolicy and dual-stack
An `ipBlock` rule selects an IP CIDR range, and a CIDR is of a single address family, so write
separate entries for IPv4 and IPv6 ranges where a policy has to cover both, or select by pod and
namespace instead of by CIDR.

## Debug routine
```bash
kubectl get nodes -o jsonpath='{.items[*].spec.podCIDRs}'
kubectl get svc myapp -o jsonpath='{.spec.ipFamilyPolicy} {.spec.ipFamilies} {.spec.clusterIPs}'
kubectl get pod <pod> -o jsonpath='{.status.podIPs}'
```
Then test from a pod to both addresses of the Service and of a pod.

## Verify
- [ ] A `RequireDualStack` Service shows two `clusterIPs`, and both answer from a pod.
- [ ] The cloud load balancer behind a LoadBalancer Service has the address families you intended.
- [ ] NetworkPolicy rules cover both families where the policy is meant to cover all traffic.

## Checked

2026-10-23, Kubernetes documentation (kubernetes/website main, v1.36 docs) and kubernetes/kubernetes source. Confirmed against the Dual-stack concept page: default-on since 1.21 and stable in 1.23, the component flags and mask defaults, first-family rules, LoadBalancer note, egress note (ip-masq-agent). Removed unconfirmed CNI and cloud capability claims (Cilium, Calico, Flannel, per-VPC IPv6 quotas), sizing advice for IPv6 pod CIDRs, Happy Eyeballs statements and the IPv6 curl commands. Replaced prose-title sources with URLs.

Method: documentation only; no commands were run.
