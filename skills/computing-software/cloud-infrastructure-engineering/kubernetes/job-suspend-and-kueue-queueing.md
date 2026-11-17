---
id: computing-software.cloud-infrastructure-engineering.kubernetes.job-suspend-and-kueue-queueing
name: job-suspend-and-kueue-queueing
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, jobs, job-suspend, kueue, kueue-queues, batch-scheduling]
level: practitioner
status: docs-checked
description: "Suspend and resume Jobs with spec.suspend, and queue batch Jobs through Kueue ClusterQueues and LocalQueues so they start only when quota is free."
sources: ["https://kubernetes.io/docs/concepts/workloads/controllers/job/#suspending-a-job", "https://kueue.sigs.k8s.io/docs/tasks/run/jobs/", "https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/", "https://kueue.sigs.k8s.io/docs/concepts/resource_flavor/", "https://kueue.sigs.k8s.io/docs/concepts/workload/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Job suspend and Kueue

## spec.suspend
```bash
# create the Job with spec.suspend: true in its manifest (Kueue-managed Jobs do not need it), then:
kubectl patch job train --type=merge -p '{"spec":{"suspend":false}}'   # start
kubectl patch job train --type=merge -p '{"spec":{"suspend":true}}'    # stop running pods
```
Suspending terminates running pods with SIGTERM (the grace period is honoured); pods terminated
this way do not count towards `completions`. Resuming resets `status.startTime`, so
`activeDeadlineSeconds` restarts. The Job shows condition `Suspended=True`.

## Kueue in one page
- `ResourceFlavor`: a kind of capacity (for example on-demand vs spot, or a GPU model).
- `ClusterQueue`: quota per flavor (`nominalQuota`), optional `cohort` for borrowing.
- `LocalQueue`: namespaced pointer to a ClusterQueue that teams submit to.
```yaml
apiVersion: kueue.x-k8s.io/v1beta2
kind: LocalQueue
metadata: {name: team-a, namespace: team-a}
spec: {clusterQueue: research}
---
apiVersion: batch/v1
kind: Job
metadata:
  name: train
  namespace: team-a
  labels: {kueue.x-k8s.io/queue-name: team-a}
spec:
  suspend: true
  template: {spec: {restartPolicy: Never, containers: [{name: t, image: busybox, command: [sleep, "60"], resources: {requests: {cpu: "2"}}}]}}
```
Kueue manages the Job's suspension through a webhook, creates a matching `Workload`, admits it
when quota allows, and then resumes the Job. It adds the chosen ResourceFlavor's labels to the
Job's `.spec.template.spec.nodeSelector`.

## Debug
```bash
kubectl get workloads -n team-a
kubectl describe workload -n team-a <name>          # why not admitted: quota, flavor, priority
kubectl get clusterqueue research -o yaml        # status.flavorsReservation and status.flavorsUsage
```

## Gotchas
- Jobs without the queue label are ignored unless `manageJobsWithoutQueueName` is set.
- Specify resource requests or limits for each Job pod: Kueue computes quota from the Workload's
  podSet requests, and if only limits are set it treats them as requests.

## Checked

Documentation release checked: Kubernetes website v1.37 docs (kubernetes/website main, 2026-10-23); Kueue docs on kubernetes-sigs/kueue main (latest release v0.20.3 at the time of checking). Confirmed: Job suspend semantics, `Suspended` condition and startTime reset (Job page); Kueue objects and manifests use `kueue.x-k8s.io/v1beta2`; the `kueue.x-k8s.io/queue-name` label; ClusterQueue `nominalQuota` and cohort borrowing; ResourceFlavor labels are added to the Job's nodeSelector; Kueue creates a Workload per Job and manages suspension by webhook; requests or limits are used for quota; ClusterQueue status has `flavorsReservation` and `flavorsUsage` (API types); a config page for `manageJobsWithoutQueueName` exists.
Wrong in the draft and corrected: apiVersion v1beta1 (docs now use v1beta2), "injects node affinity" (docs say nodeSelector), "requests are mandatory" (limits are accepted as requests).
Removed: a `yq` pipeline that depended on a third-party tool.

Method: documentation only; no commands were run.
