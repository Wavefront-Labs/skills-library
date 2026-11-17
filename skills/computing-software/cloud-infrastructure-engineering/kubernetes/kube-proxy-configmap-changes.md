---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kube-proxy-configmap-changes
name: kube-proxy-configmap-changes
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kube-proxy, kube-proxy-configmap, kubeproxyconfiguration, kube-proxy-config]
level: practitioner
status: docs-checked
description: "Change kube-proxy settings in a kubeadm cluster: edit the kube-proxy ConfigMap, roll the DaemonSet, keep changes across kubeadm upgrades, and verify mode."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-reconfigure/", "https://kubernetes.io/docs/reference/networking/virtual-ips/", "https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/", "https://kubernetes.io/docs/reference/config-api/kube-proxy-config.v1alpha1/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Changing kube-proxy configuration

## Edit
```bash
kubectl -n kube-system edit configmap kube-proxy     # key: data.config.conf (KubeProxyConfiguration)
```
Example changes:
```yaml
mode: nftables               # iptables (default) | nftables | ipvs (deprecated since 1.35)
conntrack:
  maxPerCore: 65536
metricsBindAddress: 0.0.0.0:10249     # default 127.0.0.1:10249 hides metrics from Prometheus
nodePortAddresses: ["10.0.0.0/16"]   # CIDRs and/or the keywords primary, localhost, all
```

## Apply
Restart the kube-proxy pods so new ones pick up the ConfigMap. The kubeadm docs delete them by label:
```bash
kubectl delete po -n kube-system -l k8s-app=kube-proxy
```
(`kubectl -n kube-system rollout restart daemonset kube-proxy` has the same effect.) kubeadm deploys kube-proxy
as a DaemonSet, so node-specific configuration is unsupported.

## Persist across kubeadm upgrades
kubeadm writes its KubeProxyConfiguration into the `kube-proxy` ConfigMap during cluster creation and upgrade,
so re-check your edits after `kubeadm upgrade`. For new clusters, put the config in the kubeadm config file as a
`KubeProxyConfiguration` document (separated by `---`) so it is in Git. The kubeadm reconfigure page describes
the supported flow.

## Switching modes
- To ipvs: deprecated since 1.35, disabled by default from 1.40 (re-enable with the `KubeProxyIPVS` gate) and
  removed in 1.43; kube-proxy fails to start with "can't use the IPVS proxier" if prerequisites are missing.
  Prefer nftables.
- To nftables: Linux kernel 5.13 or later; the mode is beta in 1.31 and GA in 1.33.
- Set `mode` explicitly: the default is `iptables` today but a future version will change it to `nftables`.
- On start kube-proxy removes stale rules of the other backends (switching to nftables removes iptables and
  ipvs rules; switching to iptables or ipvs removes nftables rules); `kube-proxy --cleanup` removes rules and exits.

## Verify
```bash
kubectl -n kube-system logs ds/kube-proxy       # "Using nftables Proxier" (or iptables / ipvs)
curl -s http://127.0.0.1:10249/proxyMode        # run on the node; the metrics port binds to localhost by default
```

## Checked

2026-10-26: kubernetes.io kubeadm-reconfigure, virtual-ips and kube-proxy reference pages (v1.37 docs, kubernetes/website main 2026-10-25), the kube-proxy config API source and kube-proxy server source (kubernetes/kubernetes main), and the KubeProxyIPVS and NFTablesProxyMode feature-gate pages. Confirmed: ConfigMap name and data.config.conf key, restart procedure, DaemonSet no per-node config, mode values and default, ipvs deprecation timeline, nftables kernel 5.13 and stage history, cleanup behaviour, /proxyMode on the metrics port. Removed the unconfirmed IPVS module list and the upgrade-persistence claim.

Method: documentation only; no commands were run.
