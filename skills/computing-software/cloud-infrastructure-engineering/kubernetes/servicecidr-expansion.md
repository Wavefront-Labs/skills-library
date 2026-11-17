---
id: computing-software.cloud-infrastructure-engineering.kubernetes.servicecidr-expansion
name: servicecidr-expansion
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, service, servicecidr, clusterip, kube-apiserver]
level: practitioner
status: docs-checked
description: "Size the Service CIDR, detect ClusterIP exhaustion, and add ranges at runtime with ServiceCIDR and IPAddress objects (MultiCIDRServiceAllocator)."
sources: ["https://kubernetes.io/docs/tasks/network/extend-service-ip-ranges/", "https://kubernetes.io/docs/concepts/services-networking/cluster-ip-allocation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Service CIDR sizing and expansion

## Sizing
kube-apiserver `--service-cluster-ip-range` (kubeadm `networking.serviceSubnet`, default
`10.96.0.0/12`). Each Service with a ClusterIP takes one address from the range. As a soft
convention some installers give the cluster DNS Service the 10th address, but that address is not
reserved, so a dynamic allocation can take it first.

Exhaustion symptom: `failed to allocate a serviceIP: range is full`.

## Inspect allocation
MultiCIDRServiceAllocator (alpha 1.27, beta 1.31, stable 1.33) represents the ranges as
`ServiceCIDR` objects and every allocated ClusterIP as an `IPAddress` object:
```bash
kubectl get servicecidrs
kubectl get ipaddresses
```
The control plane keeps a `ServiceCIDR` named `kubernetes` for the configured range; the
`kubernetes` Service takes its first address.

## Add a range at runtime
```yaml
apiVersion: networking.k8s.io/v1
kind: ServiceCIDR
metadata: {name: extra-1}
spec:
  cidrs: ["10.112.0.0/20"]
```
Creating a new ServiceCIDR increases the number of addresses available for Services.

## Constraints
- Plan ranges so they do not overlap with other networks in use (pod ranges, node networks,
  routed networks).
- ServiceCIDRs are protected by finalizers: you cannot delete one while IPAddress objects depend
  on it. The finalizer is only removed if another ServiceCIDR contains the existing addresses, or
  no IPAddress belongs to the range. The `Ready` condition shows `OrphanIPAddress` in that case.
- Overlap and other policy can be enforced with ValidatingAdmissionPolicy.

## Verify
```bash
kubectl get servicecidr extra-1 -o yaml
```
Check `status.conditions` shows `Ready`.

## Checked

2026-10-23, Kubernetes documentation (kubernetes/website main, v1.36 docs) and kubernetes/kubernetes source. Confirmed against the Extend Service IP Ranges task page (ServiceCIDR and IPAddress objects, GA 1.33, kubernetes ServiceCIDR, finalizer and OrphanIPAddress behaviour, the "range is full" error text), the cluster IP allocation page (10th-address convention not reserved) and kubernetes/kubernetes source (kubeadm default 10.96.0.0/12). Removed managed-service default sizes, headless address claims, the awk and dry-run commands, and the claim about replacing the default range.

Method: documentation only; no commands were run.
