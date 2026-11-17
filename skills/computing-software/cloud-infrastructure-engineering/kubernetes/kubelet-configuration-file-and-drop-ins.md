---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubelet-configuration-file-and-drop-ins
name: kubelet-configuration-file-and-drop-ins
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubelet, kubeletconfiguration, kubelet-config-file, kubelet-drop-in, kubeadm, node-configuration]
level: practitioner
status: docs-checked
description: "Change kubelet settings the supported way: KubeletConfiguration file, the config.d drop-in directory, kubeadm's kubelet-config ConfigMap and patches, and verifying via configz."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/", "https://kubernetes.io/docs/reference/node/kubelet-config-directory-merging/", "https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/kubelet-integration/", "https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/control-plane-flags/", "https://kubernetes.io/docs/tasks/administer-cluster/cpu-management-policies/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KubeletConfiguration file and drop-ins

Most kubelet flags are deprecated in favour of the config file. Where things live on a
kubeadm node:
| File | Owner |
|---|---|
| `/var/lib/kubelet/config.yaml` | KubeletConfiguration, written by kubeadm from the `kubelet-config` ConfigMap |
| `/var/lib/kubelet/kubeadm-flags.env` | per-node flags kubeadm detected (`--node-ip`, `--container-runtime-endpoint`) |
| `/etc/default/kubelet` (`/etc/sysconfig/kubelet`) | `KUBELET_EXTRA_ARGS` — yours |
| `/usr/lib/systemd/system/kubelet.service.d/10-kubeadm.conf` | systemd drop-in wiring it together (written by the kubeadm package) |

## Drop-in config directory (alpha 1.28, beta 1.30, stable 1.35)
The kubelet looks for drop-ins nowhere by default: you must pass a path, for example
`--config-dir=/etc/kubernetes/kubelet.conf.d`. (On v1.28 to v1.29 you also had to set the
environment variable `KUBELET_CONFIG_DROPIN_DIR_ALPHA`.) Only files ending in `.conf` count; they are
processed in alphanumeric order of the whole file name, after the main file, and each must carry
`apiVersion` and `kind`. Use this for per-node-pool overrides managed by config management
instead of editing config.yaml.
```yaml
# /etc/kubernetes/kubelet.conf.d/50-reserved.conf
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
systemReserved: {cpu: 500m, memory: 1Gi}
```
Merge semantics: embedded structures merge field by field, lists are replaced whole. Precedence, highest
first: command-line flags (other than feature gates), drop-ins in sort order, the config file, then feature
gates given on the command line.

## Cluster-wide change with kubeadm
```bash
kubectl -n kube-system edit cm kubelet-config         # source of truth for new/upgraded nodes
# on each node (drain first if the change is disruptive):
kubeadm upgrade node phase kubelet-config
systemctl restart kubelet
```
Per-node differences: set `patches.directory` in `JoinConfiguration` (or `InitConfiguration`) and put a
file named `kubeletconfiguration+strategic.yaml` (target, optional suffix, patch type, extension) in it;
provide the same patches again when you run `kubeadm upgrade`. kubeadm writes
`/var/lib/kubelet/config.yaml` from the `kubelet-config` ConfigMap on join, so keep changes in the
ConfigMap, patches or drop-ins rather than hand edits.

## Verify the running config
```bash
kubectl get --raw "/api/v1/nodes/<node>/proxy/configz" | jq .kubeletconfig
journalctl -u kubelet -b
```

## Gotchas
- Some settings need a drain + pod restart to take effect (cpuManagerPolicy requires removing
  `/var/lib/kubelet/cpu_manager_state`).

## Verify
- [ ] `configz` on a sample node per pool shows the intended values.
- [ ] Config is in the ConfigMap/drop-in source, not hand-edited on one node.

## Checked

2026-10-26: kubernetes.io docs for v1.37 (kubernetes/website main, 2026-10-25) and the v1.35 blog post on the drop-in directory. Confirmed: --config-dir must be set explicitly, .conf suffix, sort order, merge precedence, alpha/beta/GA versions (1.28/1.30/1.35), kubeadm kubelet-config ConfigMap, kubeadm-flags.env, 10-kubeadm.conf location, patch target and file naming, drain plus cpu_manager_state removal. Removed unconfirmed managed-service flags and the log grep patterns.

Method: documentation only; no commands were run.
