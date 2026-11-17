---
id: computing-software.cloud-infrastructure-engineering.external-dns.state-conflicts-and-crashloops
name: state-conflicts-and-crashloops
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, conflict-error, http-409, crashloop-amplification, record-ownership, scale-to-zero]
level: advanced
status: docs-checked
description: "Handle ExternalDNS provider conflict errors (HTTP 409): why it will not auto-correct, how a hard exit amplifies into API throttling, and the fix checklist."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/advanced/operational-best-practices.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# State conflicts and crashloops

A provider conflict error (HTTP 409 or equivalent) means current DNS state does not match what ExternalDNS expects. The docs call it a state problem, not a software bug. ExternalDNS has no general conflict resolution: it drops some well-known invalid records (such as CNAME self-references) but does not apply a subset or auto-correct, because that could remove records services depend on. Retrying the same request without changing input or external state will deterministically fail.

**Crashloop amplification.** If the conflict causes a hard exit, kubelet restarts the pod, informers re-LIST Services, Pods, EndpointSlices and Nodes, and the same batch is retried. On large clusters this can throttle the Kubernetes API for other controllers too.

**Fix the state**
- Make one instance own each zone or record set. With the TXT or DynamoDB registry, use a distinct `--txt-owner-id` per instance and avoid overlapping `--domain-filter` scopes.
- Remove or update conflicting records at the provider.
- Review annotations for invalid definitions, for example CNAME mixed with A/AAAA on one hostname, or a CNAME pointing at itself.
- Look for other controllers or automation writing to the same zone.
- During a migration or incident, scale ExternalDNS to zero until state is reconciled, then scale up.

**Detect:** alert on pod restarts and `CrashLoopBackOff`, since the soft-error metric does not count hard exits.

## Checked

2026-11-04. Confirmed against the ExternalDNS Operational Best Practices page (State Conflicts and Ownership): conflict semantics, crashloop amplification, the fix list and the restart alerting advice. Nothing removed.
Method: documentation only; no commands were run.
