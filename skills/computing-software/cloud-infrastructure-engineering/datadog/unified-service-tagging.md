---
id: computing-software.cloud-infrastructure-engineering.datadog.unified-service-tagging
name: unified-service-tagging
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, tagging, unified-service-tagging, env-service-version, dd-tags]
level: practitioner
status: docs-checked
description: "Apply env, service and version reserved tags across metrics, traces and logs with DD_ variables or pod labels, and follow tag format rules."
sources: ["https://docs.datadoghq.com/getting_started/tagging/unified_service_tagging/", "https://docs.datadoghq.com/getting_started/tagging/", "https://docs.datadoghq.com/getting_started/tagging/assigning_tags/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unified service tagging and tags
Goal: make every signal for a service filterable together with three reserved tags: `env`, `service`, `version`.

```
# Environment variables on the application container
DD_ENV=<ENV>
DD_SERVICE=<SERVICE>
DD_VERSION=<VERSION>
```

```yaml
# Kubernetes: labels on the pod spec (and optionally the Deployment)
labels:
  tags.datadoghq.com/env: "<ENV>"
  tags.datadoghq.com/service: "<SERVICE>"
  tags.datadoghq.com/version: "<VERSION>"
```

On Kubernetes the docs also pass the labels into `DD_ENV`, `DD_SERVICE` and `DD_VERSION` through `valueFrom.fieldRef` on `metadata.labels['tags.datadoghq.com/env']` (and `.../service`, `.../version`). The `DD_*` variables are only required for APM-enabled applications. For multi-container pods use `tags.datadoghq.com/<CONTAINER_NAME>.env` (also `.service`, `.version`). For Docker, set the `DD_*` variables plus the matching Docker labels, for example `docker run -e DD_ENV=<ENV> -l com.datadoghq.tags.env=<ENV> ...`.

- Requirements: Agent 6.19.x/7.19.x or higher, and a tracer version that supports the reserved tags (minimum SDKs: .NET 1.17.0, C++ 0.1.0, Go 1.24.0, Java 0.50.0, Node 0.20.3, PHP 0.47.0, Python 0.38.0, Ruby 0.34.0).
- `version` should change with each deployment so versions can be compared.
- Host tags: set `tags:` in `datadog.yaml` (a list of `<KEY>:<VALUE>`), or the `DD_TAGS` variable. In `DD_TAGS` tags are separated by spaces, not commas, and whitespace inside a value is not converted: `DD_TAGS="key1:value1 key2:value2"`.
- Container and pod labels become tags with `DD_CONTAINER_LABELS_AS_TAGS` and `DD_KUBERNETES_POD_LABELS_AS_TAGS`, which take a JSON map of label name to tag name.
- Tag limits: up to 200 characters including key, colon and value; span and metric tags are normalised to lowercase, so avoid camel case in keys.

Gotcha: cardinality. Each distinct tag value on a metric creates another custom metric time series, so keep unbounded values (user IDs, request IDs) out of metric tags.

## Verify
- In the Metrics Explorer, group by `service` and `env`; the APM service page and logs show the same `env` and `version` values.

## Checked
2026-11-03. Confirmed against the Unified Service Tagging, Getting Started with Tagging and Assigning Tags pages. Fixed: the draft's `DD_TAGS="team:payments,tier:1"` used commas, but `DD_TAGS` is space-separated. Removed the "(confirm names)" marker (both `*_AS_TAGS` names are on the Assigning Tags page), quarterly audit and CI advice, and Tag Policies claims.
Method: documentation only; no commands were run.
