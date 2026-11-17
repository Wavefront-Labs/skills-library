---
id: computing-software.cloud-infrastructure-engineering.observability.ottl-contexts-paths-and-error-mode
name: ottl-contexts-paths-and-error-mode
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [ottl-contexts, ottl-error-mode, ottl, transform-processor, filter-processor]
level: advanced
status: docs-checked
description: "Write OTTL statements in the transform processor: path prefixes per signal, context inference, advanced statement groups with conditions, and error_mode."
sources: ["https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/transformprocessor", "https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/pkg/ottl/contexts/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OTTL contexts, paths and error_mode

## Contexts
A context bridges an OTTL path and the underlying data model. The OTTL module provides contexts for resource,
instrumentation scope, span, span event, span link, metric, datapoint, exemplar, log, profile, profile sample and
OTelCol (the last needs the `ottl.contexts.enableOTelColContext` feature gate). Use these provided contexts unless
you have a specific need.

## Path prefixes per signal (transform processor)
| Section | Allowed path prefixes |
|---|---|
| trace_statements | `resource`, `scope`, `span`, `spanevent` |
| metric_statements | `resource`, `scope`, `metric`, `datapoint`, `exemplar` |
| log_statements | `resource`, `scope`, `log` |
| profile_statements (experimental) | `resource`, `scope`, `profile` |
For example, `span.attributes` cannot be used in `log_statements`. Statements run in configured order.

## Basic config
A plain list of statements; the processor infers the context from the path prefixes.
```yaml
processors:
  transform:
    error_mode: ignore
    trace_statements:
      - keep_keys(span.attributes, ["service.name", "cloud.region"])
      - truncate_all(span.attributes, 4096)
    log_statements:
      - set(log.severity_text, "FAIL") where log.body == "request failed"
```

## Context inference
Because paths carry the context name, the processor picks the context able to parse every path, function and enum
in the statement. In `set(metric.description, "test passed") where datapoint.attributes["test"] == "pass"` the
inferred context is `datapoint`, the only one that parses both `datapoint` and `metric` paths; with `metric` and
`resource` paths it is `metric`. If a combination of paths, functions or enums is not allowed, split it into
several advanced-config groups.

## Advanced config
Each group can set `context`, `error_mode`, `shared_cache`, `conditions` and `statements`. Conditions are ORed
global where clauses: if one is true, the group's statements (with their own where clauses) run. `shared_cache`
shares per-context caches among groups that enable it.
```yaml
processors:
  transform:
    error_mode: ignore
    metric_statements:
      - error_mode: propagate
        conditions:
          - metric.type == METRIC_DATA_TYPE_SUM
        statements:
          - set(metric.description, "Sum")
```

## error_mode
The top-level default is `ignore` and a group-level value overrides it.
| Value | Behaviour |
|---|---|
| ignore | log the error, continue with the next statement (recommended) |
| silent | ignore the error without logging, continue |
| propagate | return the error up the pipeline; the payload is dropped from the collector |

## Verify
- [ ] Statements only use path prefixes valid for their signal section.
- [ ] The collector starts (the processor checks that paths, functions and enums are parsable).

## Checked
2026-11-09. Confirmed against the transform processor README (general, basic and advanced config and context
inference sections read) and the OTTL contexts README (read in full). Removed unconfirmed claims: the per-context
path catalogues, the claim that propagate is the default (the README says ignore), the claim that inner contexts
read outer ones, the resource-attribute and nil gotchas, and the transform example using merge_maps, ParseJSON and
replace_pattern, plus the OTTL README source (not read).
Method: docs-checked 2026-11-09 against the transformprocessor README and the OTTL contexts README; documentation only, no commands run.
