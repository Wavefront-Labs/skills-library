---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-target-allocator-collector-cr-usage
name: opentelemetry-operator-target-allocator-collector-cr-usage
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, targetallocator-enabled, dollar-escaping, config-rewrite, prometheus-scrape-config, relabel-config]
level: practitioner
status: docs-checked
description: "Enable the Target Allocator in a statefulset Collector, understand how the operator rewrites the Prometheus receiver, and escape dollar signs with double dollars."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/target-allocator/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Enable the Target Allocator from the Collector CR

Minimal usage:

```yaml
apiVersion: opentelemetry.io/v1beta1
kind: OpenTelemetryCollector
metadata:
  name: collector-with-ta
spec:
  mode: statefulset
  targetAllocator:
    enabled: true
  config:
    receivers:
      prometheus:
        config:
          scrape_configs:
          - job_name: 'otel-collector'
            scrape_interval: 10s
            static_configs:
            - targets: [ '0.0.0.0:8888' ]
```

What the operator does: it creates a TA Deployment and Service serving a specific `http_sd_config` for each Collector pod, then rewrites the Collector's Prometheus receiver so it only contains a `target_allocator` section (endpoint `http://collector-with-ta-targetallocator.<namespace>.svc:80`, interval 30s, `collector_id: $POD_NAME`). The receiver's original scrape configs move to the TA's own Prometheus configuration, where they are discovered and sharded across Collectors with the same job names.

Dollar signs: the Collector config supports environment variable substitution, so a literal `$` in Prometheus config (for example a relabel `replacement: $1`) must be written `$$1` in the Collector CR. The operator converts `$$` to `$` when generating the TA configuration, because the TA does not do env substitution. Writing a single `$` in the CR would be read as an environment variable.

Scrape configs may also be put straight in the standalone TargetAllocator spec, and the TA uses both sources.

## Checked

Method: docs-checked 2026-11-09 against the Target Allocator README (docs/target-allocator, read in full).
