---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubernetes-event-based-debugging
name: kubernetes-event-based-debugging
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, events, kubectl-get-events, event-ttl, event-exporter, audit-logs, reason-codes, involvedobject, debugging, correlation]
level: advanced
status: docs-checked
description: "Reading and correlating Kubernetes Events for debugging: their short default TTL, reason/field taxonomy, aggregation/deduplication, and exporting before they expire."
sources: ["https://kubernetes.io/docs/reference/kubernetes-api/cluster-resources/event-v1/", "https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/", "https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/", "https://github.com/kubernetes/kube-state-metrics"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubernetes Events: the log of *why*, with a one-hour memory

**Goal:** use Events as the fastest path from "something happened" to "here's why," know
exactly how long you have before they vanish, and export them before an incident review
needs evidence that's already gone.

## 1. What an Event actually is
An Event is a first-class API object (`v1.Event`, in `events.k8s.io/v1` the newer schema)
recording a single occurrence tied to an `involvedObject` (a Pod, Node, PVC, Deployment,
etc.), with a `reason` (a short machine-readable code like `Scheduled`, `Pulling`, `Pulled`,
`Created`, `Started`, `Killing`, `FailedScheduling`, `BackOff`, `Unhealthy`,
`FailedMount`, `NodeNotReady`), a human-readable `message`, a `type` (`Normal` or
`Warning`), and `firstTimestamp`/`lastTimestamp`/`count` (core/v1; `series` in events.k8s.io/v1) so
that repeated occurrences of the same event can be recorded as one object rather than thousands
of rows during a crash loop.

```bash
kubectl get events -n <ns> --sort-by=.lastTimestamp
kubectl get events -n <ns> --field-selector involvedObject.name=<pod>,type=Warning
kubectl describe pod <pod>   # shows only events for that object, already correlated
```

## 2. The TTL trap
Events are **not durable records** — the kube-apiserver `--event-ttl` flag has a default of 1 hour,
after which events are garbage collected permanently. Consequences:
- An incident investigated more than an hour after the fact has **no Events left** — if the
  postmortem needs "why did this pod get evicted at 03:14," the answer must already be in a
  durable system (see §3), or the only remaining evidence is the Event-derived metrics in
  kube-state-metrics (restart counts, status) which lack the narrative `reason`/`message`
  text.
- This also means `kubectl get events` right after an incident is urgent, not optional — grab
  it before the TTL window closes if you're not already shipping Events elsewhere.

## 3. Making Events durable: event-exporter and the audit log distinction
- An **event exporter** is a small controller that watches the Events API and ships
  each event to a log/metrics backend before TTL expiry — the standard fix, usually deployed
  as a single replica (each extra replica independently watches and forwards, duplicating events).
- **Events are not the same thing as the Kubernetes audit log.** Events are emitted by
  controllers/kubelet describing *what the system observed happening* (a probe failed, an
  image pulled); the audit log records *API requests made against the apiserver* (who
  called `DELETE` on this pod, from what service account). For "who deleted this," you need
  audit logs, not Events — Events won't show the actor, only the consequence (a
  `Killing`/`Deleted` observation with no `user` field). Don't rely on Events for anything
  security/forensics-shaped.

## 4. Correlating Events with everything else
- Combine Event `reason` codes with kube-state-metrics' status gauges
  (`computing-software.cloud-infrastructure-engineering.kubernetes.kube-state-metrics-object-state-and-cardinality`)
  for the "when did state change" vs "what did the system say caused it" pairing — KSM tells
  you a Deployment's replica count dropped at time T, Events tell you it was a
  `FailedScheduling` due to insufficient CPU, not a crash.
- `FailedScheduling` events carry the **scheduler's actual predicate failure reasons** in the
  message (e.g. "0/12 nodes are available: 8 Insufficient cpu, 4 node(s) had taint
  {...} that the pod didn't tolerate") — this is often the single most information-dense
  line in the whole cluster for a stuck-Pending investigation; read the full message, not
  just the reason code.
- For logging-side correlation, Events have no body text shipped alongside app logs by
  default — an event-exporter pipeline writing into the same Loki/Elasticsearch instance as
  app logs (tagged distinctly, e.g. `job="k8s-events"`) lets one query surface both.

## Gotchas
- `type: Normal` events (`Scheduled`, `Pulled`, `Started`) are high-volume and mostly noise
  for alerting — alert on `type: Warning` reasons, and even then filter to known-actionable
  ones (`FailedScheduling`, `FailedMount`, `BackOff`, `Unhealthy`, `FailedCreate`) rather
  than all Warnings.
- `kubectl describe pod` shows only events still within the TTL window, not the full history.
- RBAC: Events are namespace-scoped like most objects; a service account or dashboard reading
  across namespaces needs explicit `list`/`watch` on `events` cluster-wide, a common gap when
  scoping a monitoring tool's RBAC narrowly for "least privilege" and then wondering why its
  event feed is empty for other namespaces.

## Verify
- [ ] An event-exporter (or equivalent) ships every `Warning` event to a durable backend before the apiserver's `--event-ttl` window closes.
- [ ] Alerting on Events is scoped to a known-actionable reason allowlist, not every Warning.
- [ ] Postmortems pull the full `FailedScheduling`/similar message text, not just the reason code.
- [ ] Anyone asking "who did this" is pointed at audit logs, not Events.

## Checked

Date: 2026-10-27. Documentation release: Kubernetes v1.37.1 (latest release; website main is the v1.38 development tree).

- `--event-ttl` default of 1 hour: kube-apiserver options source v1.37.1.
- Event reasons `Created`, `Started`, `Pulling`, `Pulled`, `Killing`, `BackOff`, `Unhealthy`, `FailedMount`,
  `FailedAttachVolume`, `FailedCreatePodSandBox`, `NodeNotReady`, `ProbeWarning`: kubelet `events/event.go` v1.37.1;
  `Scheduled` and `FailedScheduling`: scheduler `schedule_one.go`; `FailedCreate`: Deployment page.
- `0/<n> nodes are available: ...` scheduler message format: scheduler framework `types.go`.
- Event API object fields (`count`, series): Event v1 API reference.
- Removed: named third-party exporters, the claim that managed offerings fix the TTL, the `ProbeWarning` "expected noise"
  remark and the paragraph on count caps, which no documentation covers.

Method: documentation only; no commands were run.
