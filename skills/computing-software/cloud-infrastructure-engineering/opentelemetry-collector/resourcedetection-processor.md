---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.resourcedetection-processor
name: resourcedetection-processor
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, processors, resourcedetection, cloud, host, detectors]
level: practitioner
status: docs-checked
description: "Detect host, cloud and container attributes automatically with the resourcedetection processor and ordered detectors."
sources:
  - https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/resourcedetectionprocessor/README.md
  - https://opentelemetry.io/docs/collector/transforming-telemetry/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The resource detection processor detects resource information from the host, in the format of the resource semantic conventions, and appends or overrides it on telemetry. The page example:

```yaml
processors:
  resourcedetection/system:
    detectors: [env, system, gcp, ec2, azure]
    timeout: 2s
    override: false
```

Details from the README:

- If a configured detector fails, the error propagates and stops the Collector from starting, so list only detectors for your platform.
- Each detector retries failed detection with exponential backoff by default: `retry.initial_interval` 1s, `multiplier` 2, `max_interval` 30s, `randomization_factor` 0.5. `retry.max_elapsed_time` 0 means the whole session is bounded by `timeout`. The processor rejects retry enabled with both `timeout` and `max_elapsed_time` at 0.
- The `env` detector reads `OTEL_RESOURCE_ATTRIBUTES` as `key1=value1,key2=value2`.
- The `system` detector sets `host.name` to the FQDN if possible, else the OS hostname; `hostname_sources` defaults to `["dns", "os"]`. When running in a container, use the `docker` detector instead.
- GCE labels need the `roles/compute.viewer` role on the instance's service account.
- The `k8snode` name is deprecated; use `k8s_api`.
- As a sidecar, set `override: false` so values like `service.name` are not overwritten.

## Checked

2026-11-03. Claims were read against these official pages:

- https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/resourcedetectionprocessor/README.md
- https://opentelemetry.io/docs/collector/transforming-telemetry/

Removed or reworded where the pages did not confirm them.

Method: documentation only; no commands were run.
