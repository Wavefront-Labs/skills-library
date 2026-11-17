---
id: computing-software.cloud-infrastructure-engineering.kubernetes.readiness-during-shutdown
name: readiness-during-shutdown
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, probes, readiness-shutdown, readiness-probe, graceful-termination, terminating-endpoints]
level: practitioner
status: docs-checked
description: "What readiness means while a pod terminates: endpoint removal, serving and terminating conditions, and app-side shutdown sequencing to avoid dropped requests."
sources: ["https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/#conditions", "https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination", "https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Readiness during shutdown

## What Kubernetes does on pod deletion
1. Pod gets `deletionTimestamp`. In its EndpointSlice the endpoint gets `terminating: true`
   (so `ready` is false), while `serving` still follows the Pod's `Ready` condition.
2. Service proxies, ingress controllers and service meshes stop sending new traffic once they
   see the update; this propagation is asynchronous.
3. In parallel the kubelet runs preStop then sends SIGTERM.

So readiness does not need to flip for removal; deletion alone removes the pod from ready
endpoints. The race is step 2 lagging behind step 3.

## Where the readiness probe still matters
- `serving` condition: service proxies normally ignore terminating endpoints but may route to
  endpoints that are both `serving` and `terminating` when all available endpoints are
  terminating (this keeps traffic flowing during rolling updates). If the app keeps passing
  readiness while draining, it can keep receiving that fallback traffic.
- Load balancers that health-check pod IPs themselves (for example AWS Load Balancer Controller
  with IP targets) use readiness gates; see pod-conditions-and-readiness-gates.

## App-side sequence that works
1. On SIGTERM (or in preStop): start failing readiness, keep serving in-flight and new requests.
2. Wait for propagation (a few seconds, or your load balancer's deregistration delay).
3. Stop accepting, drain in-flight requests, close keep-alives (send `Connection: close`).
4. Exit before `terminationGracePeriodSeconds`.
If the app cannot do step 1-2, use a `preStop` sleep action (`lifecycle.preStop.sleep.seconds`, stable since 1.34); the value is yours to tune.

## Verify
```bash
kubectl get endpointslices -l kubernetes.io/service-name=web -o yaml | grep -A4 conditions
```
Run a load test during `kubectl rollout restart` and require zero 5xx.

## Checked

Documentation release checked: Kubernetes website v1.37 docs (kubernetes/website main, 2026-10-23). Confirmed in the EndpointSlice page: `terminating` is set when the Pod receives a deletion timestamp; `serving` maps to the Pod Ready condition; `ready` is `serving` and not `terminating`; proxies ignore terminating endpoints unless all are terminating, then may use serving-and-terminating ones. Pod lifecycle page: the kubelet runs `preStop` before sending TERM and the grace period covers both. Sleep action is stable in 1.34 (feature gate PodLifecycleSleepAction). AWS readiness-gate behaviour is from the aws-load-balancer-controller docs.
Removed: the ProxyTerminatingEndpoints gate name (stable and removed in 1.29), the externalTrafficPolicy-specific claim, GCP NEG remarks, and numeric propagation timings.

Method: documentation only; no commands were run.
