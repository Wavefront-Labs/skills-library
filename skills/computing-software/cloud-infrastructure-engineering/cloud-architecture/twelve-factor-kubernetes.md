---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.twelve-factor-kubernetes
name: twelve-factor-kubernetes
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, twelve-factor-build, twelve-factor-kubernetes, twelve-factor, kubernetes, configmaps, secrets, graceful-shutdown]
level: practitioner
status: docs-checked
description: "Map twelve-factor practices onto Kubernetes: ConfigMaps for config, Services for backing services, SIGTERM and preStop handling, Jobs for admin tasks."
sources: ["https://12factor.net/", "https://kubernetes.io/docs/concepts/configuration/configmap/", "https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination", "https://kubernetes.io/docs/concepts/workloads/controllers/job/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Twelve-factor on Kubernetes

## Factor to Kubernetes mapping
The twelve factors (12factor.net) are: I Codebase, II Dependencies, III Config (store config in the environment),
IV Backing services (attached resources), V Build/release/run (strictly separate build and run), VI Processes
(stateless), VII Port binding, VIII Concurrency (scale out via the process model), IX Disposability, X Dev/prod
parity, XI Logs (event streams), XII Admin processes (one-off).

Kubernetes features that map onto them, as documented:
| Factor | Kubernetes practice |
|---|---|
| III Config | ConfigMaps consumed as environment variables, command-line arguments or files in a volume; same code runs locally and in the cloud by changing the variable (for example a database host pointing at a Service) |
| IV Backing services | reach the backing service through a Service name set in config |
| IX Disposability | handle the TERM signal; optional `preStop` hook; `terminationGracePeriodSeconds` (default 30 seconds) before SIGKILL |
| XII Admin processes | run one-off tasks as a `Job` from the same image |
Other factors (build once and promote, stateless pods, logs to stdout, parity) follow 12factor.net directly; choose
tooling for them yourself.

## Steps
1. Audit each app against the twelve factors; record gaps as backlog items.
2. Config changes: ConfigMaps consumed as environment variables are not updated automatically and need a pod
   restart; mounted ConfigMaps are updated automatically (Kubernetes ConfigMap page). Plan rollouts accordingly.
3. Test shutdown: send SIGTERM during load and check no requests are dropped.

## Verify
- [ ] A config change reaches running pods by the mechanism you chose (restart or volume update).
- [ ] Rolling update under load shows no failed requests.

## Checked
2026-11-01. Confirmed in 12factor.net (factor titles), the Kubernetes ConfigMap page (consumption modes, env vars not
auto-updated, mounted ones are), the Pod lifecycle page (30-second default grace period, preStop, SIGKILL) and the Job
page. Removed: digest pinning, distroless, External Secrets/CSI, Helm/Kustomize/Argo, HPA/KEDA, Fluent Bit, kind/k3d,
Secrets base64 claim, shell-form entrypoint claim, per-factor tooling table rows.
Method: documentation only; no commands were run.
