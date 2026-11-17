---
id: computing-software.cloud-infrastructure-engineering.knative.sinkbinding
name: sinkbinding
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [sinkbinding, k-sink, k-ce-overrides, subject, event-producer]
level: practitioner
status: docs-checked
description: "Point any PodSpec-based workload at a sink with SinkBinding, which injects K_SINK and K_CE_OVERRIDES."
sources:
  - https://knative.dev/docs/eventing/custom-event-source/sinkbinding/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let existing workloads send events without hardcoding the destination.

A SinkBinding decouples event production from delivery addressing. It directs a subject to a sink:
- A subject is a Kubernetes resource that embeds a PodSpec template and produces events.
- A sink is an addressable Kubernetes object that can receive events.

The SinkBinding injects environment variables into a PodTemplateSpec, so application code does not need to interact directly with the Kubernetes API to locate the event destination:
- `K_SINK`: the URL of the resolved sink.
- `K_CE_OVERRIDES`: a JSON object specifying overrides to the outbound event.

Application side: read `K_SINK` at start-up to find where to send events, and apply any overrides from `K_CE_OVERRIDES` if your code builds events itself.

## Checked

Method: docs-checked 2026-11-09 against https://knative.dev/docs/eventing/custom-event-source/sinkbinding/ (read in full; it is a short page). The page has no manifest example, so the earlier example YAML, the HTTP POST step and the list of sink kinds were dropped as unconfirmed.
