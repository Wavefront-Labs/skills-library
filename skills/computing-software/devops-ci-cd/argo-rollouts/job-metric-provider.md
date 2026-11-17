---
id: computing-software.devops-ci-cd.argo-rollouts.job-metric-provider
name: job-metric-provider
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [job, kubernetes-job, metric-provider, analysis, analysis-job-namespace, argo-rollouts]
level: practitioner
status: docs-checked
description: "Use a Kubernetes Job as an analysis metric where exit code zero means success."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/analysis/job/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Job metric runs a Kubernetes Job; it is successful if the Job completes with exit code zero and failed otherwise. It is ideal for smoke tests or integration checks.

```yaml
metrics:
  - name: test
    provider:
      job:
        metadata:
          annotations:
            foo: bar
          labels:
            foo: bar
        spec:
          backoffLimit: 1
          template:
            spec:
              containers:
                - name: test
                  image: my-image:latest
                  command: [my-test-script, my-service.default.svc.cluster.local]
              restartPolicy: Never
```

`metadata` annotations and labels are copied to the Job object.

Outcomes:

1. Job ends with exit 0: passed.
2. Job ends with a non-zero code: failed.
3. A Job pod is stuck in a terminal waiting state such as `ErrImagePull`, `ImagePullBackOff` or `InvalidImageName`: the metric short-circuits to Inconclusive.
4. Job still running at the end of the rollout steps and terminated because it is no longer needed: Inconclusive with no effect on the Rollout. This happens when another metric already failed, or a background job outlives the rollout.

Control where jobs run with controller environment variables: `ARGO_ROLLOUTS_ANALYSIS_JOB_NAMESPACE` runs metric jobs in a namespace other than the default, and `ARGO_ROLLOUTS_ANALYSIS_JOB_KUBECONFIG` is a path to a kubeconfig to run them in a different cluster.

Verify with `kubectl get jobs -n NAMESPACE` while the AnalysisRun is active.

## Checked

2026-11-03. Confirmed against the Argo Rollouts documentation pages: https://argo-rollouts.readthedocs.io/en/stable/analysis/job/.

Removed or corrected: nothing; claims matched.

Method: documentation only; no commands were run.
