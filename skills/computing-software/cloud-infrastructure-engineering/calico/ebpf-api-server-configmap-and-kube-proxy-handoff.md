---
id: computing-software.cloud-infrastructure-engineering.calico.ebpf-api-server-configmap-and-kube-proxy-handoff
name: ebpf-api-server-configmap-and-kube-proxy-handoff
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [ebpf, kube-proxy, configmap, kubernetes-services-endpoint, felixconfiguration, api-server, mke, openshift]
level: advanced
status: docs-checked
description: "Prepare eBPF mode: set the kubernetes-services-endpoint ConfigMap for a stable API server address and disable or neutralise kube-proxy per platform, with Felix settings if needed."
sources:
  - https://docs.tigera.io/calico/latest/operations/ebpf/enabling-ebpf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Because eBPF mode replaces kube-proxy, Calico must reach the API server directly. Create the ConfigMap `kubernetes-services-endpoint` with the stable host and port. Namespace is `tigera-operator` for operator installs (the operator rolls Calico out automatically) and `kube-system` for manifest installs (wait about 60 seconds, then delete the `calico-node`, `calico-kube-controllers` and, if used, `calico-typha` pods).

```yaml
kind: ConfigMap
apiVersion: v1
metadata:
  name: kubernetes-services-endpoint
  namespace: tigera-operator
data:
  KUBERNETES_SERVICE_HOST: '<API server host>'
  KUBERNETES_SERVICE_PORT: '<API server port>'
```

Address choice: a load balancer for HA kubeadm; a stable DNS name or static IP for a single control plane node (a dynamic IP breaks on restart); the API load balancer FQDN on kOps, EKS and AKS (from `kubectl cluster-info`); `api-int.<cluster_name>.<base_domain>` on port 6443 for OpenShift; `proxy.local` port 6444 for MKE. Confirm by grepping a calico-node log for `KUBERNETES_SERVICE_HOST`.

**Disabling kube-proxy.** If it runs in IPVS mode, switch to iptables first. For DaemonSet kube-proxy:

```
kubectl patch ds -n kube-system kube-proxy -p '{"spec":{"template":{"spec":{"nodeSelector":{"non-calico": "true"}}}}}'
```

Not suitable for AKS with Azure CNI (the add-on manager reverts it). OpenShift: patch `networks.operator.openshift.io cluster` with `deployKubeProxy` false.

**If kube-proxy cannot be disabled**, set `bpfKubeProxyIptablesCleanupEnabled` to false (otherwise iptables rules flap) and `bpfKubeProxyHealthzPort` to `0` to avoid a port 10256 conflict, both on the default FelixConfiguration.

**MKE.** Set `vxlanPort` to 4790 before enabling eBPF, because Docker Swarm already holds UDP 4789.

## Checked

2026-11-08. The Enabling the eBPF data plane page was read in full. ConfigMap YAML, per-platform addresses, kube-proxy patches and Felix settings were confirmed on the Enabling the eBPF data plane page.

Method: documentation only; no commands were run.
