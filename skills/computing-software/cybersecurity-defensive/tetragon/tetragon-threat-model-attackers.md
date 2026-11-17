---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-threat-model-attackers
name: tetragon-threat-model-attackers
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [threat-attackers, tetragon, threat-actors, hardening, rbac]
level: advanced
status: docs-checked
description: "Apply the Tetragon threat model attacker profiles and recommended controls to harden sockets, event files, RBAC, the operator and exports."
sources:
  - "https://tetragon.io/docs/threat-model/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tetragon threat actors and controls

Goal: for each attacker profile, know the risk and the control the threat model recommends.

## Kubernetes workload attacker
Can only generate event floods (denial of service); cannot alter Tetragon's eBPF programs or config. Controls: alert on dropped events via health metrics `tetragon_events_total`, `tetragon_observer_ringbuf_events_lost_total`, `tetragon_map_in_use_gauge`, `tetragon_bpf_missed_events_total`. Event throttling limits per-cgroup rates and emits a `THROTTLE_START` event; watch for it (it may also be a legitimate busy workload).

## Limited-privilege host attacker
- Access to the gRPC Unix socket `/var/run/tetragon/tetragon.sock` (default permissions `0660`) lets them read and change tracing policies. Do not run containers with the agent's user and group IDs; keep the default permissions.
- gRPC on a network port is generally unsuitable for production without robust authentication; move to a Unix socket.
- Event export files should stay `0600`; stream over gRPC with access controls if several processes need them.
- A `CAP_SYS_BPF` holder can load arbitrary eBPF; Tetragon cannot stop successful verifier bypasses.

## Kubernetes API server attacker
Read access to the CRDs exposes the monitoring posture; write access can delete policies or add noisy ones. Control: least-privilege RBAC, limit read to security/operations, tighter write, possibly multi-person approval.

## Root-equivalent host attacker
Nothing local can be trusted: the attacker can unload eBPF programs, redirect exports or inject false events, and can extract the agent's service account token. Credentials and capabilities are recorded only at exec time for the main thread, so later setuid/setgid/capability changes will not appear in events. Control: schedule the Tetragon Operator on control plane nodes only (node selectors, taints, tolerations), not alongside untrusted workloads.

## Network attacker
Intercepts exports or metrics. Controls: encrypt all exports (HTTPS, valid certificates) and enable TLS on the Prometheus endpoint with authenticated scrapers.

## Operations
Protect event data (access controls, encryption, retention); put policy changes under review and test in non-production; filter, aggregate and enrich events to avoid alert fatigue.

## Checked

2026-11-08. Read the threat model page in full (raw docs markdown). Checked each attacker profile and recommended control against it; no claims removed.

Method: documentation only; no commands were run.
