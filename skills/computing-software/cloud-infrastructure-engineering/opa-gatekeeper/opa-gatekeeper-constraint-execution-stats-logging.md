---
id: computing-software.cloud-infrastructure-engineering.opa-gatekeeper.opa-gatekeeper-constraint-execution-stats-logging
name: opa-gatekeeper-constraint-execution-stats-logging
category: computing-software
field: cloud-infrastructure-engineering
product: opa-gatekeeper
tags: [opa-gatekeeper, log-stats, observability, templateruntimens, constraintcount, performance]
level: advanced
status: docs-checked
description: "Find slow ConstraintTemplates by enabling --log-stats-admission and --log-stats-audit and reading templateRunTimeNS and constraintCount in the logs."
sources: ["https://github.com/open-policy-agent/gatekeeper/blob/master/website/docs/metrics.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Opa gatekeeper constraint execution stats logging

To identify a template with a long execution time, enable stats logging on the controller:
- `--log-stats-admission` for admission review.
- `--log-stats-audit` for audit.

Each admission review then logs an entry with `msg: admission review request stats`, `event_type: review_response_stats`, the resource kind and request username, and an `execution_stats` list. For a template scope, `statsFor` names the constraint kind (for example `K8sRequiredLabels`) and the stats include:
- `templateRunTimeNS`: nanoseconds spent evaluating all constraints for the template (the example shows 762561).
- `constraintCount`: how many constraints of that kind were evaluated.

Each stat also carries its source engine (`Rego`) and a description. Labels show the environment, such as `TracingEnabled`, `PrintEnabled` and the `target` (`admission.k8s.gatekeeper.sh`).

Caveat: the log volume can be quite high, so enable it temporarily while investigating.

`--log-stats-audit` enables the same stats for the audit process. Statistics are written to Gatekeeper's stdout logs.

## Checked

2026-11-04. Confirmed against metrics.md (Logging Constraint Execution Stats, example log line, caveats). Removed or corrected: unsourced comparison and filtering advice about audit stats.

Method: documentation only; no commands were run.
