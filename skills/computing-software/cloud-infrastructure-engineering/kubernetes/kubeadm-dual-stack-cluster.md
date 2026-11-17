---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubeadm-dual-stack-cluster
name: kubeadm-dual-stack-cluster
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, dual-stack, dual-stack-kubeadm, ipv6, ipfamilypolicy, kubeadm, node-ip]
level: practitioner
status: docs-checked
description: "Build a dual-stack IPv4/IPv6 cluster with kubeadm: podSubnet and serviceSubnet pairs, kubelet node-ip for both families, CNI support and validation."
sources: ["https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/dual-stack-support/", "https://kubernetes.io/docs/concepts/services-networking/dual-stack/", "https://github.com/kubernetes/kubernetes/blob/master/cmd/kubeadm/app/preflight/checks_linux.go"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Dual-stack with kubeadm

## Prerequisites
Nodes with routable IPv4 and IPv6 addresses, IPv6 forwarding enabled
(`net.ipv6.conf.all.forwarding = 1`), and a CNI plugin that supports dual-stack (see its own
documentation). kubeadm's preflight checks the forwarding sysctls. Note that
`--apiserver-advertise-address` does not support dual-stack, and etcd itself is not dual-stack.

## kubeadm config
```yaml
apiVersion: kubeadm.k8s.io/v1beta4
kind: ClusterConfiguration
networking:
  podSubnet: 10.244.0.0/16,fd00:10:244::/56
  serviceSubnet: 10.96.0.0/16,fd00:10:96::/112
---
apiVersion: kubeadm.k8s.io/v1beta4
kind: InitConfiguration
localAPIEndpoint:
  advertiseAddress: 10.0.0.11
nodeRegistration:
  kubeletExtraArgs:
  - name: node-ip
    value: 10.0.0.11,fd00::11
```
The first family listed is the primary (default for single-stack Services). Joins need the same
`node-ip` pair in JoinConfiguration (`nodeRegistration.kubeletExtraArgs`).

## CNI
Configure the CNI with address pools for both families that match `podSubnet`; the exact
settings are CNI specific.

## Services
Existing and new Services default to `SingleStack`; opt in:
```yaml
spec:
  ipFamilyPolicy: PreferDualStack
  ipFamilies: [IPv4, IPv6]
```

## Validate
```bash
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name} {.status.addresses}{"\n"}{end}'
kubectl get pods -o custom-columns=POD:.metadata.name,IPS:.status.podIPs
kubectl get svc web -o jsonpath='{.spec.clusterIPs}'
kubectl run t --rm -it --image=<image-with-curl> --restart=Never -- curl -6 -s "http://[<service-ipv6>]/"
```
Each node should report two InternalIPs and each pod two podIPs.

## Checked

Checked 2026-10-26 against Kubernetes documentation v1.37 (kubernetes/website and kubernetes/kubernetes master, commit dates 2026-10-24/25). Confirmed: the v1beta4 `networking.podSubnet` and `serviceSubnet` comma-separated pairs, `kubeletExtraArgs` `node-ip` lists for InitConfiguration and JoinConfiguration, the IPv6 forwarding sysctl, that `--apiserver-advertise-address` and etcd are not dual-stack, and that new Services default to `SingleStack` with `PreferDualStack`/`RequireDualStack` as opt-ins and the first listed family primary. Removed as unconfirmed: the IPv6 service subnet size limit, the per-CNI setting names, and the third-party test image.

Method: documentation only; no commands were run.
