---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubelet-graceful-node-shutdown
name: kubelet-graceful-node-shutdown
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubelet, graceful-node-shutdown, shutdowngraceperiod, systemd-inhibitor, non-graceful-shutdown, out-of-service-taint]
level: advanced
status: docs-checked
description: "Configure kubelet graceful node shutdown (shutdownGracePeriod, critical pods, priority-based periods) via systemd inhibitor locks, and use the out-of-service taint for non-graceful cases."
sources: ["https://kubernetes.io/docs/concepts/cluster-administration/node-shutdown/", "https://github.com/kubernetes/kubernetes/blob/master/pkg/kubelet/nodeshutdown/nodeshutdown_manager_linux.go", "https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/kubelet/config/v1beta1/types.go", "https://www.freedesktop.org/software/systemd/man/latest/logind.conf.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubelet graceful node shutdown

Without it, an OS shutdown/reboot (patching, spot reclaim, `shutdown -r`) kills containers
with no preStop, no SIGTERM grace, and pods stay "Running" in the API until the node is marked
NotReady.

## Configure
On Linux the feature gates `GracefulNodeShutdown` (beta, on by default since 1.21) and
`GracefulNodeShutdownBasedOnPodPriority` (beta, on by default since 1.24) apply.
```yaml
# KubeletConfiguration
shutdownGracePeriod: 60s                 # total delay the kubelet requests from systemd
shutdownGracePeriodCriticalPods: 15s     # portion reserved for system-*-critical pods (terminated last)
```
Or by priority (more control; the field must be empty if either of the two above is set):
```yaml
shutdownGracePeriodByPodPriority:
- {priority: 2000000000, shutdownGracePeriodSeconds: 15}   # system-critical
- {priority: 10000,      shutdownGracePeriodSeconds: 30}   # business-critical
- {priority: 0,          shutdownGracePeriodSeconds: 15}   # everything else
```
The kubelet registers a **systemd inhibitor lock** (delay mode) and on shutdown: marks node
NotReady (`reason: node is shutting down`), terminates regular pods, then critical pods. Pods it
terminated show status `Terminated` (message "Pod was terminated in response to imminent node shutdown.") and
controllers recreate them elsewhere. Both settings default to zero, which leaves the feature off, so set
both to non-zero values. The kubelet also rejects new pods at admission while a shutdown is in progress,
and emits `graceful_shutdown_start_time_seconds` and `graceful_shutdown_end_time_seconds`.

## Prerequisite: logind's max delay
systemd caps inhibitor delays with `InhibitDelayMaxSec` in `logind.conf` (default 5 seconds). In the
current kubelet source, when the requested grace period is larger than logind's value the kubelet asks
logind over D-Bus to raise it, reloads logind configuration and polls for the change; if logind still
reports a smaller value the shutdown manager fails to start ("timed out ... waiting for logind
InhibitDelayMaxSec to update"). So you normally do not need to edit `logind.conf` yourself.

Debian's `unattended-upgrades` default configuration conflicts with this when `shutdownGracePeriod` is
over 30 seconds: make `/etc/systemd/logind.conf.d/unattended-upgrades-logind-maxdelay.conf` a symbolic link
to `/dev/null`.

## Non-graceful shutdown (node died, no notice)
Pods of StatefulSets stay Terminating and RWO volumes stay attached. Once you **know** the node
is down (powered off), taint it:
```bash
kubectl taint node worker-7 node.kubernetes.io/out-of-service=nodeshutdown:NoExecute
```
(`NoExecute` or `NoSchedule` both work.) Pods without a matching toleration are force-deleted and their
volumes detached immediately, letting StatefulSet pods start elsewhere (feature gate
`NodeOutOfServiceVolumeDetach`, stable and on from 1.28). Verify the node is shut down or powered off, not
restarting, before tainting it, and remove the taint yourself once the pods have moved and the node is
recovered.

## Verify
- [ ] `sudo systemctl reboot` on a test node: pods show status `Terminated` with the shutdown message, preStop hooks ran, replacements scheduled before the node returns.

## Checked

2026-10-26: kubernetes.io node-shutdown page (v1.37 docs, kubernetes/website main 2026-10-25), the kubelet config API source (staging types.go, main), kubelet nodeshutdown manager source (main), the feature-gate pages and the systemd logind.conf manual source. Confirmed: zero defaults, the priority field being exclusive with the two period fields, node NotReady reason, Terminated status text, shutdown metric names, out-of-service taint and gate stages, logind default of 5 seconds. Corrected: the kubelet raises InhibitDelayMaxSec itself (the old skill said it silently uses the smaller value); removed the unconfirmed Failed phase and the inhibitor grep checks.

Method: documentation only; no commands were run.
