---
id: computing-software.cloud-infrastructure-engineering.kubernetes.job-pods-and-logs-by-label
name: job-pods-and-logs-by-label
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, job, job-name-label, kubectl-logs, cronjob]
level: practitioner
status: docs-checked
description: "Find a Job's pods and logs via batch.kubernetes.io/job-name and controller-uid labels, follow CronJob runs, and clean up pods from finished Jobs."
sources: ["https://kubernetes.io/docs/concepts/workloads/controllers/job/", "https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/", "https://kubernetes.io/docs/reference/labels-annotations-taints/#batchkubernetesio-job-name", "https://kubernetes.io/docs/reference/kubectl/generated/kubectl_logs/", "https://github.com/kubernetes/kubernetes/blob/master/pkg/registry/batch/job/strategy.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Job pods and logs by label

## Labels the Job controller sets on its pods
- `batch.kubernetes.io/job-name=<job>` (the unprefixed `job-name` label is deprecated since 1.27)
- `batch.kubernetes.io/controller-uid=<job uid>` (unprefixed `controller-uid` deprecated since 1.27)
- Indexed Jobs: `batch.kubernetes.io/job-completion-index=<i>` (label since v1.28, behind the
  `PodIndexLabel` feature gate, enabled by default; also set as an annotation)

## Commands
```bash
kubectl get pods -l batch.kubernetes.io/job-name=import-2026-10-18
kubectl logs job/import-2026-10-18                 # first container of one pod only
kubectl logs -l batch.kubernetes.io/job-name=import-2026-10-18 --all-containers --prefix --tail=-1
kubectl logs -l batch.kubernetes.io/job-name=import,batch.kubernetes.io/job-completion-index=3
kubectl describe job import-2026-10-18 | sed -n '/Events/,$p'
```
`kubectl logs` with `-l` defaults to the last 10 lines per pod; pass `--tail=-1` for everything,
and `--max-log-requests` above 5 if many pods match.

## CronJob runs
The CronJob controller names each Job by appending 11 characters to the CronJob name (hence the
52-character CronJob name limit); find the latest:
```bash
kubectl get jobs --sort-by=.metadata.creationTimestamp | grep ^nightly- | tail -3
kubectl get jobs -o json | jq -r '.items[] | select(.metadata.ownerReferences[0].name=="nightly") | .metadata.name' | tail -1
```

## Failed pods vanish
With `ttlSecondsAfterFinished` or CronJob history limits (`successfulJobsHistoryLimit` default
3, `failedJobsHistoryLimit` default 1), Jobs, their pods and logs disappear. Ship logs to a
central store or keep `failedJobsHistoryLimit` above zero. Finished Jobs' pods are usually kept
until the Job is deleted; `backoffLimit` (default 6) caps retries.

## Cleanup
```bash
kubectl delete jobs --field-selector status.successful=1     # Jobs with exactly 1 succeeded pod; pods cascade
```

## Checked
2026-10-27, against kubernetes/website main (v1.38 dev tree): "Jobs", "CronJob", "Well-Known Labels, Annotations and Taints" and the `kubectl logs` reference; the Job field selector against `pkg/registry/batch/job/strategy.go`. Confirmed: prefixed Job labels and the 1.27 deprecation of unprefixed ones, the completion-index label and `PodIndexLabel` gate, `kubectl logs job/<name>` returning the first container, `--tail` default 10 with a selector and `--max-log-requests` default 5, the CronJob 11-character suffix, history-limit defaults 3 and 1, pods of finished Jobs usually kept, `backoffLimit` default 6, and the `status.successful` field selector.
Method: documentation only; no commands were run.
