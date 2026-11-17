---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-audit-singleton-and-disabling
name: opa-gatekeeper-audit-singleton-and-disabling
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, audit, singleton, generate, disable-audit, status-contention, helm]
level: advanced
status: docs-checked
description: "Understand why Gatekeeper audit must be a singleton and how to disable only the audit operation without breaking CRD generation or status."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/audit.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper audit singleton and disabling

Audit writes results into Constraint status, so multiple audit instances contend on the same fields. From v3.18 the audit deployment may also run the `generate` operation, which creates and updates Constraint CRDs and, if enabled, ValidatingAdmissionPolicy and binding resources; that operation must also be a singleton.

If you only consume results from logs or exports, `--constraint-violations-limit=0` stops storing individual violations in `.status.violations`. It does not remove all status writes: `.status.auditTimestamp` and `.status.totalViolations` are still updated, so replicas can still contend. If you scale audit beyond one replica, run `generate` on only one instance (Helm `audit.disableGenerateOperation=true`) and handle VAP/VAPB generation in a singleton or turn it off with `defaultCreateVAPForTemplates=false` and `defaultCreateVAPBindingForConstraints=false`.

To save CPU or memory by turning audit off, do not remove the deployment with `disableAudit: true`: the audit pod also handles CRD generation and status aggregation. Instead disable just the operation: Helm `audit.disableAuditOperation: true`, or remove the `--operation=audit` flag from the manifest.

## Checked

2026-11-08. Confirmed against audit.md, read in full (Running Audit, Why Audit Runs as a Singleton, Disabling Audit): contention on Constraint status, v3.18 generate operation, constraint-violations-limit=0 behaviour, Helm audit.disableGenerateOperation, VAP generation flags, disableAudit warning, audit.disableAuditOperation and --operation=audit. Removed or corrected: nothing.

Method: documentation only; no commands were run.
