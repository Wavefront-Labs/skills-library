---
id: computing-software.devops-ci-cd.argo-events.argo-events-eventbus-resource-and-naming
name: argo-events-eventbus-resource-and-naming
category: computing-software
field: devops-ci-cd
product: argo-events
tags: [argo-events, eventbus, default, eventbusname, crd, namespaced]
level: practitioner
status: docs-checked
description: "Create the EventBus custom resource that Argo Events requires per namespace, name it default, and reference other buses with eventBusName."
sources: ["https://github.com/argoproj/argo-events/blob/master/docs/eventbus/eventbus.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Argo events eventbus resource and naming

EventBus is a namespaced custom resource (GA since v0.17.0) carrying events from EventSources to Sensors. It is backed by NATS (the older NATS Streaming service or the newer JetStream) or Kafka, and other technologies may follow.

An EventBus must exist in a namespace before EventSources and Sensors there can work. The common practice is one named `default`. If you use a different name, or run several EventBuses in one namespace, set `eventBusName` in the `spec` of each EventSource and Sensor so they find the right one.

```yaml
apiVersion: argoproj.io/v1alpha1
kind: EventBus
metadata:
  name: default
spec:
  jetstream:
    version: latest   # pin a specific version in real deployments
```

To view the finalized config, the NATS Streaming page gives `kubectl get eventbus default -o json | jq '.status.config'`. Choosing a backend: the Kafka page recommends Jetstream for getting started quickly and Kafka for a lot of events and horizontally scaled Sensors; NATS Streaming is deprecated and new EventBuses should use JetStream.

## Checked

2026-11-04. Confirmed against the EventBus page (namespaced custom resource, GA from v0.17.0, backends, required per namespace, `default` name, `eventBusName` in EventSource and Sensor specs) and the Jetstream, Kafka and NATS Streaming pages for the example, the backend advice and the status command. Rewrote the closing paragraph to attribute these to the pages that state them and dropped "very high event volumes" and the description of the status output.
Method: documentation only; no commands were run.
