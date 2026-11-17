---
id: computing-software.cloud-infrastructure-engineering.kubernetes.indexed-job-success-and-backoff-policies
name: indexed-job-success-and-backoff-policies
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, jobs, indexed-job, successpolicy, backofflimitperindex, elastic-indexed-job, podfailurepolicy, batch]
level: advanced
status: docs-checked
description: "Control Indexed Job outcomes: backoffLimitPerIndex and maxFailedIndexes, successPolicy for leader/quorum completion, podFailurePolicy rules, and elastic resizing of completions."
sources: ["https://kubernetes.io/docs/concepts/workloads/controllers/job/#backoff-limit-per-index", "https://kubernetes.io/docs/concepts/workloads/controllers/job/#success-policy", "https://kubernetes.io/docs/concepts/workloads/controllers/job/#elastic-indexed-jobs", "https://kubernetes.io/docs/concepts/workloads/controllers/job/#pod-failure-policy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Indexed Jobs: per-index backoff, success policy, elastic sizing

Indexed Jobs (`completionMode: Indexed`) give each pod `JOB_COMPLETION_INDEX` (0..completions-1)
— a shard ID for data-parallel work and ML training.

## Per-index retries (stable 1.33)
Global `backoffLimit` fails the whole Job when *total* failures exceed it — one bad shard kills
a 1000-shard run. Instead:
```yaml
spec:
  completionMode: Indexed
  completions: 1000
  parallelism: 50
  backoffLimitPerIndex: 3        # each index retried up to 3 times
  maxFailedIndexes: 20           # Job fails once more than 20 indexes are permanently failed
  podFailurePolicy:
    rules:
    - action: FailIndex          # don't retry this index on a known-fatal exit code
      onExitCodes: {containerName: worker, operator: In, values: [42]}
    - action: Ignore             # preemption/eviction doesn't count as a failure
      onPodConditions: [{type: DisruptionTarget}]
```
`status.failedIndexes` / `status.completedIndexes` list which shards failed or succeeded. A failing
index does not interrupt the others; once all indexes finish, the Job is marked failed if any index failed.
When `backoffLimitPerIndex` is set, `backoffLimit` defaults to 2147483647 (MaxInt32).
`podFailurePolicy` requires `restartPolicy: Never`.

## Success policy (stable 1.33)
Declare the Job done before every index finishes — e.g. a leader index or a quorum:
```yaml
  successPolicy:
    rules:
    - succeededIndexes: "0"          # leader (index 0) succeeded → Job succeeds
    - succeededCount: 800            # or any 800 indexes
      succeededIndexes: "0-999"
```
When a rule matches, the Job gets `SuccessCriteriaMet` then `Complete`, and remaining pods are
terminated. Only for Indexed Jobs. If `backoffLimit` or `podFailurePolicy` terminates the Job first, the
success policy is ignored.

## Elastic Indexed Jobs (stable 1.31)
`completions` may be changed together with `parallelism` (must be equal) on Indexed Jobs to
scale a running job up/down — used by MPI/elastic training frameworks. Scaling down removes the
highest indexes.

## Watch it
```bash
kubectl get job train -o jsonpath='{.status.completedIndexes}{"\n"}{.status.failedIndexes}{"\n"}'
kubectl get pods -l batch.kubernetes.io/job-name=train -L batch.kubernetes.io/job-completion-index
```

## Gotchas
- `onExitCodes.containerName` is optional: without it the rule applies to all containers; if set it
  must match a container or init container name in the pod template. Rules are evaluated in order and
  the first match wins.
- `activeDeadlineSeconds` still applies to the whole Job and overrides retries.

## Verify
- [ ] A forced failure in one index retries that index only and the Job continues.
- [ ] Leader-success Job ends as soon as index 0 succeeds.

## Checked

Documentation release checked: Kubernetes website v1.37 docs (kubernetes/website main, 2026-10-23). Confirmed in the Job concept page and feature-gates reference: `backoffLimitPerIndex`, `maxFailedIndexes`, `status.failedIndexes` and `completedIndexes`; backoffLimit default MaxInt32 when per-index is set; `FailIndex`, `Ignore`, `Count` and `FailJob` actions; podFailurePolicy requires restartPolicy Never and rules are evaluated in order; success policy rules (`succeededIndexes`, `succeededCount`), `SuccessCriteriaMet` then `Complete`, terminating policies win over success policy; elastic Indexed Jobs (`parallelism == completions`, scale-down removes higher indexes). Stages: JobBackoffLimitPerIndex stable 1.33, JobSuccessPolicy stable 1.33, ElasticIndexedJob stable 1.31, JobPodFailurePolicy stable 1.31.
Removed: the claim that backoffLimit "must be unset" with per-index retries, and the claim that native sidecars are excluded from exit-code rules.

Method: documentation only; no commands were run.
