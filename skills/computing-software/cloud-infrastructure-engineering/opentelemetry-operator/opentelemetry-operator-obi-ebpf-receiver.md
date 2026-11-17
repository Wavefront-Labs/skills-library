---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-obi-ebpf-receiver
name: opentelemetry-operator-obi-ebpf-receiver
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, obi, ebpf, obi-receiver, unprivileged-capabilities, k8s-pod-labels]
level: advanced
status: docs-checked
description: "Run the OBI eBPF receiver in a DaemonSet Collector with hostPID, either privileged or with a minimal capability set, and select workloads by namespace and pod labels."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/use-cases/obi-ebpf-receiver.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# eBPF instrumentation with the OBI receiver

OBI (OpenTelemetry eBPF Instrumentation) instruments applications at the kernel level without code changes. Since collector contrib version 0.156.0 it is available as a Collector receiver, combining zero-code tracing with Collector processing such as tail sampling and filtering.

Collector CR: OBI needs a DaemonSet with `hostPID: true` and elevated privileges to load eBPF programs. The simple setup is `mode: daemonset`, a contrib image, a `serviceAccount`, `hostPID: true` and `securityContext` of `runAsUser: 0` plus `privileged: true`. The ServiceAccount needs a ClusterRole with list/watch on replicasets, pods, services and nodes. Receiver config:

```yaml
receivers:
  obi:
    discovery:
      instrument:
        - k8s_namespace: my-application
          k8s_pod_labels:
            obi.instrument: "true"
    attributes:
      kubernetes:
        enable: "true"
```

Unprivileged variant: drop ALL capabilities and add `BPF`, `SYS_PTRACE`, `NET_RAW`, `CHECKPOINT_RESTORE`, `DAC_READ_SEARCH`, `PERFMON`, with `readOnlyRootFilesystem: true`, an emptyDir at `/var/run/obi`, and a hostPath mount of `/sys/fs/cgroup`.

Selecting workloads: each `discovery.instrument` entry matches on all its fields (namespace plus pod labels), and `k8s_pod_annotations` can replace labels. Add the label to pod templates to opt in. `attributes.kubernetes.enable` adds `k8s.namespace.name`, `k8s.pod.name` and `service.name`, requiring list/watch on more workload kinds.

## Checked

2026-11-04. Confirmed against docs/use-cases/obi-ebpf-receiver.md: OBI included as a Collector receiver from contrib 0.156.0, the DaemonSet with `hostPID: true`, `runAsUser: 0` and `privileged: true`, the ClusterRole (replicasets, pods, services, nodes with list and watch), the receiver config, the unprivileged variant (drop ALL, the six added capabilities, `readOnlyRootFilesystem`, emptyDir `/var/run/obi`, hostPath `/sys/fs/cgroup`), namespace and pod label selection matching all fields, `k8s_pod_annotations` as an alternative, and the Kubernetes attribute enrichment with broader RBAC. Removed the closing security remark, which the page does not state.

Method: documentation only; no commands were run.
