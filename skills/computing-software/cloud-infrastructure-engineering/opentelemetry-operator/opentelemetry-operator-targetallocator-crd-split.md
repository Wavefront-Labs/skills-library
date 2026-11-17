---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-targetallocator-crd-split
name: opentelemetry-operator-targetallocator-crd-split
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, targetallocator-crd, opentelemetry-io-target-allocator, embedded-target-allocator, scrape-configs, crd-changelog]
level: advanced
status: docs-checked
description: "Move from the embedded spec.targetAllocator to a separate TargetAllocator resource linked by the opentelemetry.io/target-allocator label on the collector."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/reference/crd-changelog.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/target-allocator/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Standalone TargetAllocator CRD

The `TargetAllocator` CRD (`opentelemetry.io/v1alpha1`) exists because embedding every possible Target Allocator attribute in the `OpenTelemetryCollector` would make that resource unnecessarily large. The embedded `spec.targetAllocator` still works and is fine for simple cases; the standalone CRD is for users who need to customise the allocator further.

The two forms are equivalent. This embedded form:

```yaml
spec:
  targetAllocator:
    enabled: true
    prometheusCR:
      enabled: true
```

becomes a pair: the Collector gets the label `opentelemetry.io/target-allocator: simplest-ta`, and a separate resource exists:

```yaml
apiVersion: opentelemetry.io/v1alpha1
kind: TargetAllocator
metadata:
  name: simplest-ta
spec:
  prometheusCR:
    enabled: true
```

The Collector is connected to the TargetAllocator solely through that label, whose value is the TargetAllocator name.

Scrape configs may be given either in the Collector's prometheus receiver or directly in the TargetAllocator spec; the resulting allocator uses both. The README example keeps the Collector in `statefulset` mode.

## Checked

Method: docs-checked 2026-11-09 against the CRD changelog (TargetAllocator section) and the Target Allocator README, TargetAllocator CRD section. Dropped the list of pod-level fields on the TargetAllocator spec, which neither page lists.
