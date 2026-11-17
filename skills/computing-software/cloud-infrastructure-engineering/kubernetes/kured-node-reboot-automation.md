---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kured-node-reboot-automation
name: kured-node-reboot-automation
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, node-hardening, kured, os-hardening, drain]
level: practitioner
status: docs-checked
description: "Automate OS patch reboots with kured: reboot sentinel, locking so one node reboots at a time, time windows, blocking pod selectors and Prometheus alert gates."
sources: ["https://kured.dev/docs/", "https://github.com/kubereboot/kured", "https://github.com/kubereboot/kured/blob/main/cmd/kured/main.go", "https://github.com/kubereboot/charts/blob/main/charts/kured/values.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kured (Kubernetes Reboot Daemon)

Unattended upgrades install kernel and libc patches but they take effect only after reboot.
kured reboots nodes safely, one at a time.

## How it works
DaemonSet checks for the sentinel: the file `/var/run/reboot-required` (`--reboot-sentinel`
default), or a command given with `--reboot-sentinel-command` whose zero exit code means a reboot
is needed. When a reboot is needed, it takes a cluster-wide lock (annotation on the DaemonSet),
cordons and drains the node, reboots, uncordons and releases the lock.

## Install
```bash
helm repo add kubereboot https://kubereboot.github.io/charts
helm install kured kubereboot/kured -n kube-system \
  --set configuration.period=1h \
  --set configuration.startTime=02:00 --set configuration.endTime=05:00 \
  --set configuration.timeZone=Europe/London \
  --set configuration.rebootDays='{mo,tu,we,th}' \
  --set configuration.prometheusUrl=http://prometheus.monitoring:9090 \
  --set configuration.alertFilterRegexp='^(RebootRequired|Watchdog)$' \
  --set configuration.blockingPodSelector='{app=critical-batch}'
```
- `prometheusUrl`: no reboot while any (non-filtered) alert is active; the flag `--alert-firing-only` ignores
  pending alerts.
- `blockingPodSelector`: no reboot while matching pods run on the node.
- `drainTimeout` (default 0, infinite) and `skipWaitForDeleteTimeout` handle stuck drains.
- `concurrency` (default 1) is the number of nodes rebooted at once.

## Observability
kured serves Prometheus metrics (default port 8080), including a per-node reboot-required gauge; alert
when nodes need reboots for more than a few days.

## Gotchas
- Managed node pools with node image upgrades (GKE, AKS node image auto-upgrade, Bottlerocket)
  may make kured unnecessary; do not run both.
- The kured DaemonSet manifest sets `hostPID: true` and a privileged container (to `nsenter` into
  the host); restrict its namespace accordingly.

## Verify
`touch /var/run/reboot-required` on a test node and watch it cordon, reboot and return within the window.

## Checked

Date: 2026-10-27. Documentation release: Kubernetes v1.37.1 (latest release; website main is the v1.38 development tree).

- Flags and defaults (`--reboot-sentinel` /var/run/reboot-required, `--reboot-sentinel-command` zero exit code, `--period`
  1h, `--concurrency` 1, `--drain-timeout` 0, `--blocking-pod-selector`, `--prometheus-url`, `--alert-firing-only`, metrics
  port 8080, lock annotation on the DaemonSet): `cmd/kured/main.go` on main (latest release 1.23.0).
- Helm values `configuration.*` names (`period`, `startTime`, `endTime`, `timeZone`, `rebootDays`, `prometheusUrl`,
  `alertFilterRegexp`, `blockingPodSelector`, `concurrency`): chart `values.yaml`.
- `hostPID: true` and `privileged: true` in the DaemonSet manifest: `kured-ds.yaml`.
- Removed: the `needs-restarting -r` example (its exit-code sense is not covered by kured documentation), the exact
  metric name and the claim that PDBs are respected, which the checked files do not state.

Method: documentation only; no commands were run.
