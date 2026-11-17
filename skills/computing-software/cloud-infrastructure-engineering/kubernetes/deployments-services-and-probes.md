---
id: computing-software.cloud-infrastructure-engineering.kubernetes.deployments-services-and-probes
name: deployments-services-and-probes
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubectl, deployment, service, clusterip, readiness-probe, liveness-probe, startup-probe, resource-requests, resource-limits, oomkilled, cpu-throttling, rolling-update, maxsurge, maxunavailable, poddisruptionbudget, rollout-undo, crashloopbackoff, kubectl-debug, endpointslices, graceful-shutdown, prestop, topology-spread]
level: practitioner
status: docs-checked
description: "Ship a Kubernetes workload that rolls out safely: Deployment and Service, sane requests/limits, correct liveness/readiness/startup probes, PDBs and a kubectl debugging routine."
sources: ["https://kubernetes.io/docs/concepts/workloads/controllers/deployment/", "https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/", "https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/", "https://kubernetes.io/docs/concepts/workloads/pods/disruptions/", "https://kubernetes.io/docs/tasks/run-application/configure-pdb/", "https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/", "https://kubernetes.io/docs/concepts/workloads/pods/pod-qos/", "https://github.com/kubernetes/kubernetes/blob/release-1.37/staging/src/k8s.io/api/core/v1/types.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubernetes Deployments, Services and probes — zero-downtime by construction

**Goal:** a Deployment that only receives traffic when ready, is restarted only when
truly stuck, survives node drains, and that you can debug in minutes when it fails.

## 1. The core manifest
```yaml
apiVersion: apps/v1
kind: Deployment
metadata: {name: api, labels: {app: api}}
spec:
  replicas: 3
  revisionHistoryLimit: 5
  strategy: {type: RollingUpdate, rollingUpdate: {maxSurge: 25%, maxUnavailable: 0}}
  selector: {matchLabels: {app: api}}          # immutable after creation
  template:
    metadata: {labels: {app: api}}
    spec:
      terminationGracePeriodSeconds: 30
      topologySpreadConstraints:
      - {maxSkew: 1, topologyKey: topology.kubernetes.io/zone, whenUnsatisfiable: ScheduleAnyway, labelSelector: {matchLabels: {app: api}}}
      containers:
      - name: api
        image: registry.example.com/api@sha256:<DIGEST>
        ports: [{name: http, containerPort: 8080}]
        resources:
          requests: {cpu: 250m, memory: 256Mi}
          limits:   {memory: 256Mi}
        startupProbe:   {httpGet: {path: /healthz, port: http}, periodSeconds: 5, failureThreshold: 30}
        readinessProbe: {httpGet: {path: /ready,   port: http}, periodSeconds: 5, failureThreshold: 2}
        livenessProbe:  {httpGet: {path: /healthz, port: http}, periodSeconds: 10, failureThreshold: 3}
        lifecycle: {preStop: {sleep: {seconds: 5}}}
---
apiVersion: v1
kind: Service
metadata: {name: api}
spec:
  selector: {app: api}
  ports: [{name: http, port: 80, targetPort: http}]
```

## 2. Requests and limits
- **Requests** drive scheduling and HPA utilisation percentages; set them from observed usage.
- **Memory limit = memory request** for predictable behaviour; a container that exceeds its
  memory limit can be OOM-killed (reason `OOMKilled`, exit code 137).
- **CPU limits** are enforced by throttling: the container cannot use more CPU than its limit
  even if the node has spare capacity. Many teams set CPU requests only.
- Requests = limits for CPU and memory in every container gives **Guaranteed** QoS, the class
  least likely to be evicted under node pressure.
- Make language runtimes respect the container memory limit (JVM and Go both have settings
  for this).

## 3. Probes — each has one job
- **startupProbe**: covers slow boot; no other probes run until it succeeds.
  Budget = `periodSeconds × failureThreshold` (150 s above).
- **readinessProbe**: "can I serve now?" Failing removes the pod from EndpointSlices; it
  is *not* restarted. May check critical local dependencies briefly.
- **livenessProbe**: "am I wedged beyond recovery?" Failing restarts the container.
  Must check **only the process itself** — never the database or downstream APIs.
- Defaults if omitted: `periodSeconds: 10`, `timeoutSeconds: 1`, `failureThreshold: 3`.
  A 1 s timeout is often too tight for a busy process; raise it deliberately.

## 4. Rollouts and disruption
- `maxUnavailable: 0` + readiness probe means capacity never drops during a rollout.
- `minReadySeconds: 10` catches pods that crash shortly after becoming ready.
- `kubectl rollout status deploy/api --timeout=5m`, `kubectl rollout history deploy/api`,
  `kubectl rollout undo deploy/api --to-revision=<N>`.
- PodDisruptionBudget so drains and upgrades keep capacity:
  `spec: {maxUnavailable: 1, selector: {matchLabels: {app: api}}}`. PDBs limit evictions
  (drains); they do not limit the Deployment's own rolling update.
- Graceful shutdown: endpoint removal starts at the same time as the kubelet begins graceful
  shutdown, so a `preStop` sleep (the native `sleep` action is stable since 1.34, beta and on by
  default from 1.30; older clusters use `exec: {command: ["sleep","5"]}`) delays SIGTERM until
  load balancers stop sending traffic.

## 5. Debugging routine
```bash
kubectl get pods -l app=api -o wide
kubectl describe pod <POD>                # Events: probe failures, OOMKilled, image pull, scheduling
kubectl logs <POD> --previous             # logs of the crashed container
kubectl get endpointslices -l kubernetes.io/service-name=api
kubectl debug -it <POD> --image=busybox:<tag> --target=api   # ephemeral container sharing namespaces
kubectl events --for pod/<POD>
kubectl top pod -l app=api                # needs metrics-server
```
- `Pending`: insufficient requests capacity, taints, PVC zone mismatch.
- `CrashLoopBackOff`: app exits; check `--previous` logs and `Last State` reason.
- Service returns nothing: selector does not match pod labels, or `targetPort` wrong — empty EndpointSlice.

## Gotchas
- Liveness checking a shared dependency turns one DB blip into a fleet-wide restart storm.
- Same endpoint for liveness and readiness with no startup probe → slow boots get killed repeatedly.
- A PDB with `minAvailable` equal to replicas (or `maxUnavailable: 0`) means zero voluntary
  evictions, so node drains never complete.
- `kubectl apply` with a changed `selector` fails; you must delete and recreate the Deployment.
- HPA plus a hard-coded `replicas` in Git: every apply resets the count. Omit `replicas` when HPA owns it.
- `latest` tags with `imagePullPolicy: IfNotPresent` give different code on different nodes.

## Verify
- [ ] `kubectl rollout restart` completes with zero failed requests under load.
- [ ] Liveness probe passes with all dependencies down; readiness fails appropriately.
- [ ] Every container has memory request = limit and a CPU request.
- [ ] `kubectl drain` on a node succeeds and the PDB keeps at least N-1 pods serving.
- [ ] Service EndpointSlice lists exactly the ready pods.
- [ ] `kubectl rollout undo` tested once in staging.

Related: computing-software.cloud-infrastructure-engineering.docker.multi-stage-dockerfiles

## Checked
Checked 2026-10-27 against kubernetes/website (main tree, v1.38 development; latest release
v1.37) and the core/v1 API types in kubernetes/kubernetes release-1.37: probe defaults
(timeoutSeconds 1, periodSeconds 10, failureThreshold 3) and startupProbe blocking other probes
(core/v1 types), CPU limits enforced by throttling and `OOMKilled` exit code 137 (Resource
Management), Guaranteed QoS least likely to be evicted (Pod QoS), PDB zero voluntary evictions
blocking drains (Configure PDB), PDBs not limiting rolling updates (Disruptions), endpoint
removal concurrent with graceful shutdown (Pod Lifecycle), PodLifecycleSleepAction stages
(alpha 1.29, beta 1.30, stable 1.34), `kubectl debug --target`, `kubectl events --for`, and
removing `spec.replicas` under an HPA. Removed an unconfirmed cAdvisor metric name, specific
JVM/Go flags and a pinned debug image tag; fixed the `exec` preStop syntax; replaced prose
`sources:` titles with URLs.

Method: documentation only; no commands were run.
