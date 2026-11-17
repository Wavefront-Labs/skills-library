---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.queue-based-scaling
name: queue-based-scaling
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, scalability, queue-based-scaling, keda, queue-depth-autoscaling, backlog-per-instance, sqs-scaling, worker-autoscaling]
level: practitioner
status: docs-checked
description: "Autoscale workers on queue backlog: backlog-per-instance target tracking for EC2 Auto Scaling with SQS, scale-in protection, and where KEDA and Container Apps fit."
sources: ["https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-using-sqs-queue.html", "https://keda.sh/docs/latest/concepts/scaling-deployments/", "https://learn.microsoft.com/azure/container-apps/scale-app"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Queue-depth based scaling

## Metric choice (EC2 Auto Scaling guide)
Scale in proportion to waiting work with a **backlog per instance** metric. A policy that tracks only the
queue length ignores how many instances exist and can add more instances than needed while the queue drains.
- Backlog per instance = `ApproximateNumberOfMessages` divided by the running capacity (instances in the
  InService state).
- Acceptable backlog per instance (the target value) = acceptable latency divided by the average time an
  instance takes to process a message. Worked example on the page: 10 s acceptable latency and 0.1 s per
  message give a target of 100; with 1500 messages on 10 instances the backlog is 150, so the group scales
  out by five instances.
- The page notes you can now avoid publishing your own custom metric by using metric math in a target
  tracking policy. Publishing a custom metric needs the AWS CLI or an SDK.

## Scale-in
Messages not processed when an instance terminates return to the SQS queue for another instance. For long
tasks, use instance scale-in protection so a worker is protected while it processes a work unit and
unprotected between units.

## Other platforms
- **KEDA** generates a Horizontal Pod Autoscaler for a scaled object and supports scale to zero when
  configured. Check the KEDA scalers list for the scaler of your queue and its trigger fields.
- **Azure Container Apps** scales replicas between `minReplicas` and `maxReplicas` using scale rules; see
  its scale page for rule types and settings.

## Steps
1. Measure processing time per message.
2. Set the target backlog per worker from the latency you can accept, and set maximum capacity so scaling
   cannot overload downstream systems.
3. Let in-flight work finish or return to the queue when an instance is terminated (see the SQS visibility
   timeout in queue-based-load-leveling).

## Gotchas
- Scaling on CPU alone for I/O-bound workers may never trigger; scale on the queue.
- Scaling from zero adds start-up delay before the first message is handled.

## Verify
- [ ] Burst test: backlog drains within the latency target and workers scale back in.

## Checked
2026-11-01. Confirmed against the EC2 Auto Scaling "Scaling policy based on Amazon SQS" page (backlog per
instance, target value, example, metric math note, scale-in protection) and the KEDA scaling-deployments
page (HPA, scale to zero). Removed: the KEDA field names (`queueLength`, `lagThreshold`, `cooldownPeriod`,
`pollingInterval`), Lambda maximum concurrency, the Kafka partition rule and the oldest-message alarm advice,
which these pages do not state or were not read.
Method: documentation only; no commands were run.
