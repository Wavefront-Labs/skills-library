---
id: computing-software.cloud-infrastructure-engineering.keda.cloudeventsource-emit-keda-events
name: cloudeventsource-emit-keda-events
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [cloudeventsource, cloudevents, eventing-keda-sh, event-sink, azure-event-grid, http-destination]
level: advanced
status: docs-checked
description: "Create a CloudEventSource (experimental) to emit KEDA events to an HTTP endpoint or Azure Event Grid, with clusterName and authenticationRef."
sources:
  - https://keda.sh/docs/2.17/operate/cloud-events/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The schema block in the page lists two destinations side by side, `http` with a `uri` and `azureEventGridTopic` with an `endpoint` URL, while the sink section spells the Event Grid key `azureEventGrid`; check the spelling against your KEDA version.
`CloudEventSource` (apiVersion `eventing.keda.sh/v1alpha1`) subscribes to events and delivers them to a CloudEvent sink. The feature is described as experimental. When the resource exists, events go to both Kubernetes Events and the CloudEvents destination.

```yaml
apiVersion: eventing.keda.sh/v1alpha1
kind: CloudEventSource
metadata:
  name: {cloud-event-name}
spec:
  clusterName: {cluster-name}
  authenticationRef:
    name: {trigger-authentication-name}
    kind: TriggerAuthentication
  destination:
    http:
      uri: http://foo.bar
```

`clusterName` is optional, appears in each event's source and subject, defaults to `kubernetes-default` and can be set at install time with `--k8sClusterName`; the resource value wins. `authenticationRef` is optional and can point to a ClusterTriggerAuthentication via `kind`.

Supported destinations are an HTTP endpoint (`destination.http.uri`) and Azure Event Grid (`destination.azureEventGrid.endpoint`). Event Grid authentication comes from a TriggerAuthentication: either `accessKey` for connection-string auth or the `azure-workload` pod identity provider.

Each event is a CloudEvents 1.0 JSON object with `type` `com.cloudeventsource.keda`, `source` `/{cluster-name}/{keda-namespace}/keda`, `subject` `/{cluster-name}/{namespace}/{object-type}/{object-name}`, and `data` holding `reason` and `message`.

## Checked

2026-11-03. Confirmed on the 2.17 CloudEvent Support page: schema, clusterName default and --k8sClusterName, destinations, Event Grid auth, event structure, and the azureEventGridTopic vs azureEventGrid spelling difference.

Method: documentation only; no commands were run.
