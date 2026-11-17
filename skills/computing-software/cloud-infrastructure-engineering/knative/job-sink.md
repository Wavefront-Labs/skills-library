---
id: computing-software.cloud-infrastructure-engineering.knative.job-sink
name: job-sink
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [jobsink, long-running-jobs, batch-job, kueue, jobsink-event]
level: advanced
status: docs-checked
description: "Run event-triggered work longer than a request using JobSink, which creates a Kubernetes Job per event."
sources:
  - https://knative.dev/docs/eventing/sinks/job-sink/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: process events with jobs that outlive an HTTP connection.

Event processing with a Knative Service is expected to finish in a relatively short period, minutes, because the HTTP connection must stay open or the service is scaled down. Long-lived connections increase the chance of failure, and the processing then restarts when the request is retried.

`JobSink` is a resource for long-running asynchronous jobs and tasks. It supports the full Kubernetes `batch/v1` Job resource and its features, and Job queuing systems such as Kueue.

Prerequisite: a cluster with Knative Eventing installed.

When an event is sent to a JobSink, Eventing creates a Job and mounts the received event as a JSON file at `/etc/jobsink-event/event`. Your container reads that file instead of handling a request.

```yaml
apiVersion: sinks.knative.dev/v1alpha1
kind: JobSink
metadata:
  name: job-sink-logger
spec:
  job:
    spec:
      completions: 1
      parallelism: 1
```

The `spec.job` field takes a normal Job spec, so add the pod template with your container beneath it. The sample sets `completions` and `parallelism` to 1.

Idempotency: a Job is created per distinct event, identified by the event `source` and `id`; a repeat with the same pair does not create another Job while one exists. To clean up finished Jobs, set `spec.job.spec.ttlSecondsAfterFinished` (the page uses 600 seconds). A JobSink can also be the sink of a source, a Trigger or a Broker dead letter sink.

Choose JobSink over a Knative Service sink when work takes longer than a request should stay open.

## Checked

2026-11-04. Confirmed against the JobSink page (knative/docs source): the short-processing limitation of Knative Service sinks, JobSink supporting the full `batch/v1` Job and Kueue, the Eventing prerequisite, the event mounted as JSON at `/etc/jobsink-event/event`, the `sinks.knative.dev/v1alpha1` JobSink manifest with `completions` and `parallelism`, per-event Job creation keyed on `source` and `id`, `ttlSecondsAfterFinished`, and use from sources, Triggers and as a Broker dead letter sink. Added the idempotency, cleanup and trigger-source facts from the same page. Nothing removed.

Method: documentation only; no commands were run.
