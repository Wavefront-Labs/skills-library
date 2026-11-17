---
id: computing-software.cloud-infrastructure-engineering.keda.long-running-executions-in-keda
name: long-running-executions-in-keda
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [long-running-jobs, terminationgraceperiodseconds, prestop-hook, sigterm, scale-down-risk, scaledjob]
level: advanced
status: docs-checked
description: "Protect long messages from being killed on scale-down by delaying termination with SIGTERM handling or by using ScaledJobs."
sources:
  - https://keda.sh/docs/2.17/concepts/scaling-deployments/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The problem: a Deployment triggered by a RabbitMQ queue where each message takes 3 hours may scale out to 4 replicas. When the HPA scales down to 2, you cannot choose which replicas are terminated, so one 2.9 hours into a message might be picked.

Two documented options:

1. Use the container lifecycle. Kubernetes sends `SIGTERM` when it intends to terminate a pod and waits for the process to exit or for `terminationGracePeriodSeconds` to expire before killing it. Your consumer can trap `SIGTERM`, finish the current batch of messages, then exit. A `preStop` hook is another way to delay termination. Downside: while delaying, the pod stays in the `Terminating` phase, so a very long delay shows `Terminating` for the whole period.

2. Run the work as Kubernetes Jobs instead of a Deployment or custom resource, using a ScaledJob (see scaledjob-overview-and-pausing). Each event gets its own Job that pulls one message, processes it to completion and terminates.

The page presents the Jobs approach as the alternative way to handle long-running executions.

## Checked

2026-11-03. Confirmed on the 2.17 Scaling Deployments page: the 3 hour example, SIGTERM and terminationGracePeriodSeconds, preStop, Terminating downside, run as jobs. Removed: advice on grace period sizing and on when to choose each option.

Method: documentation only; no commands were run.
