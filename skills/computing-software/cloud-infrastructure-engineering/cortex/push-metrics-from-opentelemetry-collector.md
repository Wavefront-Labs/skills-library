---
id: computing-software.cloud-infrastructure-engineering.cortex.push-metrics-from-opentelemetry-collector
name: push-metrics-from-opentelemetry-collector
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [opentelemetry, otlp, remote-write, tenant-header, distributor]
level: practitioner
status: docs-checked
description: "Send OpenTelemetry Collector metrics to Cortex via the prometheusremotewrite or OTLP HTTP exporter with the tenant header."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/guides/open-telemetry-collector.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two ways to push metrics from an OpenTelemetry Collector.

Prometheus format, using the `prometheusremotewrite` exporter:

```yaml
exporters:
  prometheusremotewrite:
    endpoint: http://<cortex-endpoint>/api/v1/push
    headers:
      X-Scope-OrgId: <orgId>
service:
  pipelines:
    metrics:
      exporters: [prometheusremotewrite]
```

OTLP format, using the `otlphttp` exporter pointed at the OTLP path:

```yaml
exporters:
  otlphttp:
    endpoint: http://<cortex-endpoint>/api/v1/otlp
    headers:
      X-Scope-OrgId: <orgId>
```

Add the exporter to the metrics pipeline under `service.pipelines`. In both cases the `X-Scope-OrgId` header carries the tenant ID that Cortex requires; see the authentication and authorisation page.

OTLP over gRPC is also possible but experimental and disabled by default. Enable it with `-distributor.otlp.grpc-enabled=true`, then use the `otlp` exporter against the distributor gRPC port (9095 in the example) with `compression: gzip` and the `X-Scope-OrgId` header. The exporter uses TLS by default, so set `tls` to match the Cortex gRPC server. The maximum request size is `-server.grpc-max-recv-msg-size-bytes` (default 4 MiB) and applies to all distributor gRPC traffic; raise it or shrink the Collector batch size if batches are larger. The gRPC port is often reachable only inside the cluster with no authenticating gateway, and the distributor trusts `X-Scope-OrgId` as sent, so do not expose it to untrusted clients.

OTLP ingestion options sit under `limits.promote_resource_attributes` and `distributor.otlp` (`convert_all_attributes`, `disable_target_info`, `allow_delta_temporality`, `enable_type_and_unit_labels`, `add_metric_suffixes`).

## Checked

2026-11-04. Claims were read against the Cortex docs page: Use OpenTelemetry Collector to send metrics to Cortex (see sources). Removed filler and unconfirmed wording.

Method: documentation only; no commands were run.
