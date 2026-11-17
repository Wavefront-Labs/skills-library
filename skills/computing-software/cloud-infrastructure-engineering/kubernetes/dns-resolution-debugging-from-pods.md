---
id: computing-software.cloud-infrastructure-engineering.kubernetes.dns-resolution-debugging-from-pods
name: dns-resolution-debugging-from-pods
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, dns, coredns, nslookup-debug, servfail, nxdomain, ndots, dns-troubleshooting, cka]
level: practitioner
status: docs-checked
description: "Debug pod DNS failures step by step: dnsutils pod, nslookup/dig against CoreDNS, reading SERVFAIL vs NXDOMAIN vs timeout, resolv.conf/ndots, CoreDNS logs and NetworkPolicy blocks."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/dns-debugging-resolution/", "https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/", "https://coredns.io/plugins/log/", "https://coredns.io/plugins/loop/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Debugging DNS resolution from pods

## 1. Get a test pod with tools
The Kubernetes DNS debugging page uses a `dnsutils` Pod (manifest
`admin/dns/dnsutils.yaml` in the website examples, image
`registry.k8s.io/e2e-test-images/agnhost:2.39`):
```bash
kubectl apply -f https://k8s.io/examples/admin/dns/dnsutils.yaml
kubectl exec -ti dnsutils -- cat /etc/resolv.conf
```
The documented healthy output has `nameserver <cluster DNS IP>`,
`search <namespace>.svc.cluster.local svc.cluster.local cluster.local` and `options ndots:5`.
If NetworkPolicies select pods by label, test from a pod that carries the same labels.

## 2. Query
```bash
kubectl exec -i -t dnsutils -- nslookup kubernetes.default
```
If it fails ("can't resolve 'kubernetes.default'"), work through the next steps in order.

## 3. CoreDNS side
```bash
kubectl get pods --namespace=kube-system -l k8s-app=kube-dns
kubectl logs --namespace=kube-system -l k8s-app=kube-dns
kubectl get endpointslice -l kubernetes.io/service-name=kube-dns --namespace=kube-system
```
The `k8s-app` label value for CoreDNS is `kube-dns`, for backward compatibility. Check the
logs for suspicious messages, check that the `kube-dns` Service has endpoints, and enable the CoreDNS
`log` plugin in the Corefile ConfigMap to see whether queries arrive.
If the CoreDNS `loop` plugin reports a loop, CoreDNS is forwarding to itself, commonly because
the node's `/etc/resolv.conf` lists a local address such as `127.0.0.53` (systemd-resolved);
point the kubelet's resolv.conf setting at a file with real upstream servers, as the CoreDNS
loop plugin documentation describes.

## 4. ndots amplification
With `ndots:5`, a name with fewer than 5 dots is tried against each search domain first. Use fully
qualified names with a trailing dot in configuration, or set `ndots` lower through
`dnsConfig.options` for pods that mostly resolve external names.

## Verify
- [ ] `nslookup kubernetes.default` and an external name resolve from the application's namespace.

## Checked

2026-10-23, Kubernetes documentation (kubernetes/website main, v1.36 docs) and kubernetes/kubernetes source. Confirmed against the Debugging DNS Resolution task page (dnsutils pod and agnhost image from the website example manifest, resolv.conf contents, k8s-app=kube-dns label, kubectl logs, EndpointSlice check) and the CoreDNS loop and log plugin documentation (loop cause and loopback nameserver advice). Removed the rcode troubleshooting table, the dig commands, the 5-second delay and conntrack claims, the SERVFAIL metric and exact error strings.

Method: documentation only; no commands were run.
