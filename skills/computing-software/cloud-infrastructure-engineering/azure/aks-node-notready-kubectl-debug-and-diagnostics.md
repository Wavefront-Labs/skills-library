---
id: computing-software.cloud-infrastructure-engineering.azure.aks-node-notready-kubectl-debug-and-diagnostics
name: aks-node-notready-kubectl-debug-and-diagnostics
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, aks, node-not-ready, kubectl-debug, aks-diagnose, check-network-outbound, troubleshooting]
level: advanced
status: docs-checked
description: "Troubleshoot AKS nodes: NotReady and pressure conditions, kubectl debug node with chroot, kubelet logs, outbound checks, auto-repair and reimaging a bad node."
sources: ["https://learn.microsoft.com/troubleshoot/azure/azure-kubernetes/availability-performance/node-not-ready-basic-troubleshooting", "https://learn.microsoft.com/azure/aks/node-access", "https://learn.microsoft.com/azure/aks/node-auto-repair"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AKS node NotReady and node debugging

**Goal:** find out why a node is NotReady (or evicting pods) and fix or replace it.

## Triage
```bash
kubectl get nodes -o wide
kubectl describe node aks-user1-12345678-vmss000003   # Conditions, Events, Allocated resources
kubectl get events -A --sort-by=.lastTimestamp | tail -40
```
Conditions: `Ready=False/Unknown` (kubelet not reporting), `MemoryPressure`, `DiskPressure`, `PIDPressure`,
`NetworkUnavailable`.

## Get a shell on the node
```bash
kubectl debug node/aks-user1-12345678-vmss000003 -it --image=mcr.microsoft.com/azurelinux/busybox:1.36
# inside the debug pod:
chroot /host
systemctl status kubelet containerd
journalctl -u kubelet --since "30 min ago" | tail -100
df -h /var/lib/containerd ; free -m
```
`kubectl debug` runs a privileged container on the node; remove the debug pod afterwards (`kubectl delete pod node-debugger-...`). If the node is too broken for pods, the node access article also describes connecting through the AKS ARM API.

## Common causes
| Cause | Signal | Fix |
|---|---|---|
| Egress blocked to required endpoints | kubelet can't reach API server/MCR | Compare firewall/UDR rules with the AKS outbound rules article |
| Disk full (images/logs) | DiskPressure, evictions | Larger OS disk, ephemeral OS, image cleaner, log rotation |
| Memory exhaustion | MemoryPressure, OOM kills | Requests/limits, bigger SKU, fewer pods per node |
| Too many pods/PIDs | PIDPressure | Fix fork-bombing workload, max pods setting |
| Platform/VM issue | Node Unknown, VM unhealthy | Auto-repair, reimage, redeploy |

## Repair
- AKS **node auto-repair** acts on a node that reports NotReady on consecutive checks within 10 minutes, or reports no status for 10 minutes, and stays unhealthy for at least five minutes: it reboots, then reimages, then (Linux only) redeploys, retrying the sequence up to three times (up to about one hour overall). It is best-effort; events such as `NodeRebootStart` and `NodeReimageStart` record each action.
- Manual: cordon and drain, then reimage/delete the VMSS instance:
```bash
kubectl cordon <node>; kubectl drain <node> --ignore-daemonsets --delete-emptydir-data
az aks nodepool delete-machines -g rg --cluster-name aks01 -n user1 --machine-names <node>
```

## Verify
- [ ] Node Ready, no pressure conditions; root cause recorded and addressed (rule, disk size, limits).

## Checked
Date: 2026-10-24. Checked against MicrosoftDocs/azure-aks-docs (node-access, node-auto-repair; main branch) and the Azure CLI `acs` help (`az aks nodepool delete-machines --machine-names`).
- Confirmed: `kubectl debug node/<node> -it --image=mcr.microsoft.com/azurelinux/busybox:1.36` then `chroot /host`; auto-repair triggers, reboot-reimage-redeploy sequence, three retries, one-hour bound, event names; `az aks nodepool delete-machines`.
- Removed as unconfirmed: `az aks check-network outbound`, `az vmss run-command invoke` as a fallback, and the portal detector remark.
Method: documentation only; no commands were run.
