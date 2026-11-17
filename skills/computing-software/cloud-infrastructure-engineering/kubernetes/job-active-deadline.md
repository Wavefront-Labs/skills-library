---
id: computing-software.cloud-infrastructure-engineering.kubernetes.job-active-deadline
name: job-active-deadline
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, job, deadlineexceeded, activedeadlineseconds, backofflimit]
level: practitioner
status: docs-checked
description: "Bound Job runtime with activeDeadlineSeconds, how DeadlineExceeded interacts with backoffLimit, pod termination and CronJob scheduling."
sources: ["https://kubernetes.io/docs/concepts/workloads/controllers/job/#job-termination-and-cleanup", "https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/job-v1/", "https://github.com/kubernetes/kube-state-metrics/blob/main/docs/metrics/workload/job-metrics.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Job activeDeadlineSeconds

```yaml
apiVersion: batch/v1
kind: Job
spec:
  activeDeadlineSeconds: 3600     # whole Job, counted from job start (or resume)
  backoffLimit: 4
  template:
    spec:
      restartPolicy: Never
      containers:
      - name: etl
        image: etl:2.1
```

## Semantics
- Applies to the Job's total duration regardless of retries. When reached, all running pods are
  terminated and the Job gets condition `Failed` with reason `DeadlineExceeded`.
- Takes precedence over `backoffLimit`: a Job that is retrying failed pods creates no more pods
  once the deadline passes, even with retries left.
- The pod template has its own `activeDeadlineSeconds` field (in `spec.template.spec`); the docs
  warn to set the field at the proper level.
- Suspending a Job resets the timer when it resumes.

## Diagnose
```bash
kubectl get job etl -o jsonpath='{range .status.conditions[*]}{.type}={.status} {.reason}: {.message}{"\n"}{end}'
kubectl describe job etl
```

## CronJobs
Set `activeDeadlineSeconds` in `jobTemplate.spec` shorter than the schedule interval when using
`concurrencyPolicy: Forbid`; otherwise one hung run blocks all future runs. Monitor with
kube-state-metrics: `kube_job_status_failure_reason{reason="DeadlineExceeded"}` (marked experimental in its docs).

## Gotchas
- Termination of the Job's pods follows the normal pod shutdown: `terminationGracePeriodSeconds` can delay the moment the terminal `Failed` condition appears (the controller adds `FailureTarget` first from 1.31).
- The deadline runs from the Job's start time, so scheduling and image pull time count against it.

## Checked

Documentation release checked: Kubernetes website v1.37 docs (kubernetes/website main, 2026-10-23). Confirmed in the Job concept page: `activeDeadlineSeconds` applies to the whole Job regardless of pods created; on reaching it all running pods are terminated and the Job gets `type: Failed`, `reason: DeadlineExceeded`; it takes precedence over `backoffLimit`; both the Job spec and the pod template have such a field; suspend and resume resets `status.startTime` and so the deadline timer; `FailureTarget` is added before the terminal condition and `terminationGracePeriodSeconds` can delay it. kube-state-metrics job metrics doc: reason breakdown is `kube_job_status_failure_reason` (experimental). CronJob `Forbid` skips a run while the previous Job is still running (CronJob page).
Wrong in the draft and corrected: the metric name for the DeadlineExceeded reason, and the claim that a pod-level deadline makes the Job retry that pod (not documented).

Method: documentation only; no commands were run.
