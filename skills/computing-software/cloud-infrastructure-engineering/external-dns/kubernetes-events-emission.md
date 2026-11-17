---
id: computing-software.cloud-infrastructure-engineering.external-dns.kubernetes-events-emission
name: kubernetes-events-emission
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, events-emit, kubernetes-events, record-error, kubectl-events, alpha-feature]
level: practitioner
status: docs-checked
description: "Read ExternalDNS Kubernetes Events (alpha): kubectl field selectors, action, reason and type fields, RecordError, and the caveats on retention and deletion events."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/advanced/events.md
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/advanced/operational-best-practices.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ExternalDNS Kubernetes Events

Events are an alpha feature: they show what was created, updated or deleted and surface errors on the Service or Ingress that caused them. Enable error events with `--events-emit=RecordError`.

```sh
kubectl describe service <name>
kubectl get events --field-selector involvedObject.kind=Service
kubectl get events --field-selector type=Normal|Warning
kubectl get events --field-selector reason=RecordReady|RecordDeleted|RecordError
kubectl get events --field-selector reportingComponent=external-dns
```

- **Action:** `Created`, `Updated`, `Deleted`, `FailedSync`.
- **Reason:** `RecordReady`, `RecordDeleted`, `RecordError`.
- **Type:** `Normal` means success; `Warning` means a problem.
- Repeated identical events may indicate a misconfiguration.

**Flow:** the Source emits Endpoints with a reference object, the Plan applies changes through the Provider, each Endpoint is labelled Success, Failed or Skip, and an Event is emitted against the referenced object.

**Caveats**
- Events are ephemeral (default retention about one hour) and best-effort, so they complement logs and metrics rather than replace them.
- `RecordDeleted` events carry no UID, so `kubectl describe` misses them; use `kubectl get events -n <namespace>`.
- `unstructured` source kinds are lowercase (for example `virtualmachineinstance`).
- Records without a registry `resource` label (for example `--registry=noop`) emit none.
- `DNSEndpoint` validation failures appear in status conditions, not events.

## Checked

2026-11-04. Confirmed against the ExternalDNS Kubernetes Events page (consuming events, field meanings, sequence, caveats) and the Operational Best Practices page (events-emit RecordError, DNSEndpoint status conditions). Nothing removed.
Method: documentation only; no commands were run.
