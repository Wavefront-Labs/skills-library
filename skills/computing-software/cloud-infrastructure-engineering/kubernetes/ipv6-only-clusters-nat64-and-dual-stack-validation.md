---
id: computing-software.cloud-infrastructure-engineering.kubernetes.ipv6-only-clusters-nat64-and-dual-stack-validation
name: ipv6-only-clusters-nat64-and-dual-stack-validation
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, ipv6, ipv6-only, single-stack-ipv6, nat64, dns64, dual-stack-ingress, dual-stack-validation, eks-ipv6]
level: advanced
status: docs-checked
description: "Run IPv6-only clusters (pod/service CIDRs, EKS IPv6), reach IPv4 services via NAT64/DNS64, expose dual-stack ingress, and validate pod, Service and node addressing."
sources: ["https://kubernetes.io/docs/concepts/services-networking/dual-stack/", "https://kubernetes.io/docs/tasks/network/validate-dual-stack/", "https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/dual-stack-support/", "https://docs.aws.amazon.com/eks/latest/userguide/cni-ipv6.html", "https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-nat64-dns64.html", "https://coredns.io/plugins/dns64/", "https://kubernetes-sigs.github.io/aws-load-balancer-controller/latest/guide/service/annotations/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IPv6-only clusters, NAT64/DNS64 and dual-stack validation

## Why IPv6-only
IPv4 exhaustion in large VPCs (VPC CNI pod IPs), no overlapping-CIDR pain between clusters.
Cost: every IPv4-only dependency needs translation.

## Setting up (kubeadm)
```yaml
apiVersion: kubeadm.k8s.io/v1beta4
kind: InitConfiguration
localAPIEndpoint:
  advertiseAddress: "2001:db8::10"
---
apiVersion: kubeadm.k8s.io/v1beta4
kind: ClusterConfiguration
networking:
  podSubnet: fd00:10:244::/56
  serviceSubnet: fd00:10:96::/112      # kube-apiserver rejects IPv6 service ranges with a prefix shorter than /108
```
`advertiseAddress` in `InitConfiguration` is the API server's advertised address (the
`--apiserver-advertise-address` flag equivalent). The CNI must support IPv6 (Calico, Cilium,
Flannel with `EnableIPv4: false`); set kube-proxy's `clusterCIDR` to the IPv6 range; enable
`net.ipv6.conf.all.forwarding=1`; use IPv6 node IPs (kubelet `--node-ip`).

**EKS** (AWS documentation): choose the IP family at cluster creation; it cannot be changed
afterwards, and an existing cluster cannot be switched. EKS does not support dual-stack
Pods or Services: Services get only IPv6 addresses, and Pods get an IPv6 address plus a
host-local IPv4 address that VPC CNI SNATs to the node's primary ENI IPv4 address when the
Pod talks to external IPv4 destinations. AWS states this built-in node NAT eliminates the
need for DNS64 and NAT64 on EKS. Nodes are assigned both IPv4 and IPv6 addresses. Other
requirements from the page: Nitro-based EC2 or Fargate nodes, VPC CNI 1.10.1 or later, an
IPv4 and an IPv6 CIDR on the VPC and subnets, subnets that auto-assign IPv6 to nodes, IPv6
routes and security group rules, no custom networking, and AWS Load Balancer Controller
2.3.1 or later with load balancers in IP (not instance) mode.

## Reaching IPv4 from IPv6-only pods (self-managed clusters)
- **DNS64**: the CoreDNS `dns64` plugin synthesizes AAAA answers from A records when a name
  has no AAAA record, only for queries that arrive over IPv6, using the well-known prefix
  `64:ff9b::/96` by default:
```
.:53 {
    dns64 { prefix 64:ff9b::/96 }
    forward . /etc/resolv.conf
    ...
}
```
- **NAT64** gateway translates `64:ff9b::a.b.c.d` to IPv4. AWS NAT gateways support NAT64,
  used with DNS64 on Route 53 Resolver or your own DNS64 server.
- Apps that hardcode IPv4 literals never query DNS, so DNS64 cannot help them; find them early.

## Dual-stack ingress / LBs
To give an IPv6-backed workload IPv4 reachability, use a load balancer that supports both
families. With the AWS Load Balancer Controller: Service annotation
`service.beta.kubernetes.io/aws-load-balancer-ip-address-type: dualstack` (NLB) and Ingress
annotation `alb.ingress.kubernetes.io/ip-address-type: dualstack` (ALB; the controller docs
list `ipv4`, `dualstack` and `dualstack-without-public-ipv4`).
On dual-stack clusters a Service can set `ipFamilyPolicy: RequireDualStack` with
`ipFamilies: [IPv6, IPv4]`; `.spec.clusterIP` is the first family listed.

## Validate addressing
```bash
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.podCIDRs}{"\t"}{.status.addresses}{"\n"}{end}'
kubectl get pod p -o jsonpath='{.status.podIPs}'
kubectl get svc web -o jsonpath='{.spec.ipFamilyPolicy} {.spec.clusterIPs}'
kubectl exec p -- ip -6 addr; kubectl exec p -- ping -6 -c2 <other-pod-ipv6>
kubectl exec p -- curl -6 -sI http://web.default.svc.cluster.local
kubectl exec p -- nslookup -type=AAAA example.com     # DNS64 returns 64:ff9b:: on IPv4-only names
```

## Verify
- [ ] Pods, Services and nodes report the expected families; pod to IPv4 internet works via NAT64 (or EKS node NAT); the LB answers on both families.

## Checked
2026-10-27. Documentation releases: Kubernetes website main (v1.38 dev tree; latest release v1.37.1) and kube-apiserver and kubeadm sources at v1.37.1; EKS user guide and VPC NAT64 page (current); CoreDNS dns64 plugin page; AWS Load Balancer Controller docs (main).
Confirmed: kubeadm `localAPIEndpoint.advertiseAddress` and subnet fields; /108 minimum service prefix; EKS IPv6 behaviour (no dual-stack Pods/Services, host-local IPv4 SNAT, immutability, prerequisites); dns64 semantics and default prefix; AWS NAT gateway NAT64 with Route 53 Resolver DNS64; the two load-balancer annotations and values; `ipFamilies` ordering.
Method: documentation only; no commands were run.
