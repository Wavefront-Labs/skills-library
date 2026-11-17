---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-collector-privileged-pod-security
name: opentelemetry-operator-collector-privileged-pod-security
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, hostpath, hostnetwork, hostpid, privileged, rbac-equivalence, pod-security]
level: advanced
status: docs-checked
description: "Understand that creating an OpenTelemetryCollector grants whatever hostPath, hostNetwork, hostPID and privileged settings it contains, with no operator-side filtering."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/collector/security.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Privileged pod fields in the Collector spec

The operator copies host-level pod settings from the `OpenTelemetryCollector` spec into the generated workload verbatim. It applies no security filtering, and the validating webhook does not inspect them. Both `v1alpha1` and `v1beta1` expose them. Treat `create` on `opentelemetrycollectors.opentelemetry.io` as equivalent to `create` on `daemonsets.apps`: in `mode: daemonset` it can mean root on every node.

Fields that grant power:
- `spec.volumes` with `hostPath`: read/write to any node path.
- `spec.hostNetwork`: the node network namespace, including loopback-only services.
- `spec.hostPID`: visibility of every process on the node.
- `spec.securityContext`: `privileged`, extra capabilities, `runAsUser: 0`.
- `spec.podSecurityContext`: UID/GID, sysctls, `fsGroup`.
- `spec.initContainers` and `spec.additionalContainers`: arbitrary images and commands.
- `spec.serviceAccount`: runs with an existing ServiceAccount token.
- `spec.tolerations`, `nodeSelector`, `affinity`: placement on control-plane or restricted nodes.

Why they exist: `filelog` reads container logs from `/var/log/pods` (hostPath), `hostmetrics` needs `/proc` and `/sys` and `hostPID` to attribute processes, eBPF components need `/sys/fs/cgroup` plus capabilities such as BPF, PERFMON and SYS_PTRACE, and receivers binding node ports such as statsd need `hostNetwork`. Rejecting them by default would break the primary use case, so running with them is normal; the control is deciding who may create these resources.

## Checked

2026-11-04. Confirmed against docs/collector/security.md: fields copied verbatim with no operator filtering and no webhook inspection, the field table (volumes hostPath, hostNetwork, hostPID, securityContext, podSecurityContext, initContainers and additionalContainers, serviceAccount, tolerations, nodeSelector, affinity), both API versions, the create-equals-daemonsets equivalence and the reasons (filelog, hostmetrics, eBPF capabilities, statsd). Nothing removed.

Method: documentation only; no commands were run.
