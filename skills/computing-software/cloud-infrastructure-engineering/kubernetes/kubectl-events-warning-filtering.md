---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubectl-events-warning-filtering
name: kubectl-events-warning-filtering
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, events, warning-events, kubectl-get-events, reason-codes]
level: practitioner
status: docs-checked
description: "Filter Kubernetes events efficiently with kubectl events: --for an object, --types=Warning, watch mode, sorting, field selectors and JSON for scripts."
sources: ["https://kubernetes.io/docs/reference/kubectl/generated/kubectl_events/", "https://kubernetes.io/docs/reference/kubernetes-api/cluster-resources/event-v1/", "https://github.com/kubernetes/kubernetes/tree/master/staging/src/k8s.io/kubectl/pkg/cmd/events", "https://github.com/kubernetes/enhancements/tree/master/keps/sig-cli/1440-kubectl-events"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Filtering events

`kubectl events` (alpha 1.23, beta 1.26, stable 1.28 per KEP-1440) sorts by time and adds object filtering that `kubectl get events`
lacks.
```bash
kubectl events -n shop                                   # sorted oldest to newest
kubectl events -n shop --types=Warning                   # only warnings
kubectl events -n shop --for=pod/web-5d8c                # one object
kubectl events -n shop --for=deployment/web              # events for the Deployment object
kubectl events -A --types=Warning --watch                # live stream cluster-wide
```

## With kubectl get events
```bash
kubectl get events -A --field-selector type=Warning --sort-by=.lastTimestamp
kubectl get events -n shop --field-selector involvedObject.kind=Pod,reason=FailedMount
```
Supported event field selectors include `involvedObject.kind/name/namespace/uid`, `reason`,
`type`, `source`, `reportingComponent`.

## Useful Warning reasons
`FailedScheduling` (scheduler), `FailedMount`, `FailedAttachVolume`, `BackOff`, `Unhealthy`,
`NodeNotReady`, `FailedCreatePodSandBox` (kubelet), `FailedCreate` (workload controller could not create a Pod)
and `SyncLoadBalancerFailed` (cloud service controller).

`FailedCreate` on a ReplicaSet explains a Deployment that has no pods.
```bash
kubectl events -n shop --for=replicaset/web-5d8c --types=Warning
```

## Retention
Events last `--event-ttl` (default 1 h) on the API server. Ship them with an event exporter for
history.

## Checked
Checked 2026-10-24 against the kubectl events source (main), KEP-1440 metadata (alpha v1.23, beta v1.26, stable v1.28) and the kube-apiserver source (`--event-ttl` default 1 hour): flags `--for`, `--types`, `--watch`, `-A`, time sorting, the field-selector keys, and the event reason constants for kubelet, scheduler, ReplicaSet controller and cloud service controller. Removed the jq pipeline and the unconfirmed OOMKilling, Evicted and image-pull reasons.
Method: documentation only; no commands were run.
