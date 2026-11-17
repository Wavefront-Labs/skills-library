---
id: computing-software.cloud-infrastructure-engineering.cilium.hubble-deployment-troubleshooting
name: hubble-deployment-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, hubble, relay, crashloopbackoff, hubble-peer, cilium-status]
level: advanced
status: docs-checked
description: "Troubleshoot Hubble and Relay using cilium status warnings, pod describe and logs, and the hubble-peer connection refused error."
sources:
  - https://docs.cilium.io/en/stable/observability/hubble/setup/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Troubleshooting Hubble deployment

Start with `cilium status`. Unhealthy Relay shows e.g. `Hubble Relay: 1 errors, 2 warnings`, with lines such as `1 pods of Deployment hubble-relay are not ready` and `pod is pending`.

Steps:
1. `kubectl -n kube-system get pods -l k8s-app=hubble-relay` (look for CrashLoopBackOff).
2. Pending pods: `kubectl describe -n kube-system pod/<name>`.
3. Not Running: `kubectl -n kube-system logs <relay-pod>`. Repeated `Failed to create peer notify client for peers change notification` means Relay cannot reach the Hubble API on the agents through the `hubble-peer` service (`connection refused`); check port 4244 and Hubble on the agents.
4. For TLS errors use the Hubble TLS troubleshooting section.

Key fact: Hubble is a non-critical subsystem of the agent. Agents stay running and healthy even when Hubble fails to start, so a warning on the Cilium line with a Relay error points to Hubble misconfiguration. Example warning: `Hubble: failed to setup metrics: metric 'unknown-metric' does not exist`. Check agent pods with `kubectl -n kube-system get pods -l k8s-app=cilium` and describe or read their logs.

## Checked

2026-11-03. Claims were read against: https://docs.cilium.io/en/stable/observability/hubble/setup/. 

Method: documentation only; no commands were run.
