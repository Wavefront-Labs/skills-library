---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cpu-limits-policy
name: cpu-limits-policy
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cpu-limits-debate, requests-only, cfs-throttling, cpu-quota, qos-class, resource-policy]
level: advanced
status: docs-checked
description: "Decide a CPU limits policy: requests-only vs limits, CFS throttling mechanics, when limits are required (Guaranteed QoS, pinning, tenancy) and measuring throttling."
sources: ["https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/", "https://kubernetes.io/docs/tasks/administer-cluster/cpu-management-policies/", "https://github.com/google/cadvisor/blob/master/docs/storage/prometheus.md", "https://docs.kernel.org/admin-guide/cgroup-v2.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CPU limits policy: requests-only or limits?

## Mechanics
- **CPU request** → CPU shares (converted to `cpu.weight` on cgroup v2) in the kubelet: proportional
  share under contention, and the scheduler's placement budget. It does not throttle.
- **CPU limit** → CFS quota per period (the kubelet's default period is 100 ms): when a container
  approaches its limit the kernel restricts its CPU (the docs: "cpu limits are enforced by CPU
  throttling"). A multi-threaded app can use up its quota early in a period and then wait for the
  next one even if the node is idle: latency spikes with low average CPU.

## The default recommendation for most services: requests, no CPU limits
- Requests guarantee each pod its share under contention; idle CPU is used by whoever needs it.
- Removes throttling-induced p99 latency and probe timeouts.
- Requires **accurate requests** (right-sizing), otherwise noisy neighbours get more than fair.

## When to set CPU limits
- **Guaranteed QoS** needed (limits == requests for CPU and memory): the static CPU Manager policy
  gives exclusive cores only to Guaranteed pods with integer CPU requests.
- **Multi-tenant** clusters where tenants pay for what they request and must not consume
  others' idle CPU; or a LimitRange/quota policy that demands limits (`limits.cpu` quota).
- **Benchmarking/predictability**: same performance regardless of node idleness.
- Batch jobs that would otherwise starve the node's system daemons (also fix with reservations).
If you set CPU limits, leave room above the request for bursty services, and keep memory limits
regardless (memory is not compressible).

## Measure throttling
```promql
sum by (namespace,pod,container) (rate(container_cpu_cfs_throttled_periods_total[5m]))
/ sum by (namespace,pod,container) (rate(container_cpu_cfs_periods_total[5m]))
```
Both metrics are exported by cAdvisor. Inside the container, cgroup v2 `cpu.stat` reports `nr_periods`,
`nr_throttled` and `throttled_usec`. Alert on sustained high ratios for latency-sensitive workloads.

## Policy as code
- An admission policy can require `requests.cpu` and `limits.memory`; don't require `limits.cpu`
  unless a tenancy rule says so.
- A ResourceQuota on `limits.cpu` rejects pods that do not set a CPU limit — drop it from quotas if
  adopting requests-only.

## Gotchas
- Runtimes that size thread pools from the visible CPU count may see all node cores when no limit is
  set; check how your runtime detects CPUs and set its processor count explicitly if needed.

## Verify
- [ ] Throttling ratio is low for latency-sensitive workloads; policy documented and enforced.

## Checked
2026-10-23, against the Kubernetes website resource-management page (cpu limits enforced by throttling, quota on limits requires limits), the kubelet cgroup helper source (requests to shares and cpu.weight, quota with 100000 microsecond default period), the cAdvisor Prometheus metrics list (container_cpu_cfs_periods_total, container_cpu_cfs_throttled_periods_total), the Linux cgroup-v2 documentation (cpu.stat fields) and the CPU management policies page (static policy). The kernel 5.4 bug, runtime flags, the 2-4x rule and numeric thresholds were removed as unconfirmed.
Method: documentation only; no commands were run.
