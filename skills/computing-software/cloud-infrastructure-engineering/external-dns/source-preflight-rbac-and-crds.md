---
id: computing-software.cloud-infrastructure-engineering.external-dns.source-preflight-rbac-and-crds
name: source-preflight-rbac-and-crds
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, rbac-watch-permission, preflight-validation, missing-crd, context-deadline-exceeded, dry-run-once]
level: advanced
status: docs-checked
description: "Prevent silent ExternalDNS staleness: install CRDs first, grant list and watch RBAC, scope sources per cluster, and validate in CI with --dry-run --once."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/advanced/operational-best-practices.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Source preflight: CRDs and RBAC

ExternalDNS fails fast when a configured source cannot initialise. That is intentional: a crashloop is an explicit signal. The danger is failures that are not clean.

| Misconfiguration | Symptom |
|---|---|
| CRD not installed | `context deadline exceeded` after about 60s; no "CRD not found" message |
| No LIST permission | `403 Forbidden`, exit |
| LIST allowed, WATCH denied | starts and looks healthy, but never gets updates; records drift silently |
| Admission webhook misconfigured | source initialises; changes are silently rejected |

**Practices**
- Only configure `--source=` types whose CRDs are installed and RBAC granted. For Gateway API, Istio or the CRD source, install CRDs first and confirm `kubectl get crd <name>` shows established.
- Grant `list` and `watch` for every resource each source needs.
- Keep RBAC minimal: excess rights hide misconfiguration.
- Use per-cluster source lists in Helm or Argo CD values, for example `sources: [service, gateway-httproute]` on one cluster and `[service, ingress]` on another.
- Validate in CI against staging with the same CRD and RBAC profile:

```sh
external-dns --dry-run --once ...
```

`--once` alone applies real DNS changes, so always pair it with `--dry-run`.

## Checked

2026-11-04. Confirmed against the ExternalDNS Operational Best Practices page (Source Configuration and Preflight Validation): failure-mode table, practices, per-cluster source lists and the dry-run advice. Nothing removed.
Method: documentation only; no commands were run.
