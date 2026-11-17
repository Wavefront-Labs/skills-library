---
id: computing-software.devops-ci-cd.argo-events.argo-events-architecture-event-source-sensor-eventbus-trigger
name: argo-events-architecture-event-source-sensor-eventbus-trigger
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, architecture, eventsource, sensor, eventbus, trigger, cloudevents]
level: intro
status: docs-checked
description: "Understand the four Argo Events building blocks and how an event flows from EventSource over the EventBus to a Sensor and its Triggers."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/concepts/architecture.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events architecture event source sensor eventbus trigger

Argo Events is built from four parts:
1. EventSource: defines how to consume events from an external source (webhooks, AWS SNS and SQS, GCP PubSub, Kafka, GitHub, GitLab, Slack, Stripe, MQTT, NATS, Redis, calendar, files, Kubernetes resources and more) and transforms each event into a CloudEvent that it dispatches to the EventBus.
2. EventBus: the transport layer connecting EventSources and Sensors. EventSources publish; Sensors subscribe. Implementations are NATS Streaming (deprecated), JetStream and Kafka.
3. Sensor: a set of event dependencies (inputs) and triggers (outputs). It listens on the EventBus and acts as an event dependency manager that resolves and executes triggers.
4. Trigger: the resource or workload a Sensor runs once its dependencies resolve.

A dependency is simply an event the Sensor is waiting for. Trigger types include AWS Lambda, Apache OpenWhisk, Argo Rollouts, Argo Workflows, custom "build your own", HTTP requests (OpenFaaS, Kubeless, KNative and similar), Kafka messages, NATS messages, Slack notifications, Azure Event Hubs messages, creation of any Kubernetes object, and a Log trigger for debugging bus messages.

Full API specifications are in the APIs document, and runnable examples live under `examples/event-sources` and `examples/sensors` in the repository.

## Checked

2026-11-04. Confirmed against the Architecture page and the four concept pages it links (Event Source, EventBus, Sensor, Trigger): the component roles, the EventBus implementations (NATS deprecated, JetStream, Kafka), the trigger type list, the example folders and the APIs reference link. Nothing removed.
Method: documentation only; no commands were run.
