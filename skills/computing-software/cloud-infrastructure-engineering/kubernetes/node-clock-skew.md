---
id: computing-software.cloud-infrastructure-engineering.kubernetes.node-clock-skew
name: node-clock-skew
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, troubleshoot-nodes, node-clock-skew, chrony, certificates, etcd]
level: practitioner
status: docs-checked
description: "Detect and fix clock skew on nodes: chrony checks, symptoms (x509 not yet valid, token used before issued, etcd clock warnings, CronJob drift)."
sources: ["https://etcd.io/docs/latest/op-guide/monitoring/", "https://chrony-project.org/doc/4.6.1/chronyc.html", "https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/#time-zones", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configure-ec2-ntp.html", "https://cloud.google.com/compute/docs/instances/configure-ntp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node clock skew

## Symptoms
| Where | Message |
|---|---|
| kubelet joining or rotating certs | `x509: certificate has expired or is not yet valid` |
| ServiceAccount / OIDC tokens | tokens rejected as not yet valid or already expired |
| etcd | `prober found high clock drift` (logged when the measured difference to a peer is above 1 s) |
| CronJobs without `.spec.timeZone` | schedules are read in the kube-controller-manager's local time zone |
| Logs and traces | events out of order across nodes |

## Check
```bash
timedatectl
chronyc tracking
chronyc sources -v
date -u; ssh other-node date -u
```
Across nodes quickly:
```bash
kubectl get nodes -o name | cut -d/ -f2 | xargs -I{} ssh {} 'echo {} $(date +%s.%N)'
```

## Fix
- Run a time sync service (chrony or systemd-timesyncd) on every node, pointing at reliable sources
  (cloud provider time service: `169.254.169.123` on AWS, `metadata.google.internal` on GCP).
- `chronyc makestep` to step the clock immediately when far off.
- After fixing, restart kubelet on nodes that failed TLS bootstrap; re-issue tokens if needed.

## Monitor
node-exporter: `node_timex_offset_seconds` and `node_timex_sync_status`:
```yaml
- alert: NodeClockSkew
  expr: abs(node_timex_offset_seconds) > 0.05
  for: 10m
```

## Checked

Date: 2026-10-27. Documentation release: Kubernetes v1.37.1 (latest release; website main is the v1.38 development tree).

- etcd `prober found high clock drift` message and its 1 s threshold: etcd `rafthttp/probing_status.go` (main branch).
- `node_timex_offset_seconds` and `node_timex_sync_status` metric names: node_exporter `timex` collector source.
- CronJob schedule time zone behaviour: CronJob concept page.
- `chronyc tracking`, `chronyc sources -v` and `makestep`: chronyc reference (chrony 4.6.1).
- AWS `169.254.169.123` and GCE `metadata.google.internal` time sources: AWS and Google Cloud NTP pages.
- Removed: `token used before issued` message text, the second etcd message, hypervisor-sync advice and the example
  `timedatectl` output, which no checked documentation covers.

Method: documentation only; no commands were run.
