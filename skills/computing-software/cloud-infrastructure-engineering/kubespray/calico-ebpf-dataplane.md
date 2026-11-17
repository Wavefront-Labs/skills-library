---
id: computing-software.cloud-infrastructure-engineering.kubespray.calico-ebpf-dataplane
name: calico-ebpf-dataplane
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [calico, ebpf, bpf, kube-proxy, dsr, host-endpoints]
level: sme
status: docs-checked
description: "Enable the Calico eBPF dataplane in Kubespray: remove kube-proxy and ipvs leftovers, set the API endpoint, DSR mode and BPF debug logging."
sources:
  - https://kubespray.io/docs/CNI/calico.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Enable the eBPF dataplane in the inventory. kube-proxy is incompatible with this mode and must be removed from the system:

```yaml
calico_bpf_enabled: true
```

Advice from the page: use the latest Calico with eBPF. On Ubuntu, run the `-generic` kernel, because `kernel-kvm` lacks `CONFIG_NET_SCHED`.

**Convert an existing cluster.** Calico node cannot clean up after kube-proxy in ipvs mode. Delete the `kube-proxy` DaemonSet and clean ipvs leftovers. Check with `ipvsadm -l`, clean with `ipvsadm -C`.

**API access.** Calico node, typha and kube-controllers must reach the Kubernetes API. Kubespray creates the `kubernetes-services-endpoint` configmap from `kube_apiserver_cluster_internal_endpoint`. Without an external load balancer, eBPF can use the localhost load balancer only if its port equals the kube-apiserver port; then enable Calico Automatic Host Endpoints so services like `coredns` and `metrics-server` can reach the Kubernetes host endpoint.

**DSR.** The default is Tunneled service mode:

```yaml
calico_bpf_service_mode: "DSR"
```

**Logging.**

```yaml
calico_bpf_log_level: "Debug"
```

Read the output through the kernel trace buffer with `tc exec bpf debug`.

## Checked

2026-11-08. Cited pages re-read in full. Variables, kernel caveat and cleanup commands were confirmed under eBPF Support on the Calico page.

Method: documentation only; no commands were run.
