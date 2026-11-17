---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-audit-reading-results
name: opa-gatekeeper-audit-reading-results
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, audit, metrics, constraint-status, audit-logs, violations, event-type]
level: practitioner
status: docs-checked
description: "Read Gatekeeper audit results from Prometheus metrics, Constraint status or structured audit logs, and know the limits of each."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/audit.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper audit reading results

Audit periodically evaluates existing resources against constraints. Three ways to read results:

1. Prometheus metrics: `gatekeeper_audit_last_run_time`, `gatekeeper_audit_last_run_end_time` and `gatekeeper_violations` (count for the last run, by severity).
2. Constraint `status`: only the most recent run, capped per constraint because Kubernetes limits object size. Excess violations are counted in `totalViolations` but not listed. The cap is `--constraint-violations-limit` (default 20); the docs recommend at most 500 to stay under the default etcd limit of 1.5MB per resource and to limit audit pod memory.
3. Audit logs: the audit pod writes JSON to stdout. Entries have `process: audit`, an `audit_id` identifying the run, and `event_type: violation_audited`, plus the constraint kind, name, action and the resource group, version, kind, namespace, name and labels. Other event types are `audit_started`, `constraint_audited` (with violation count) and `audit_finished`, all sharing the `audit_id`.

Log drawback: violation lines are mixed with other log output. Status drawback: truncation. A fourth option, exporting violations to a message system, avoids both limits but can drop messages and adds a backend dependency.

## Checked

2026-11-04. Confirmed against audit.md (Reading Audit Results, audit log fields, other event types). Removed or corrected: wording corrected from 'request limit' to the page's 'per resource'.

Method: documentation only; no commands were run.
