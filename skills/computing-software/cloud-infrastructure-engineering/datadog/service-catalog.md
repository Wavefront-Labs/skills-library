---
id: computing-software.cloud-infrastructure-engineering.datadog.service-catalog
name: service-catalog
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, service-catalog, service-definition, ownership, dependencies]
level: practitioner
status: docs-checked
description: "Register services with a service definition (schema v2) for ownership, runbooks and dependencies."
sources: ["https://docs.datadoghq.com/internal_developer_portal/catalog/set_up/create_entities/", "https://docs.datadoghq.com/internal_developer_portal/catalog/troubleshooting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service Catalog and definitions
Goal: know who owns each service.

```yaml
# service.datadog.yaml (schema v2.2, adapted from the docs example)
schema-version: v2.2
dd-service: my-unmonitored-cron-job
team: e-commerce
lifecycle: production
application: shopping-app
description: important cron job for shopist backend
tier: "2"
type: web
contacts:
  - type: slack
    contact: https://example.slack.com/archives/XXXXX
links:
  - name: Common Operations
    type: runbook
    url: https://wiki.example.net/runbooks/cron
tags: []
```

- Name the file `service.datadog.yaml` or `entity.datadog.yaml` (both accepted). The name field is `dd-service` for schema v2.2 or earlier and `name` for schema v3.0 and later. Several definitions can share one file separated by `---`.
- Import with Terraform (`datadog_service_definition_yaml`, provider v3.16.0 or later), the Service Definition API (schema v2.x) or Catalog API (v3+), or the GitHub or GitLab integration, which scans repositories for those file names.
- Do not update the same service through both a source code integration and the API, which can overwrite changes.
- With the GitHub integration an Edit in GitHub button appears on the service's Definition tab. Validation errors show in Event Management, filtered by `source:software_catalog` and `status:error`.
- Catalog relies on the `DD_SERVICE` tag across telemetry types (infrastructure metrics, logs, Cloud Network Monitoring) to gather information about a service; configure it per Unified Service Tagging.

Gotcha: a service whose telemetry lacks the expected `DD_SERVICE` tag will not show that data in the Catalog; also check the current schema version, since v3.0 changes the name field.

## Verify
- The service page shows its Definition tab with team and links.

## Checked
2026-11-09. Confirmed against the Create entities and Catalog troubleshooting pages (file names, name field per schema version, multi-document files, import routes, provider version, overwrite warning, GitHub button, validation event filter, `DD_SERVICE` reliance). Removed: the claim that a name mismatch attaches metadata to a different entry, `team` handles for monitor routing, the "telemetry auto-discovers services" claim as worded, the `tags: [tier:1]` example, and the CI-automation, unowned-services review and on-call surfacing advice.
Method: documentation only; no commands were run.
