---
id: computing-software.cloud-infrastructure-engineering.observability.k8sobjects-receiver-for-kubernetes-events
name: k8sobjects-receiver-for-kubernetes-events
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [k8sobjects-receiver-config, k8s-events-receiver, otel-kubernetes, kubernetes-events, otel-collector]
level: practitioner
status: docs-checked
description: "Collect Kubernetes events and object snapshots with the k8sobjects receiver: watch vs pull modes, RBAC, single-replica deployment, and shaping event logs for Loki."
sources: ["https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/k8sobjectsreceiver", "https://opentelemetry.io/docs/platforms/kubernetes/collector/components/#kubernetes-objects-receiver", "https://kubernetes.io/docs/reference/kubernetes-api/cluster-resources/event-v1/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# k8sobjects receiver for events

Kubernetes events (scheduling failures, image pull errors, probe failures) are short-lived: the kube-apiserver `--event-ttl`
flag defaults to 1 hour. Ship them as logs to keep history and alert on them.

## Config (cluster-level collector, 1 replica)
```yaml
receivers:
  k8s_objects:                       # component type; the old name k8sobjects is deprecated
    auth_type: serviceAccount
    storage: file_storage             # optional: persists resourceVersion for watch objects
    objects:
      - name: events
        mode: watch
        group: events.k8s.io           # omit to select the first group, which for events is core v1
        exclude_watch_type: [DELETED]
      - name: pods
        mode: pull
        interval: 15m                  # periodic snapshot as log records
        label_selector: app.kubernetes.io/part-of=shop
        namespaces: [shop]
```
RBAC: a ClusterRole that allows the verbs the receiver uses (list and watch, plus get) on the watched resources, bound to the
collector's service account; the README has a full example manifest. Deploy as a **single replica**: the README states other
counts produce duplicated data. The `k8s_leader_elector` setting enables leader election through the `k8sleaderelector`
extension. The Helm chart has a `presets.kubernetesEvents` option.
Options used above: `mode` is `pull` (list API every `interval`, default 1h) or `watch`; `exclude_watch_type` accepts `ADDED`,
`MODIFIED`, `DELETED`, `BOOKMARK`, `ERROR` and only works in watch mode; `namespaces` defaults to all.

## Shaping
In watch mode each record's body is a map with `type` (the watch event type) and `object` (the Kubernetes object). The receiver also sets
`k8s.resource.name` as a log attribute and `k8s.namespace.name` on the resource. Make the fields queryable:
```yaml
transform/events:
  log_statements:
    - context: log
      statements:
        - set(attributes["k8s.event.reason"], body["object"]["reason"])
        - set(severity_text, body["object"]["type"])            # Normal | Warning
        - set(severity_number, SEVERITY_NUMBER_WARN) where body["object"]["type"] == "Warning"
        - set(body, body["object"]["note"])                       # events.k8s.io field; core v1 uses "message"
```
Keep `reason` and `type` as attributes so a log backend can filter on them (`reason`, `regarding`, `note` and `type` are fields of the
`events.k8s.io/v1` Event).

## Alternatives
The `k8s_events` receiver is a separate component; this receiver can also pull or watch any other API object (pods, nodes,
deployments, custom resources whose CRDs exist).

## Checked

2026-10-24. OpenTelemetry Collector contrib k8sobjects receiver README, metadata.yaml, and unstructured_to_logdata.go (main branch), kubernetes/kubernetes kube-apiserver options (`--event-ttl` default 1h) and k8s.io/api events/v1 types, and the opentelemetry-collector Helm chart values (`presets.kubernetesEvents`). Confirmed: component type is `k8s_objects` (deprecated alias `k8sobjects`), modes and options, single-replica requirement, watch body map with `type` and `object`, `k8s.resource.name` and namespace resource attribute, and the Event v1 field names. Removed Loki-specific indexing and alert queries (not covered by these sources).

Method: documentation only; no commands were run.
