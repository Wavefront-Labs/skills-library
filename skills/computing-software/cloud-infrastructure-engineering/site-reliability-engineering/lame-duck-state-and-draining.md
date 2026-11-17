---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.lame-duck-state-and-draining
name: lame-duck-state-and-draining
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [lame-duck-state, lame-duck-draining, graceful-shutdown, prestop, readiness-probe, connection-draining, load-balancing]
level: practitioner
status: docs-checked
description: "Implement lame duck mode so backends drain cleanly: enter lame duck on SIGTERM, finish in-flight work, then exit; Kubernetes preStop hooks, readiness and grace periods."
sources: ["https://sre.google/sre-book/load-balancing-datacenter/", "https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/", "https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lame duck state and draining

SRE Book "Load Balancing in the Datacenter": a backend has three states from the client's view: healthy,
refusing connections, and **lame duck**: listening and able to serve, but explicitly asking clients to
stop sending requests. Lame duck lets a task shut down without failing the requests that were in flight.

## Shutdown sequence (as the SRE Book describes it)
1. The scheduler sends SIGTERM to the backend task.
2. The task enters lame duck state and asks clients to send new requests elsewhere; the RPC layer exposes a
   call that the SIGTERM handler invokes.
3. Requests started before lame duck (or after it but before a client noticed) execute normally.
4. As responses flow back, active requests fall to zero.
5. After a configured interval the task exits cleanly or the scheduler kills it. Set the interval long enough
   for typical requests to finish; the book's rule of thumb is between 10s and 150s depending on client complexity.

## Kubernetes implementation
Termination is not instant: when a Pod is deleted, the kubelet runs any `preStop` hook, then sends the stop
signal (SIGTERM by default). Meanwhile the control plane removes the Pod from EndpointSlices at the same time,
and a failed readiness probe also removes the Pod's IP from matching Services. The default
`terminationGracePeriodSeconds` is 30 seconds; if a `preStop` hook needs longer, raise it. The hook
actions include `exec`, `httpGet` and `sleep` (a pause for a set duration).
```yaml
spec:
  terminationGracePeriodSeconds: 45
  containers:
  - name: api
    readinessProbe:
      httpGet: { path: /readyz, port: 8080 }
      periodSeconds: 2
      failureThreshold: 1
    lifecycle:
      preStop:
        sleep: { seconds: 10 }      # check your cluster version supports the sleep action; else exec: ["sleep","10"]
```
In the application's SIGTERM handler: make the readiness endpoint fail, stop accepting new work, and
wait for active requests up to a deadline before exiting.
Budget: preStop duration + max request duration < terminationGracePeriodSeconds.

## Other layers
Proxies, gRPC servers and cloud load balancers each have their own drain or deregistration setting
(connection draining, deregistration delay, GOAWAY-style signals). Look up the exact setting in that
product's documentation. For long-lived connections (WebSockets, streams), tell clients to reconnect,
spread over the drain window.

## Gotchas
- Without a delay, rolling updates can send traffic to a Pod that is already shutting down.
- Readiness failing during startup also counts; separate startup, readiness and liveness probes.
- Lame duck too long slows rollouts; measure your slowest normal requests and set accordingly.

## Verify
- [ ] Rolling restart under load shows no errors at the load balancer.
- [ ] Deleting a busy pod completes in-flight requests (test with long requests).

## Checked
2026-11-01. Confirmed against the SRE Book chapter (lame duck states, shutdown steps, 10s-150s rule of thumb)
and the Kubernetes lifecycle-hooks and pod-termination pages (preStop, sleep action, 30 s default grace
period, EndpointSlice removal on readiness failure). Removed: Kubernetes version gate for sleep, the Go
snippet, Envoy admin endpoints and flags, gRPC and AWS API names, and "several health-check intervals"
(no fetched page states them).
Method: documentation only; no commands were run.
