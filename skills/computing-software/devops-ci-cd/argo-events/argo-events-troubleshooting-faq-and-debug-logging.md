---
id: computing-software.devops-ci-cd.argo-events.argo-events-troubleshooting-faq-and-debug-logging
name: argo-events-troubleshooting-faq-and-debug-logging
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, faq, debugging, log-level, eventbus, sensor-logs, namespace]
level: intro
status: docs-checked
description: "Work through the official debug checklist when an EventSource receives events but nothing triggers, and raise log verbosity."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/FAQ.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events troubleshooting faq and debug logging

Debug checklist from the FAQ:
1. Everything is installed as per the installation guide.
2. An `EventBus` resource exists in the namespace.
3. EventBus, EventSource and Sensor pods are running; if not, read the logs of the sensor-controller, event-source-controller and event-bus-controller.
4. If pods run but no events arrive: check the EventSource configuration and the EventSource pod container logs.

Set the env var `LOG_LEVEL` (`info`, `debug` or `error`) on any container for more output (see `examples/sensors/log-debug.yaml`).

EventSource receives events but nothing happens: check that the Sensor exists and its pod runs, and look for `Started to subscribe events for triggers` in the Sensor log. If that appears but no trigger resource is created, raise an issue. Verify each dependency's `eventSourceName` and `eventName` match the EventSource object.

Other FAQ answers: EventSources and Sensors can live in a namespace other than `argo-events` if you update the namespace and service account and grant the needed roles. The Minio EventSource is only for Minio servers; for AWS S3 notifications use the AWS SNS EventSource. Do not trust the `latest` image tag; pin versions. The Helm chart and the kustomization are community-maintained and may lag the official `install.yaml`. To run a specific trigger on a specific event within one Sensor, use trigger conditions (circuit and switch tutorial).

## Checked

2026-11-07: Read in full from a local clone of the argoproj/argo-events docs (master), which is the source of the cited GitHub page: docs/FAQ.md. Confirmed: debug checklist, LOG_LEVEL values, subscribe log line, namespace answer, Minio vs SNS, latest tag, Helm and kustomize, trigger conditions answer. Removed or changed: nothing; every claim matched the page. The example manifests the page links to (under examples/) were not opened; only snippets printed on the page were checked.

Method: documentation only; no commands were run.
