---
id: computing-software.ai-ml-engineering.ml-platform-engineering.kueue-quotas-and-gang-scheduling
name: kueue-quotas-and-gang-scheduling
category: computing-software
field: ai-ml-engineering
product: ml-platform-engineering
tags: [ml-platform, gpu, kueue, gang-scheduling, clusterqueue, localqueue, resource-quotas, kubernetes-batch]
level: practitioner
status: docs-checked
description: "Share GPU clusters fairly with Kueue: ResourceFlavors, ClusterQueues with nominal quotas, cohorts and borrowing, LocalQueues, all-or-nothing admission and preemption."
sources:
  - https://kueue.sigs.k8s.io/docs/concepts/
  - https://kueue.sigs.k8s.io/docs/tasks/manage/setup_wait_for_pods_ready/
  - https://kueue.sigs.k8s.io/docs/concepts/preemption/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kueue quotas and gang scheduling

**Goal:** teams share GPU capacity with guaranteed quotas, idle capacity gets borrowed, and distributed jobs start all-or-nothing instead of deadlocking half-scheduled.

## Objects
```yaml
apiVersion: kueue.x-k8s.io/v1beta2
kind: ResourceFlavor
metadata: {name: h100}
---
apiVersion: kueue.x-k8s.io/v1beta2
kind: ClusterQueue
metadata: {name: team-a}
spec:
  namespaceSelector: {}
  resourceGroups:
  - coveredResources: ["cpu", "memory"]    # add GPU resource names here too
    flavors:
    - name: h100
      resources:
      - {name: "cpu", nominalQuota: 256}
      - {name: "memory", nominalQuota: 2Ti}
---
apiVersion: kueue.x-k8s.io/v1beta2
kind: LocalQueue
metadata: {name: team-a, namespace: team-a}
spec: {clusterQueue: team-a}
```

## Submitting work
Label the job with its queue:
```yaml
metadata:
  labels: {kueue.x-k8s.io/queue-name: team-a}
```
Kueue creates jobs **suspended**, admits them when the whole workload's quota fits, then unsuspends. Check the Kueue docs for the list of supported workload types. Priority via `WorkloadPriorityClass`, independent of pod priority.

## Gang scheduling
Quota admission is all-or-nothing for the workload's resources, but pods can still fail to schedule (fragmentation, node taints). Enable `waitForPodsReady` in the Kueue config: if all pods aren't ready within the timeout, the workload is evicted and requeued, releasing capacity instead of holding half a job's GPUs forever.

## Policies to decide
- Nominal quota per team, borrowing limits (`borrowingLimit`), and the `withinClusterQueue` and `reclaimWithinCohort` preemption policies of each ClusterQueue (see the preemption page); queues in a cohort can borrow unused nominal quota.
- Fair sharing (weights across cohorts) for shared research clusters.
- Separate ClusterQueues/flavors for interactive (notebooks) vs batch training vs spot capacity.

## Verify
- [ ] A job exceeding free quota stays pending (suspended) without holding GPUs.
- [ ] Borrowed capacity is reclaimed when the owner submits work.
- [ ] Multi-node job either fully starts or is requeued after the readiness timeout.

## Checked
2026-11-01. Confirmed against the Kueue concepts, preemption and wait-for-pods-ready pages: v1beta2 API version, ClusterQueue resourceGroups/coveredResources/flavors/nominalQuota/namespaceSelector, queue-name label, suspended jobs, WorkloadPriorityClass, waitForPodsReady eviction and requeue, withinClusterQueue and reclaimWithinCohort, borrowingLimit, Fair Sharing weights. Removed: v1beta1 apiVersion, nodeLabels, cohort field, policy values, GPU resource example, integration list.
Method: documentation only; no commands were run.
