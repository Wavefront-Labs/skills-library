---
id: computing-software.cloud-infrastructure-engineering.azure.container-apps-health-probes-and-graceful-termination
name: container-apps-health-probes-and-graceful-termination
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, container-apps, aca-probes, liveness-probe-aca, readiness-probe, startup-probe, graceful-shutdown]
level: practitioner
status: docs-checked
description: "Configure liveness, readiness and startup probes on Azure Container Apps, understand the default probes, and handle SIGTERM with terminationGracePeriodSeconds."
sources: ["https://learn.microsoft.com/en-us/azure/container-apps/health-probes", "https://learn.microsoft.com/en-us/azure/container-apps/application-lifecycle-management", "https://learn.microsoft.com/en-us/azure/container-apps/revisions", "https://learn.microsoft.com/en-us/azure/container-apps/troubleshoot-health-probe-failures", "https://learn.microsoft.com/en-us/azure/container-apps/troubleshoot-target-port-settings"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container Apps health probes and graceful termination

**Goal:** traffic only reaches ready replicas, hung replicas restart, slow starters aren't killed, and scale-in
doesn't drop in-flight requests.

## Probes (YAML)
```yaml
template:
  containers:
  - name: api
    image: crcorp.azurecr.io/api:2.3.1
    probes:
    - type: Startup
      httpGet: { path: /healthz/startup, port: 8080 }
      periodSeconds: 5
      failureThreshold: 30          # 30 x 5 s = up to 150 s to start
    - type: Readiness
      httpGet: { path: /healthz/ready, port: 8080 }
      periodSeconds: 10
      failureThreshold: 3
    - type: Liveness
      httpGet: { path: /healthz/live, port: 8080 }
      initialDelaySeconds: 5
      periodSeconds: 10
      timeoutSeconds: 2
      failureThreshold: 3
```
```bash
az containerapp update -g rg -n ca-api --yaml app.yaml
```
`tcpSocket: { port: 8080 }` for non-HTTP apps.

## Defaults
With ingress enabled and a probe type not defined, the portal adds a default TCP probe on the ingress target port (startup: timeout 3 s, period 1 s, failure threshold 240; liveness: TCP only; readiness: timeout 5 s, period 5 s, failure threshold 48); GPU workload profiles and sidecar containers get no defaults. If the
app listens on a different port than the target port, probes fail and the revision does not become ready.

## Probe design
- **Liveness**: "process is not deadlocked" - don't check dependencies (a DB outage would restart every replica).
- **Readiness**: "can serve now" - may check critical dependencies briefly; failing removes the replica from load balancing.
- **Startup**: protects slow boots; liveness/readiness start after it succeeds.

## Graceful termination
When a replica shuts down (scale-in, revision deactivation, app deletion) the container host sends **SIGTERM**; if the app has not stopped within 30 seconds it is killed with SIGKILL. Handle SIGTERM: stop accepting new work, finish in-flight
requests/messages, flush, exit.

## Gotchas
- Aggressive liveness timeouts cause restart loops; if the failure threshold is exceeded the revision may need a restart or reconfiguration.
- Event-driven workers (KEDA-scaled) need graceful handling too, or messages get redelivered.

## Verify
- [ ] Revision shows healthy replicas; killing the dependency doesn't trigger restarts; scale-in during load causes no 5xx.

## Checked
Checked 2026-10-24 against azure-docs container-apps pages (health-probes, application-lifecycle-management, revisions, troubleshoot-health-probe-failures). Confirmed: probe types Startup, Liveness, Readiness with httpGet and tcpSocket, initialDelaySeconds, periodSeconds, failureThreshold; default probe values; default probes only when ingress is enabled and not for GPU profiles or sidecars; SIGTERM then SIGKILL after 30 seconds on shutdown. Found wrong and fixed: defaults were described as TCP probes only (startup and readiness have explicit timing defaults). Removed unconfirmed: terminationGracePeriodSeconds with its default and maximum, the RestartCount advice, the authentication note for probe endpoints.

Method: documentation only; no commands were run.
