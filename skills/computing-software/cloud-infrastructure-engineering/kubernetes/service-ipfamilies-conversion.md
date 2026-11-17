---
id: computing-software.cloud-infrastructure-engineering.kubernetes.service-ipfamilies-conversion
name: service-ipfamilies-conversion
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, dual-stack, ipfamilies-change, ipfamilypolicy, services, ipv6]
level: practitioner
status: docs-checked
description: "Convert existing Services between single-stack and dual-stack by changing ipFamilyPolicy, and know which fields are immutable and what clients see."
sources: ["https://kubernetes.io/docs/concepts/services-networking/dual-stack/", "https://kubernetes.io/docs/tasks/network/validate-dual-stack/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Converting Services between single and dual stack

Existing Services in a cluster that becomes dual-stack are set to `ipFamilyPolicy: SingleStack`
with the family of the Service's existing cluster IP.

## Upgrade to dual stack
```bash
kubectl patch svc web -p '{"spec":{"ipFamilyPolicy":"PreferDualStack"}}'
kubectl get svc web -o jsonpath='{.spec.ipFamilies} {.spec.clusterIPs}'
```
Changing `ipFamilyPolicy` from `SingleStack` to `PreferDualStack` or `RequireDualStack` makes
Kubernetes assign the missing address family, so the Service gets an IPv4 and an IPv6 address.
`PreferDualStack` falls back to single-stack behaviour if dual-stack is not enabled or supported;
with `RequireDualStack` the Service API object creation fails in that case.

## Downgrade
```bash
kubectl patch svc web -p '{"spec":{"ipFamilyPolicy":"SingleStack"}}'
```
Kubernetes keeps only the first element of `.spec.clusterIPs`, sets `.spec.clusterIP` to that
address and sets `.spec.ipFamilies` to its family. Clients of the dropped family lose the Service.

## Rules
- `.spec.ipFamilies` is conditionally mutable: you can add or remove the secondary family, but you
  cannot change the primary family of an existing Service; recreate the Service to switch it.
- The first family listed in `ipFamilies` is used for the legacy `.spec.clusterIP` field.
- `type: LoadBalancer` needs `ipFamilyPolicy` of `PreferDualStack` or `RequireDualStack`, and the
  cloud provider must support both IPv4 and IPv6 load balancers.

## Verify
```bash
kubectl get svc web -o jsonpath='{.spec.ipFamilyPolicy} {.spec.ipFamilies} {.spec.clusterIPs}'
```
Then reach the Service from a pod once over each address family.

## Checked

2026-10-23, Kubernetes documentation (kubernetes/website main, v1.36 docs) and kubernetes/kubernetes source. Confirmed against the Dual-stack concept page: default SingleStack for existing Services, the switch procedure in both directions, conditional mutability of ipFamilies, PreferDualStack and RequireDualStack semantics, and the LoadBalancer note. Removed unconfirmed claims about headless-Service per-pod records, resolver address preference, immutability of the primary clusterIP value and the busybox test command.

Method: documentation only; no commands were run.
