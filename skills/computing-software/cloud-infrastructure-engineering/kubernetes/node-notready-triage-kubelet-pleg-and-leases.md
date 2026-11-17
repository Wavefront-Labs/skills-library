---
id: computing-software.cloud-infrastructure-engineering.kubernetes.node-notready-triage-kubelet-pleg-and-leases
name: node-notready-triage-kubelet-pleg-and-leases
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, node-notready, journalctl-kubelet, kubelet-restart, pleg, pleg-not-healthy, node-lease, node-monitor-grace-period, cka]
level: practitioner
status: docs-checked
description: "Triage NotReady nodes: kubelet service state and journal, 'PLEG is not healthy' runtime problems, node Lease heartbeats and node-monitor-grace-period."
sources: ["https://kubernetes.io/docs/concepts/architecture/nodes/#node-heartbeats", "https://kubernetes.io/docs/reference/node/node-status/", "https://kubernetes.io/docs/tasks/debug/debug-cluster/", "https://kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/#feature-gates-for-alpha-or-beta-features"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NotReady node triage: kubelet, PLEG, leases

## How Ready is decided
The kubelet renews a **Lease** in `kube-node-lease` every 10s (`nodeLeaseDurationSeconds` 40)
and updates `NodeStatus` on change or every 5 min. The node lifecycle controller marks the node
`Unknown` when no heartbeat arrives within `--node-monitor-grace-period` (default 50s), taints it `node.kubernetes.io/unreachable`, and pods are evicted after their
`tolerationSeconds` (default 300s). The kubelet itself reports `Ready=False` for runtime/network
problems.

```bash
kubectl get nodes; kubectl describe node <n> | sed -n '/Conditions/,/Addresses/p'
kubectl -n kube-node-lease get lease <n> -o jsonpath='{.spec.renewTime}'
```
`Ready Unknown "Kubelet stopped posting node status"` → kubelet down or can't reach API.
`Ready False` + message → kubelet is up and telling you why (PLEG, CNI not ready, runtime down).

## On the node
```bash
systemctl status kubelet containerd
journalctl -u kubelet --since "30 min ago" --no-pager | tail -100
journalctl -u kubelet | grep -E "PLEG|certificate|connection refused|x509|Unauthorized|NetworkReady"
crictl ps -a | head; crictl info | jq .status.conditions
df -h /var /var/lib/kubelet; free -m; uptime
```
| Journal line | Cause |
|---|---|
| `x509: certificate has expired` / `Unauthorized` | kubelet client cert expired (rotation off or CSR not approved) |
| `dial tcp <api>:6443: connect: connection refused` | API/LB down or firewall |
| `container runtime is down` / `PLEG is not healthy: pleg was last seen active ... ago; threshold is 3m0s` | runtime hung or overloaded |
| runtime network not ready (kubelet runtime condition `NetworkReady` false) | CNI not installed or not running on the node |
| kubelet refuses to start with swap enabled (`failSwapOn` defaults to true) | node config drift |

## PLEG (Pod Lifecycle Event Generator)
The generic PLEG relists containers via CRI every second. If no relist has completed for 3 minutes
the PLEG health check fails and the node goes NotReady.
Causes: container runtime hung or slow (stuck mount, storage I/O), too many containers/pods,
slow disk. Check `crictl ps` latency; `time crictl pods`. Fix: restart the runtime, reduce pod
density, faster disk. The `EventedPLEG` feature gate (alpha, off by default, needs runtime
support) can reduce relist load.

## Recovery
```bash
systemctl restart containerd && systemctl restart kubelet      # a kubelet restart leaves running Pods in place
```
If the node is unrecoverable: cordon/drain (pods will already be evicted after 5 min), replace it,
`kubectl delete node <n>`. For stateful pods stuck Terminating on a dead node, see the
out-of-service taint (non-graceful node shutdown).

## Verify
- [ ] Node Ready, lease renewTime recent (the kubelet renews about every 10s by default); no PLEG lines after restart.

## Checked

Date: 2026-10-27. Documentation release: Kubernetes v1.37.1 (latest release; website main is the v1.38 development tree).

- Lease and status heartbeat defaults (lease duration 40s, status report every 5 min, status update 10s) and the
  `node-monitor-grace-period` default of 50s: kubelet and node lifecycle controller defaults in the v1.37.1 source,
  node-status reference page.
- PLEG relist period (1s) and unhealthy threshold (3 min): kubelet source v1.37.1.
- `EventedPLEG` is alpha, default off: feature-gate listing and v1.37.1 `kube_features.go`.
- Default tolerationSeconds 300 for not-ready and unreachable: DefaultTolerationSeconds admission plugin source.
- Removed: the `NetworkPluginNotReady` message text and the "restart containerd keeps containers running" claim, which
  no documentation covers.

Method: documentation only; no commands were run.
