---
id: computing-software.cloud-infrastructure-engineering.talos-linux.oom-handler-trigger-and-ranking
name: oom-handler-trigger-and-ranking
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [oomconfig, oom, cel, psi, cgroups, qos, triggerexpression, cgrouprankingexpression]
level: sme
status: docs-checked
description: "How the Talos userspace OOM handler decides: PSI-based triggerExpression defaults, QoS cgroup classes, ranking formula, strict class ordering, and which pods are killable."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/configure-your-talos-cluster/system-configuration/oom.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Since Talos v1.12 a userspace OOM controller runs inside `machined`, enabled by default, configured through CEL expressions in `OOMConfig`. It reacts to memory pressure (PSI stall time), well before the kernel OOM killer, which stays enabled alongside it. It is disabled when Talos itself runs in a container (Docker provisioner).

Each `sampleInterval` (default 500ms): collect PSI per QoS class, evaluate `triggerExpression`, score cgroups with `cgroupRankingExpression`, pick one victim, `SIGKILL` the whole cgroup via `cgroup.kill` and call `process_mrelease`. At most one cgroup dies per cycle. Classes from least to most important: `Besteffort`, `Burstable`, `Guaranteed`, `Podruntime` (containerd, kubelet, etcd), `System` (Talos services). Candidates are immediate children, so a whole pod or a single service.

Default trigger (it watches only System and Podruntime pressure, to keep the node manageable):

```cel
multiply_qos_vectors(d_qos_memory_full_total, {System: 8.0, Podruntime: 4.0}) > 3000.0 &&
multiply_qos_vectors(qos_memory_full_avg10, {System: 1.0, Podruntime: 1.0}) > 5.0 &&
time_since_trigger > duration("5s")
```

The `d_` prefix gives per-second derivatives. Talos 1.14 dropped the clause on whole-machine `memory_full_avg10 > 75.0` because a memory-limited, I/O-heavy pod caused false triggers.

Default ranking (score 0 means never killed):

```cel
memory_max.hasValue() ? 0.0 :
{Besteffort: 1.0, Burstable: 0.5, Guaranteed: 0.0, Podruntime: 0.0, System: 0.0}[class] *
double(memory_current.orValue(0u))
```

`strictCgroupClassOrdering` (default true) picks the least important class with any eligible cgroup first, then the top score inside it. Outcome: BestEffort pods die first; Burstable pods only if the pod cgroup has no memory limit; Guaranteed pods, limited Burstable pods, and Talos and runtime services are never killed. The kubelet limits the pod cgroup only when every container, including init containers, sets `resources.limits.memory`.

## Checked

2026-11-04. Sample cycle, class table, default expressions, strict ordering and pod outcome table confirmed on the OOM Handler page.

Method: documentation only; no commands were run.
