---
id: computing-software.cloud-infrastructure-engineering.kyverno.metrics-reference
name: metrics-reference
category: computing-software
field: cloud-infrastructure-engineering
product: kyverno
tags: [metrics-reference, prometheus-metrics, policy-results, admission-review, controller-reconcile, ttl-controller]
level: practitioner
status: docs-checked
description: "Look up Kyverno Prometheus metrics by family: policy and rule, per-CEL-policy-type, admission, HTTP, controller, cleanup and TTL, with their key labels."
sources:
  - https://kyverno.io/docs/reference/metrics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Legacy rules:
- `kyverno_policy_rule_info_total` (gauge; `policy_name`, `policy_type`, `policy_namespace`, `rule_name`, `rule_type`, `policy_validation_mode`, `policy_background_mode`, `status_ready`).
- `kyverno_policy_results` (counter; `rule_result`, `rule_type`, `rule_execution_cause`, `resource_kind`, `resource_namespace`, `resource_request_operation`...).
- `kyverno_policy_execution_duration_seconds` (histogram).

CEL types, each with an `_execution_duration_seconds` histogram and a `_results_total` counter, labelled by `policy_name`, `policy_namespace`, `result`, `execution_cause`, `resource_kind`:
- `kyverno_validating_policy_*` (also `policy_validation_mode`)
- `kyverno_mutating_policy_*`
- `kyverno_generating_policy_*`
- `kyverno_image_validating_policy_*`

Other:
- `kyverno_policy_changes_total` with `policy_change_type` create, update or delete.
- Admission: `kyverno_admission_requests_total` and `kyverno_admission_review_duration_seconds` (`request_allowed`, `request_webhook`, `resource_kind`, `resource_namespace`, `resource_request_operation`); `kyverno_deprecated_api_requests_total` (`group`, `version`, `kind`, `field`).
- HTTP: `kyverno_http_requests_total` and `kyverno_http_requests_duration_seconds` (`http_method`, `http_url`).
- Controllers: `kyverno_controller_reconcile_total`, `kyverno_controller_requeue_total` (plus `num_requeues`), `kyverno_controller_drop_total`, each by `controller_name`.
- Cleanup: `kyverno_cleanup_controller_deletedobjects_total` and `_errors_total`; `kyverno_ttl_controller_deletedobjects` and `_errors`; `kyverno_deleting_controller_deletedobjects_total` and `_errors_total`.
- `kyverno_client_queries_total` (`client_type`, `operation`); `kyverno_info` (version gauge, constant 1).

Metric names above follow the Kyverno metrics reference page; confirm against `/metrics` of your version.

## Checked

2026-11-08. Read the Kyverno Metrics reference page (kyverno.io/docs/reference/metrics) for metric names, types and labels; the sections after the cleanup controller metrics were checked by search for names, types and labels rather than read line by line. Removed the claim about the monitoring guide omitting `_total`, which comes from a page not cited here.

Method: documentation only; no commands were run.
