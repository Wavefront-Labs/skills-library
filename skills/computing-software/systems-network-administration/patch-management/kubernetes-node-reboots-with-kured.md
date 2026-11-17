---
id: computing-software.systems-network-administration.patch-management.kubernetes-node-reboots-with-kured
name: kubernetes-node-reboots-with-kured
category: computing-software
field: systems-network-administration
product: patch-management
tags: [kured, node-drain-reboot, rolling-patching, reboot-management, kubernetes, pod-disruption-budget]
level: practitioner
status: docs-checked
description: "Patch Kubernetes node OSes and reboot safely with kured: sentinel files, lock, reboot windows, drain behaviour with PodDisruptionBudgets, and alerting blockers."
sources:
  - https://kured.dev/docs/configuration/
  - https://github.com/kubereboot/charts/blob/main/charts/kured/values.yaml
  - https://kubernetes.io/docs/tasks/run-application/configure-pdb/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubernetes node reboots with kured

On self-managed or AKS-style nodes where unattended-upgrades/dnf-automatic installs OS
updates, someone must reboot nodes one at a time. **kured** (KUbernetes REboot Daemon) does:
watch for a sentinel, take a cluster-wide lock, cordon + drain, reboot, uncordon.

## Install (Helm)
```sh
helm repo add kubereboot https://kubereboot.github.io/charts
helm install kured kubereboot/kured -n kube-system \
  --set configuration.rebootDays="{mo,tu,we,th}" \
  --set configuration.startTime="02:00" --set configuration.endTime="05:00" \
  --set configuration.timeZone="Europe/London" \
  --set configuration.period="1h" \
  --set configuration.drainTimeout="15m" \
  --set configuration.notifyUrl="slack://tokenA/tokenB/tokenC"
```
Key options: `rebootSentinel` (default `/var/run/reboot-required`, Debian/Ubuntu),
`rebootSentinelCommand` (a zero exit status triggers a reboot and the sentinel file is then ignored; for the RHEL family, `needs-restarting -r` exits 1 when a reboot is needed, so negate it, for example `sh -c "! needs-restarting --reboothint"`),
`period` (check interval, default 1h), `concurrency` (default 1), `blockingPodSelector` (don't reboot a node while matching pods, such as batch jobs, run on it),
`preferNoScheduleTaint` (disabled by default), `prometheusUrl` + `alertFilterRegexp` (skip reboots while alerts are active).

## Make drains succeed
- Every replicated app needs ≥ 2 replicas and a **PodDisruptionBudget**
  (`minAvailable: 1` or `maxUnavailable: 1`); single-replica deployments with PDB
  `minAvailable: 1` block drains forever (kured times out and retries).
- `drainTimeout` defaults to 0 (wait indefinitely); `forceReboot` (default false) would reboot even if the drain fails, so leave it off unless you accept the disruption.
- StatefulSets with quorum (etcd, Kafka, ZooKeeper) need PDBs matching quorum.

## Observe
```sh
kubectl -n kube-system logs ds/kured --tail=50
kubectl get nodes        # SchedulingDisabled during drain
kubectl -n kube-system get ds kured -o yaml    # lock annotation under metadata.annotations
```
Metric `kured_reboot_required` (per node, served on port 8080 by default) is a gauge for the presence of the sentinel: alert if it stays above 0 for more than N days (blocked).

## Gotchas
- On managed node pools, follow the provider's node image upgrade guidance instead of rebooting in place.
- Lock held by a node that died: the lock is recorded in a DaemonSet annotation (default `weave.works/kured-node-lock`); `lockTtl` expires it after a set time (default 0, disabled). Removing a stale annotation by hand is a recovery step: confirm the locking node is really gone first.

## Verify
After a patch night, `kured_reboot_required` back to 0 on all nodes, no app availability
alerts, nodes uncordoned.

## Checked

Checked 2026-10-27 against the kured documentation (configuration page) and the kured Helm chart values.
- Helm values `rebootDays`, `startTime`, `endTime` (schedule), `timeZone`, `period` (default 1h), `drainTimeout` (default 0), `notifyUrl`, `concurrency` (default 1), `blockingPodSelector`, `preferNoScheduleTaint`, `rebootSentinel` default `/var/run/reboot-required`: confirmed.
- `rebootSentinelCommand` semantics (zero return code triggers reboot): confirmed. Lock annotation default `weave.works/kured-node-lock`, `lockTtl`, `forceReboot`: confirmed.
- Metric `kured_reboot_required` on :8080: confirmed.
- Removed unconfirmed: the claim about drain flag equivalents and the one-line annotation removal command.
Method: documentation only; no commands were run.
