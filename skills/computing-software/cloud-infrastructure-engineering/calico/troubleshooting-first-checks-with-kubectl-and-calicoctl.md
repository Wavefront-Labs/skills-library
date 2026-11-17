---
id: computing-software.cloud-infrastructure-engineering.calico.troubleshooting-first-checks-with-kubectl-and-calicoctl
name: troubleshooting-first-checks-with-kubectl-and-calicoctl
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [troubleshooting, kubectl, tigerastatus, calicoctl, diags, calico-node, cni, operator]
level: intro
status: docs-checked
description: "A first-pass checklist for a sick Calico cluster: node and pod state, tigerastatus, CNI config, calicoctl version match, Installation spec, and calicoctl node diags."
sources:
  - https://docs.tigera.io/calico/latest/operations/troubleshoot/commands
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use `calico-system` as the namespace for operator installs and `kube-system` for manifest installs.

1. **Nodes and agents.** `kubectl get nodes`, then `kubectl get pods -n calico-system -o wide` to see a calico-node pod Ready on every node.
2. **Operator health.** `kubectl get tigerastatus` shows the `calico` component Available True, Progressing False, Degraded False when healthy. `kubectl get pod -n tigera-operator` checks the operator pod.
3. **Installation parameters.** `kubectl get installation -o yaml` shows the effective `calicoNetwork` settings: ipPools, encapsulation, `nodeAddressAutodetectionV4`, and `cni.type`/`cni.ipam.type`.
4. **CNI config on a node.** `cat /etc/cni/net.d/10-calico.conflist`.
5. **Version match.** The cluster version and type must match your calicoctl; check with `calicoctl version`.
6. **Other system pods.** `kubectl get pod -n kube-system -o wide`. If coredns pods get no IP, suspect the CNI; if other pods fail, it is probably ordinary Kubernetes trouble. Also check `systemctl status kubelet` and `journalctl -u kubelet | head`.
7. **Test from inside.** Run a pod from `praqma/network-multitool`, then `kubectl exec -it multitool -- bash` and use ping, `curl -I -k https://kubernetes` (a 403 means the API server answered) and `nslookup`.
8. **Diagnostics bundle.** `sudo calicoctl node diags` dumps netstat, routes, interfaces and iptables to a tar.gz in a temp directory.

For pod detail use `kubectl describe pods <pod_name> -n <namespace>` and `kubectl logs <pod_name> -n <namespace>`.

## Checked

2026-11-08. The Troubleshooting commands page was read in full. Each command and the expected healthy tigerastatus line were confirmed on the Troubleshooting commands page.

Method: documentation only; no commands were run.
