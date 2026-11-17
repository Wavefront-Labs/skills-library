---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.disposability
name: disposability
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, 12-factor-app, twelve-factor, disposability, graceful-shutdown, sigterm, fast-startup, crash-only, prestop-hook, termination-grace-period, connection-draining]
level: practitioner
status: docs-checked
description: "Apply factor IX: fast startup and graceful SIGTERM shutdown so instances can be killed at any time — signal handling, draining, preStop hooks and crash-only job design."
sources: ["https://12factor.net/disposability", "https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination", "https://cloud.google.com/run/docs/container-contract#instance-shutdown"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Factor IX — Disposability

Processes start fast and stop gracefully; they can be started or stopped at a moment's notice (scale-in, deploys,
node drain) without losing work.

## Startup
- Aim for a few seconds from launch command to ready for requests or jobs (12factor.net). Short startup makes
  scaling and rescheduling easier.
- Run migrations as a separate admin process rather than at boot.

## Shutdown sequence (Kubernetes)
1. Pod is granted a graceful termination period (`terminationGracePeriodSeconds`, default 30 seconds).
2. A `preStop` hook, if configured, runs inside the container first. If it needs longer than the grace period allows,
   raise `terminationGracePeriodSeconds`.
3. Containers receive the TERM signal. Meanwhile the control plane stops treating the Pod as in-service, but
   terminating endpoints are not removed from EndpointSlices immediately (their ready status is false), so a short
   preStop delay or serving-condition check is how you drain.
4. When the grace period expires, the container runtime sends SIGKILL to anything still running.

## Implementation checklist
- Web process: stop listening on the service port, let current requests finish, then exit (12factor.net). Cloud Run
  likewise sends SIGTERM and then SIGKILL after a 10-second period; install a SIGTERM handler.
- Make sure your container's main process actually receives SIGTERM (test it; do not assume a shell wrapper forwards it).
- Workers: return the current job to the queue (for example a NACK); jobs must be reentrant (transaction or
  idempotent). Be robust against sudden death too ("crash-only" design).

## Verify
- [ ] Rolling deploy under load: no failed requests or connection resets.
- [ ] Kill a worker mid-job: the job completes on another worker without double effects.

## Checked
2026-11-01. Confirmed in 12factor.net Disposability (startup, SIGTERM, web and worker shutdown, crash-only), the
Kubernetes Pod lifecycle page (30-second default, preStop, endpoint removal not immediate, SIGKILL after grace period)
and the Cloud Run container contract (SIGTERM then SIGKILL after 10 seconds). Removed: `sleep 5-10`, exec-form/tini
claims, per-framework shutdown calls, spot interruption notice times.
Method: documentation only; no commands were run.
