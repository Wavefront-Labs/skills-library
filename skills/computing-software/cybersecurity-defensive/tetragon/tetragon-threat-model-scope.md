---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-threat-model-scope
name: tetragon-threat-model-scope
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [threat-scope, tetragon, threat-model, architecture, operator]
level: advanced
status: docs-checked
description: "Understand the scope, deployment attack surface, agent and operator components in the Tetragon threat model before hardening a deployment."
sources:
  - "https://tetragon.io/docs/threat-model/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon threat model: scope and architecture

Goal: know what Tetragon's own attack surface is so you can protect the monitor itself.

## Scope
The model covers Kubernetes DaemonSet, standalone containerized and systemd-managed deployments. It assumes fully patched, hardened systems (including Kubernetes security best practices) and considers five attacker profiles: Kubernetes workload, limited-privilege host, root-equivalent host, Kubernetes API server, and network attacker. Using the wrong hook points in a tracing policy is a security/visibility risk, not a Tetragon vulnerability, so validate hook choices.

## Deployment surface
- Kubernetes: DaemonSet, an agent per node; relies on the Kubernetes API for policy distribution, so it depends on control plane security.
- Standalone (container or systemd): policy management and event collection need other mechanisms, with risks around local file access and network communications.

## Agent
The agent loads eBPF programs, collects events and enforces policy; its privileged position makes it a high-value target.
- Config in Kubernetes comes from the `TracingPolicy` and `TracingPolicyNamespaced` CRDs; strict RBAC is required. Standalone config is YAML on the host, protected by filesystem permissions.
- The optional gRPC endpoint listens on a Unix domain socket (better isolation) or a local network port; both need access control.
- Event export (stdout container logs, JSON log files, gRPC streams) needs controls protecting event confidentiality.
- The Prometheus metrics endpoint can disclose configuration, performance and operational state that aids reconnaissance.

## Operator
Manages CRD lifecycle and has privileged Kubernetes API access. It registers `TracingPolicy`, `TracingPolicyNamespaced` and `PodInfo`. `PodInfo` is a key-value store mapping Pod IPs to workload objects, used to attribute network activity. Operator compromise could allow cluster-wide policy manipulation.

## Checked

2026-11-08. Read the threat model page in full (raw docs markdown). Checked scope, deployment surface, agent and operator sections against it; no claims removed.

Method: documentation only; no commands were run.
