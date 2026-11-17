---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kube-proxy-configuration-and-nftables-mode
name: kube-proxy-configuration-and-nftables-mode
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kube-proxy, kubeproxyconfiguration, kube-proxy-config, nftables, masquerade-all, iptables, ipvs]
level: advanced
status: docs-checked
description: "Configure kube-proxy via KubeProxyConfiguration (mode, clusterCIDR, conntrack, nodePortAddresses, masquerade) and migrate to the nftables mode that replaces iptables at scale."
sources: ["https://kubernetes.io/docs/reference/networking/virtual-ips/", "https://kubernetes.io/docs/reference/config-api/kube-proxy-config.v1alpha1/", "https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/", "https://github.com/kubernetes/kubernetes/blob/master/pkg/proxy/nftables/proxier.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KubeProxyConfiguration and nftables mode

## Where it lives
kubeadm: ConfigMap `kube-system/kube-proxy` key `config.conf` (a KubeProxyConfiguration), read
by the kube-proxy DaemonSet. Edit, then restart the kube-proxy pods (`kubectl -n kube-system rollout restart ds/kube-proxy`).
For new clusters put it in the kubeadm config as a separate YAML document.
```yaml
apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration
mode: nftables                        # iptables (default on Linux) | ipvs (deprecated) | nftables
clusterCIDR: 10.244.0.0/16            # CIDR of the cluster's pods; used to detect local traffic
nodePortAddresses: ["primary"]        # default in nftables mode; iptables and ipvs default to all addresses
masqueradeAll: false                  # true = SNAT all traffic to Service cluster IPs (iptables/ipvs only; some CNIs need it)
conntrack:
  maxPerCore: 32768                   # 0 leaves the kernel limit as-is
  min: 131072
iptables: {minSyncPeriod: 1s, syncPeriod: 30s}
metricsBindAddress: 0.0.0.0:10249     # default 127.0.0.1:10249, so Prometheus cannot scrape
```

## nftables mode (beta 1.31, GA 1.33)
Why: the nftables API is the successor to iptables and processes Service and EndpointSlice changes faster and
more efficiently, and also handles packets more efficiently in the kernel (noticeable only with tens of thousands
of Services). The project recommends it as the replacement for both `iptables` and `ipvs` modes, and a future
version will make it the default, so set `mode` explicitly.
Requirement: Linux kernel 5.13 or later.
Differences to know before switching:
- NodePorts answer only on `nodePortAddresses`, default `primary` (the node's primary IPs). To serve them on
  `127.0.0.1` you need the alpha `KubeProxyNFTablesLocalhostNodePorts` gate and `primary,localhost`; check the
  `iptables_localhost_nodeports_accepted_packets_total` metric to see if anything depends on it.
- In iptables mode kube-proxy adds accept rules for NodePorts for aggressive firewalls; nftables mode does not,
  so allow the NodePort range in a local firewall yourself.
- Kernels before 6.1 can reset long-lived TCP connections to Service IPs; iptables mode installs a
  workaround, nftables mode does not. Check `iptables_ct_state_invalid_dropped_packets_total`, and if needed
  set `conntrack.tcpBeLiberal` (`--conntrack-tcp-be-liberal`).
- On start kube-proxy removes the iptables and ipvs rules left by the previous mode.

Migration: kubeadm runs kube-proxy as a DaemonSet with one shared config, so node-specific configuration is
unsupported; switch cluster-wide and watch the Service tests below.
```bash
nft list table ip kube-proxy
nft list map ip kube-proxy service-ips
```

## Verify
- [ ] `kubectl -n kube-system logs ds/kube-proxy | grep -i "Using nftables Proxier"`.
- [ ] Service and NodePort tests pass from pods and from outside; `kubeproxy_sync_proxy_rules_duration_seconds` is lower than before.

## Checked

2026-10-26: kubernetes.io virtual-ips page (v1.37 docs, kubernetes/website main 2026-10-25), the kube-proxy config API source and kube-proxy nftables proxier source (kubernetes/kubernetes main), and the NFTablesProxyMode feature-gate page. Confirmed: mode values and iptables default, nodePortAddresses keywords and per-mode defaults, kernel 5.13, beta 1.31 and GA 1.33, differences list (NodePort addresses, firewall, conntrack workaround, localhost NodePorts gate), nft table and map names, log line. Removed the unconfirmed 1.29 note, conntrack timeout values, CNI interoperability claim and per-node-pool migration advice.

Method: documentation only; no commands were run.
