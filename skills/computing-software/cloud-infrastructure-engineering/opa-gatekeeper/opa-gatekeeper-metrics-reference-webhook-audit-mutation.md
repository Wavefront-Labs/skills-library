---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-metrics-reference-webhook-audit-mutation
name: opa-gatekeeper-metrics-reference-webhook-audit-mutation
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, metrics, prometheus, gatekeeper-violations, validation-request-count, audit-duration, observability]
level: practitioner
status: docs-checked
description: "Alert on Gatekeeper health with its Prometheus metrics for constraints, webhook latency, audit runs, mutators, sync, watches and external data."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/metrics.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper metrics reference webhook audit mutation

Key metric families (counters may need a `_total` suffix depending on the client library):
- Constraints: `gatekeeper_constraints` by `enforcement_action` (deny, dryrun, warn) and `status` (active, error); `gatekeeper_constraint_templates`, ingestion count and duration, and `gatekeeper_constraint_templates_with_cel`.
- Webhook: `gatekeeper_validation_request_count` (by `admission_status` allow/deny and `admission_dryrun`), `gatekeeper_validation_request_duration_seconds`, plus mutation equivalents `gatekeeper_mutation_request_count` and duration.
- Audit: `gatekeeper_violations` (by enforcement action), `gatekeeper_audit_duration_seconds`, `gatekeeper_audit_last_run_time` and `gatekeeper_audit_last_run_end_time`.
- Mutation: `gatekeeper_mutators`, ingestion count and duration, and `gatekeeper_mutator_conflicting_count`.
- Sync: `gatekeeper_sync` by kind, `gatekeeper_sync_duration_seconds`, `gatekeeper_sync_last_run_time`.
- Watch: `gatekeeper_watch_manager_watched_gvk` and `..._intended_watch_gvk`.
- External data: `gatekeeper_providers` and `gatekeeper_provider_error_count`.
- VAP: `gatekeeper_validating_admission_policies`, `..._for_constraints` and `..._bindings`, by generation status.
- Expansion: `gatekeeper_expansion_templates`.

Aggregation types matter when querying: constraint, template, sync and watch gauges are `LastValue`; request and ingestion counters are `Count`; durations are `Distribution`. Export-related webhook counters are `gatekeeper_admission_export_queued_count`, `..._queue_full_count`, `..._published_count`, `..._publish_error_count`, `..._dropped_count` (tagged by reason) and the gauges `..._queue_depth` and `..._queue_bytes`. The `gatekeeper_validating_admission_policies_for_constraints` metric reports policies generated in `constraint` mode, while `gatekeeper_validating_admission_policies` reports the shared policies generated in `template` mode.

## Checked

Method: docs-checked 2026-11-09 against the Gatekeeper website docs metrics.md (raw markdown, read in full).
