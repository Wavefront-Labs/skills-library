---
id: computing-software.cloud-infrastructure-engineering.kubernetes.job-mechanics-parallelism-and-completions
name: job-mechanics-parallelism-and-completions
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, job, completions, parallelism, indexed-job, completionmode, backofflimit, podfailurepolicy, activedeadlineseconds, ttlsecondsafterfinished, suspend, restartpolicy, batch-processing, job-completion-index, work-queue]
level: advanced
status: docs-checked
description: "Job completion modes (NonIndexed/Indexed), parallelism vs completions, backoffLimit and podFailurePolicy, activeDeadlineSeconds, TTL cleanup, and suspend for queued batch work."
sources: ["https://kubernetes.io/docs/concepts/workloads/controllers/job/#parallel-jobs", "https://kubernetes.io/docs/concepts/workloads/controllers/job/#completion-mode", "https://kubernetes.io/docs/concepts/workloads/controllers/job/#pod-backoff-failure-policy", "https://kubernetes.io/docs/concepts/workloads/controllers/job/#pod-failure-policy", "https://kubernetes.io/docs/tasks/job/indexed-parallel-processing-static/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Job mechanics — completions, parallelism and what counts as "done"

**Goal:** pick the right completion mode and failure handling for batch work so a Job
finishes exactly once per unit of work, retries the right failures, and doesn't retry the
wrong ones forever.

## 1. completions × parallelism × completionMode
- `completions` is **how many successful pod completions are needed** for a fixed-completion-count
  Job. With both `completions` and `parallelism` unset, both default to 1 (non-parallel Job). With
  `completions` unset and `parallelism` set, it is a work-queue Job: pods coordinate on their own,
  no new pods start once one succeeds, and the Job completes when one pod has succeeded and all pods
  have terminated.
- `parallelism` (default 1; 0 pauses the Job) is the requested ceiling on concurrently running
  pods, not a guarantee: for fixed-count Jobs it never exceeds the remaining completions, and
  quota, permissions, controller throttling after many failures and pod shutdown time can all
  lower it.
- `completionMode: NonIndexed` (default): pods are interchangeable; any `completions`
  successes count equally, with no notion of "which" item each pod did. Fine for a
  self-dequeuing work queue (each pod pulls the next item from an external queue).
- `completionMode: Indexed`: each pod gets an index 0..completions-1, available as the
  `JOB_COMPLETION_INDEX` env var, the `batch.kubernetes.io/job-completion-index` annotation and
  label (label from 1.28) and the hostname `$(job-name)-$(index)`, so you can statically partition work
  (`process-shard-$JOB_COMPLETION_INDEX`) without an external queue. A failed index is
  retried as *that same index*, not a new arbitrary unit — this is the mechanism that makes
  Indexed jobs usable for "process files 0..999, one pod per file range."

## 2. Retry and failure accounting
- `backoffLimit` (default 6) is the number of retries before the Job is marked `Failed`. It counts
  pods in phase `Failed` and, with `restartPolicy: OnFailure`, container restarts in Pending or
  Running pods; if either count reaches the limit the Job fails. For Indexed Jobs,
  `backoffLimitPerIndex` gives independent per-index limits (and `backoffLimit` then defaults to
  MaxInt32). Replacement pods are created with exponential backoff (10s, 20s, 40s, ...) capped at
  ten minutes.
- `restartPolicy: OnFailure` restarts the **container in place** on the same pod, and the pod is
  terminated once the backoff limit is reached, which can make debugging harder (the docs suggest
  `Never` while debugging or shipping logs elsewhere); `restartPolicy: Never` lets the pod fail and
  the Job controller creates a **new pod** for the retry. Most batch jobs want `Never` so each
  attempt starts from a clean pod/filesystem.
- `podFailurePolicy` (stable since 1.31; requires `restartPolicy: Never`; rules are evaluated in order) lets you react
  to *why* a pod failed instead of just that it failed:
  ```yaml
  podFailurePolicy:
    rules:
    - action: FailJob            # don't retry — e.g. a bad input that will never succeed
      onExitCodes: {containerName: worker, operator: In, values: [42]}
    - action: Ignore              # don't count against backoffLimit — e.g. node was preempted
      onPodConditions: [{type: DisruptionTarget, status: "True"}]
  ```
  Without this, a spot-node preemption or a deliberate "no more work, exit 42" both just
  burn a `backoffLimit` retry indistinguishably from a real bug.

## 3. Lifetime and cleanup
- `activeDeadlineSeconds` is a **wall-clock** cap on the whole Job (not per-pod); exceeding
  it marks the Job `Failed` with reason `DeadlineExceeded` and kills all running pods —
  use it as a circuit breaker against a batch job that hangs instead of erroring.
- `ttlSecondsAfterFinished` (stable since 1.23) lets the TTL controller delete the Job, and its pods
  by cascading, that many seconds after it finishes (`Complete` or `Failed`). Without it, finished
  Jobs and their pods are kept (useful for logs) until you delete them, which adds API server load.
- `suspend: true` creates the Job object without starting any pods; flipping it to `false`
  starts them. Resuming resets `status.startTime`, so the `activeDeadlineSeconds` timer restarts.
  Suspending terminates running pods with SIGTERM and they do not count towards `completions`.

## Gotchas
- Setting `completions` without `parallelism` runs one pod at a time — fine for
  correctness, slow for throughput; raise `parallelism` deliberately.
- Indexed jobs still need external coordination if work items aren't a dense `0..N-1` range
  — the index is just an integer, not a lookup key into your data unless you make it one.
- Finished Jobs and their pods are kept until deleted: set `ttlSecondsAfterFinished` or clean up
  yourself (a CronJob also prunes by its history limits).
- `backoffLimit: 0` means any single pod failure fails the whole Job immediately — useful
  for "fail fast" migrations where a retry could do partial, inconsistent work.

## Verify
- [ ] `kubectl get job <name> -o jsonpath='{.status.succeeded}/{.spec.completions}'` reaches
      the expected ratio with no pods stuck `Pending` under the `parallelism` ceiling.
- [ ] For an Indexed job, `kubectl logs <pod>` for each shows a distinct, expected
      `JOB_COMPLETION_INDEX` with no duplicate or missing index.
- [ ] A deliberately failing pod with `podFailurePolicy: FailJob` on its exit code fails the
      Job on the first failure, not after `backoffLimit` retries.
- [ ] Finished Jobs disappear within `ttlSecondsAfterFinished` of completion.

## Checked

Documentation release checked: Kubernetes website v1.37 docs (kubernetes/website main, 2026-10-23). Confirmed in the Job concept page: the three Job types and defaults (completions and parallelism both default to 1 when unset; parallelism 0 pauses); completion modes and the four index mechanisms; backoffLimit default 6 and how failures are counted for Never and OnFailure, backoff capped at ten minutes; podFailurePolicy semantics; suspend resets startTime and terminates pods with SIGTERM; TTL mechanism stable 1.23; activeDeadlineSeconds behaviour.
Wrong in the draft and corrected: the backoff cap was stated as 6 minutes (docs say ten minutes); the OnFailure retry accounting; the claim that CronJob uses suspend internally to create Jobs (not documented); the "confirm GA" note on podFailurePolicy.

Method: documentation only; no commands were run.
