---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.scaling-prometheus-target-allocator
name: scaling-prometheus-target-allocator
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, scaling, prometheus, target-allocator, operator, statefulset]
level: sme
status: docs-checked
description: "Scale Prometheus scraping across Collector replicas with the OpenTelemetry Operator Target Allocator."
sources:
  - https://opentelemetry.io/docs/collector/scaling/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Scrapers such as the Prometheus receiver actively obtain telemetry. You cannot simply add replicas with the same configuration, because each Collector would scrape the same endpoints as every other, causing problems such as out-of-order samples. The solution is to shard endpoints across Collector instances.

One way is a configuration file per Collector, each discovering only its relevant endpoints, for example one Kubernetes namespace or label set per Collector. The other is the Target Allocator, an extra binary deployed as part of the OpenTelemetry Operator that distributes Prometheus scrape targets for a configuration across the cluster of Collectors.

```yaml
apiVersion: opentelemetry.io/v1alpha1
kind: OpenTelemetryCollector
metadata:
  name: collector-with-ta
spec:
  mode: statefulset
  targetAllocator:
    enabled: true
  config: |
    receivers:
      prometheus:
        config:
          scrape_configs:
          - job_name: 'otel-collector'
            scrape_interval: 10s
            static_configs:
            - targets: [ '0.0.0.0:8888' ]
```

After reconciliation, the Operator adds a `global` section and an `http_sd_configs` entry to the scrape config, pointing at a Target Allocator instance such as `http://collector-with-ta-targetallocator:80/jobs/otel-collector/targets?collector_id=$POD_NAME`. To scale, change `replicas` on the custom resource, and the allocator hands each pod its own `http_sd_config` targets.

The page says to shard once scraping all targets takes a time close to the scrape interval.

## Checked

Method: docs-checked 2026-11-09 against the opentelemetry.io collector/scaling page (docs repo raw markdown).
