---
id: computing-software.cloud-infrastructure-engineering.keda.scaledjob-overview-and-pausing
name: scaledjob-overview-and-pausing
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [scaledjob, jobtargetref, scaling-jobs, pause-scaledjob, rabbitmq, keda-jobs]
level: practitioner
status: docs-checked
description: "Use a ScaledJob to run one Kubernetes Job per event, with the example RabbitMQ manifest and the autoscaling.keda.sh/paused annotation."
sources:
  - https://keda.sh/docs/2.17/concepts/scaling-jobs/
  - https://keda.sh/docs/2.17/reference/scaledjob-spec/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A ScaledJob is the alternative to scaling Deployments when work is long-running. For each detected event KEDA schedules a Kubernetes Job that initialises, pulls a single event, processes it to completion and terminates. The flow with RabbitMQ: no messages means no Jobs; a message arrives and KEDA creates a Job; more messages create more Jobs; finished or failed Jobs are cleaned up according to `successfulJobsHistoryLimit` and `failedJobsHistoryLimit`.

Example spec fragment from the documentation:

```yaml
spec:
  jobTargetRef:
    template:
      spec:
        containers:
        - name: demo-rabbitmq-client
          image: demo-rabbitmq-client:1
        restartPolicy: Never
    backoffLimit: 4
  pollingInterval: 10
  maxReplicaCount: 30
  triggers:
  - type: rabbitmq
    metadata:
      queueName: hello
      host: RabbitMqHost
      queueLength: '5'
```

`jobTargetRef` is a batch/v1 JobSpec and its `template` is required. ScaledJob labels and annotations are applied to the child Jobs.

Pausing: add `autoscaling.keda.sh/paused: true` to the ScaledJob metadata; remove it or set it to `false` to resume. Pausing is preferable to deleting because the definition survives.

## Checked

2026-11-03. Confirmed on the 2.17 Scaling Jobs and ScaledJob specification pages: flow, example, jobTargetRef, labels and annotations, pausing.

Method: documentation only; no commands were run.
