---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cpu-manager-and-topology-manager
name: cpu-manager-and-topology-manager
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubelet, cpu-manager, static-cpu-policy, topology-manager, memory-manager, numa, latency-sensitive, cpu-pinning]
level: advanced
status: docs-checked
description: "Pin exclusive CPUs for latency-critical pods with the static CPU Manager policy, align CPU/device/memory to NUMA with Topology Manager, and switch policies safely."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/cpu-management-policies/", "https://kubernetes.io/docs/tasks/administer-cluster/topology-manager/", "https://kubernetes.io/docs/tasks/administer-cluster/memory-manager/", "https://kubernetes.io/docs/reference/config-api/kubelet-config.v1beta1/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CPU Manager and Topology Manager

## When
Telco/DPDK, trading, real-time audio, some databases: workloads that suffer from CFS quota
throttling and cross-NUMA memory access. Not worth it for typical web services.

## CPU Manager static policy
```yaml
cpuManagerPolicy: static
reservedSystemCPUs: "0,1"          # or kubeReserved/systemReserved cpu; a reservation above zero is required
cpuManagerPolicyOptions:
  full-pcpus-only: "true"          # allocate whole physical cores (GA, visible by default from 1.33)
cpuManagerReconcilePeriod: 10s     # default
```
A container gets **exclusive** CPUs only if the pod is **Guaranteed** and the container's
CPU request is an **integer** (`requests.cpu == limits.cpu == 4`). Everyone else, including Guaranteed
containers with fractional requests, shares the remaining pool. The kubelet refuses the static policy with
a zero CPU reservation, because the shared pool could become empty. `reservedSystemCPUs` takes precedence over
`kubeReserved`/`systemReserved`.

## Topology Manager
Aligns CPU (CPU Manager), devices (device plugins, e.g. GPUs/SR-IOV NICs) and memory to the
same NUMA node:
```yaml
topologyManagerPolicy: single-numa-node   # none | best-effort | restricted | single-numa-node
topologyManagerScope: pod                 # container (default) | pod
memoryManagerPolicy: Static               # optional: NUMA-pinned memory for Guaranteed pods
reservedMemory:
- {numaNode: 0, limits: {memory: 1100Mi}}
```
`restricted`/`single-numa-node` **reject** pods that cannot be aligned: the pod ends in `Terminated` with a pod
admission failure (a "Topology Affinity" error). The scheduler is not topology-aware, so the pod can be placed on a
node and then fail there, and it does not reschedule a Terminated pod; use a Deployment or similar to trigger a
replacement. The Topology Manager is also not aware of NUMA distances by default.

## Switching policy on a node
1. Drain the node.
2. Stop kubelet, change config, **delete `/var/lib/kubelet/cpu_manager_state`**, start kubelet. Otherwise the kubelet
   crash-loops with `could not restore state from checkpoint ... configured policy "static" differs from state checkpoint policy "none"`.
   The same reset is needed if the set of online CPUs changes, or when you change the policy options.
3. Uncordon.
Do it per node pool; label pools (`cpu-policy=static`) and target latency pods there.

## Check
```bash
cat /var/lib/kubelet/cpu_manager_state      # on the node: the CPU Manager checkpoint
```

## Gotchas
- Fractional requests (3500m) get the shared pool, not exclusive CPUs; enforce integer requests with an admission policy on that pool.
- Only Guaranteed pods qualify; a Burstable or BestEffort pod never gets exclusive CPUs.

## Verify
- [ ] `cpu_manager_state` lists dedicated CPU sets for the Guaranteed integer-CPU containers.
- [ ] No pods with a Topology Affinity admission failure on single-numa-node pools.

## Checked

2026-10-26: kubernetes.io CPU management policies, Topology Manager and Memory Manager task pages (v1.37 docs, kubernetes/website main 2026-10-25) and the kubelet config API source. Confirmed: exclusive CPUs only for Guaranteed pods with integer requests, nonzero reservation requirement, reservedSystemCPUs precedence, full-pcpus-only GA 1.33, reconcile period default 10s, state-file reset and the checkpoint error text, topology policies and scopes with defaults, Static memory policy needing reservedMemory, rejected pods ending Terminated and not being rescheduled, scheduler not topology-aware. Removed the unconfirmed CFS-throttling, NUMA-aware scheduler, init container, HPA/VPA and memory_manager_state remarks and host command checks.

Method: documentation only; no commands were run.
