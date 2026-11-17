---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cold-start-mitigation-and-overprovisioning
name: cold-start-mitigation-and-overprovisioning
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cold-start, overprovisioning, pause-pods, priorityclass, preemption, image-pre-pull, daemonset, node-boot-time, warm-pool, cluster-autoscaler, karpenter]
level: advanced
status: docs-checked
description: "Cutting scale-up latency with low-priority pause pods, image pre-pulling, and warm node pools, layered against pod startup and node boot time separately."
sources: ["https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md", "https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/", "https://kubernetes.io/docs/concepts/containers/images/", "https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/preview/concepts/capacitybuffers.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cold-start mitigation and overprovisioning

**Goal:** shrink the time between "demand arrives" and "capacity is actually serving it," by
attacking each layer of cold-start latency separately — node boot, image pull, and application
startup are different problems with different fixes.

## 1. Decompose the cold-start, don't treat it as one number
A scale-up from zero/near-zero typically stacks:
1. **Detection latency** — the HPA controller syncs every 15s by default
   (`--horizontal-pod-autoscaler-sync-period`), and Cluster Autoscaler checks for unschedulable pods
   every 10s by default (`--scan-interval`). Predictive or scheduled scaling is the main lever
   here, not tuning the poll interval down (which has its own stability cost).
2. **Node boot time** — if no existing node has room, the cloud provider must launch an instance
   and the kubelet must register before pods can start; measure this on your own cloud and image.
3. **Image pull time** — if the node has never run this image, pulling a large image (ML and JVM
   images can be very large) can dominate total cold-start time on a cold node.
4. **Application startup** — JVM/runtime init, cache warmup, DB connection pool establishment,
   readiness probe's `initialDelaySeconds`/`periodSeconds` gating when the pod is actually marked
   Ready and receives traffic.
Each has its own fix; throwing more replicas at the problem only helps #1 and does nothing for #2-4.

## 2. The overprovisioning / pause-pod pattern (node boot latency)
Standard pattern documented in the Cluster Autoscaler FAQ (also usable with Karpenter, which can
instead use its alpha CapacityBuffer resource, documented in the Karpenter preview docs): run a
Deployment of trivial, low-priority placeholder pods (a `pause` image or any no-op image) with
requests sized like your real workload's pod, at a **low `PriorityClass`**:
```yaml
apiVersion: v1
kind: PriorityClass
metadata: {name: overprovisioning}
value: -10
globalDefault: false
---
# Deployment of N pause pods with priorityClassName: overprovisioning,
# resources.requests matching a real pod's shape
```
The FAQ reserves priority `-10` for overprovisioning pods: it is the lowest priority that still
triggers a scale-up (`--expendable-pods-priority-cutoff` defaults to `-10`, and pods below it are
expendable and cause no scale-up). Other pods need priority 0 or higher to preempt them.
These pods occupy node capacity that the autoscaler therefore keeps provisioned. When real,
higher-priority pods need room, the scheduler **preempts** the pause pods (no cloud API call is
needed to place the real pod), and the pause pods go back to `Pending`, which *then* triggers the autoscaler to
provision a **replacement** node for them — effectively pre-paying the node-boot latency for the
next scale-up instead of the current one. Size the pause-pod Deployment's replica count/resources
to match the burst capacity you want standing by; it has a direct, visible cost (you're paying for
idle nodes), so treat it as a cost/latency tradeoff, not a free win.

## 3. Image pre-pulling
- A `DaemonSet` running on every node (or every node in a target node pool/NodePool) with
  `initContainers` that just reference the production image (no need to run it, just pull) forces
  the image onto every node's local cache ahead of real scheduling. Works well combined with
  overprovisioning: pause-pod replacement nodes get the image pre-pulled before they're needed.
- Custom node images with the application image baked in (Karpenter's `EC2NodeClass` selects AMIs
  with `amiSelectorTerms`) remove pull time for the baked image, at the cost of maintaining an image
  pipeline kept in sync with app releases.
- `imagePullPolicy` defaults to `IfNotPresent` unless the tag is `:latest` or omitted, in which case
  it defaults to `Always`; pre-pulling only helps when the policy is `IfNotPresent`, so confirm it
  is not `Always` on hot-path workloads.

## 4. Application startup
- Lower `initialDelaySeconds` and tune `periodSeconds`/`failureThreshold` on readiness probes only
  as far as the app's real startup behaviour allows — making a probe optimistic before the app can
  actually serve traffic just shifts errors to users instead of removing them.
- A `startupProbe` (separate from readiness) lets you give slow-starting apps a long startup grace
  period without weakening the readiness probe's steady-state sensitivity — use both together
  rather than stretching one probe to cover two different concerns.
- JVM/runtime-level fixes (AppCDS/class-data sharing, lazy vs eager initialization, connection
  pool pre-warming in a startup hook rather than lazily on first request) are outside Kubernetes
  but often the single biggest lever for #4 — don't assume Kubernetes-level tuning alone solves
  slow app startup.

## Gotchas
- Pause pods must request the **same resource shape** as real workload pods or the autoscaler
  provisions the wrong node size/type when preempting them — a tiny pause pod doesn't reserve
  room for a large real pod.
- Preempted victims still receive their graceful termination period (Pod Priority and Preemption
  docs), and PodDisruptionBudgets are honoured only on a best-effort basis. Pause pods need no
  clean shutdown; if you repurpose the pattern with real low-priority workloads, handle
  `preStop`/SIGTERM and shorten their grace period.
- Pre-pulling via DaemonSet only helps nodes that **already exist** when the DaemonSet pod runs —
  a brand-new node from a scale-up still pulls on first boot unless combined with overprovisioned
  standing nodes or a baked AMI.
- Overprovisioning has a real, continuous cost (idle node capacity) — track it as a line item, not
  background noise, and revisit the sizing as traffic patterns change.

## Verify
- [ ] A forced scale-up event (synthetic load) shows the preempt-and-replace cycle for pause pods
      in `kubectl get events`, and the real pod schedules without waiting on a cold node boot.
- [ ] `kubectl describe node <new-node>` after a scale-up shows the target image already present
      (pre-pull/baked AMI working) rather than a fresh pull in the pod's `Events`.
- [ ] Readiness/startup probe timings are validated against real app startup logs, not guessed —
      a probe passing before the app can serve traffic is worse than a slightly conservative one.
- [ ] Overprovisioning node cost is visible in cost reporting and has an owner who reviews it
      against actual burst patterns periodically.

## Checked

Checked 2026-10-27. Documentation checked: Cluster Autoscaler FAQ (autoscaler master), Kubernetes website main tree (v1.38 dev; v1.37 latest release) for image pull policy defaults and probes, kube-controller-manager reference for the HPA sync period, Karpenter v1.15 docs (EC2NodeClass AMI selection) and Karpenter preview docs (CapacityBuffer, alpha). Confirmed: overprovisioning PriorityClass should be -10 (FAQ), CA scan interval 10s, HPA sync period 15s, imagePullPolicy defaults, startup probe purpose. Fixed: PriorityClass value was -1 and is now the FAQ value -10. Removed as unconfirmed: node boot and image pull timing figures, the claim Karpenter makes the pattern matter less, and sub-second preemption timing.

Method: documentation only; no commands were run.
