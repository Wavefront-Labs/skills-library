---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.loki-ingestion-from-cloud-fluent-otel-and-docker
name: loki-ingestion-from-cloud-fluent-otel-and-docker
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [loki-ingest, cloudwatch-to-loki, gcp-logs-loki, lambda-promtail, fluent-bit-loki-output, fluentd-loki, otlphttp-to-loki, otel-collector-loki-exporter, docker-loki-driver, docker-logging-driver]
level: practitioner
status: docs-checked
description: "Get logs into Loki from AWS (lambda-promtail, Firehose), GCP Pub/Sub, Fluent Bit and Fluentd, the OTel Collector via OTLP, and the Docker Loki logging driver."
sources: ["https://grafana.com/docs/loki/latest/send-data/", "https://grafana.com/docs/loki/latest/send-data/lambda-promtail/", "https://docs.fluentbit.io/manual/data-pipeline/outputs/loki", "https://grafana.com/docs/loki/latest/send-data/docker-driver/", "https://grafana.com/docs/loki/latest/send-data/docker-driver/configuration/", "https://grafana.com/docs/loki/latest/send-data/fluentd/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loki ingestion from cloud, Fluent, OTel and Docker

## AWS
- **lambda-promtail**: Lambda subscribed to CloudWatch Logs groups (subscription filter) or S3 (ALB/CloudFront
  access logs) pushing to Loki or any Loki push API compatible endpoint (including Alloy). The lambda-promtail docs page covers the Terraform and CloudFormation deployment and the environment variables; read it for the exact names. Watch Lambda concurrency and Loki rate limits. It is unrelated to the standalone Promtail agent, which is end-of-life as of 2026-03-02.
- Alternative: Alloy `loki.source.awsfirehose` behind a Firehose HTTP endpoint delivery stream.
## GCP
Log Router sink -> Pub/Sub topic -> Alloy `loki.source.gcplog` (pull subscription, or push to HTTP)
with `use_incoming_timestamp` set as needed.

## Fluent Bit
```ini
[OUTPUT]
    Name        loki
    Match       kube.*
    Host        loki-gateway.monitoring
    Port        80
    Tenant_ID   prod
    Labels      job=fluent-bit, namespace=$kubernetes['namespace_name'], app=$kubernetes['labels']['app']
    Remove_Keys kubernetes,stream
    Line_Format json
    Structured_Metadata trace_id=$trace_id
```
## Fluentd
`fluent-plugin-grafana-loki` (`@type loki`, `url`, `tenant`, `<label>` block with record keys).

## OpenTelemetry Collector
Use the **otlphttp** exporter to Loki's native OTLP endpoint (`<LOKI_URL>/otlp`); see the Loki OTel page for the exact endpoint and for how resource attributes map to labels and structured metadata.

## Docker logging driver
```bash
docker plugin install grafana/loki-docker-driver:<VERSION>-amd64 --alias loki --grant-all-permissions   # add -arm64 for ARM64 hosts; not supported on Windows
```
```json
{"log-driver": "loki", "log-opts": {"loki-url": "http://loki:3100/loki/api/v1/push",
 "loki-batch-size": "400", "loki-retries": "2", "loki-max-backoff": "800ms", "loki-timeout": "1s", "keep-file": "true"}}
```
(set in `daemon.json`, or per container). Caveat: a known issue can deadlock the Docker daemon while Loki is unreachable; lower the wait with `loki-retries=2`, `loki-max-backoff=800ms`, `loki-timeout=1s` and `keep-file=true`, or prefer a host agent (Alloy reading Docker log files). The driver is a third-party client without the support commitment of Alloy.

## Label hygiene everywhere
Keep labels to environment/namespace/app/container/job; send IDs as structured metadata or in the line.

## Verify
- [ ] Each source shows up in Loki with the expected labels and no 4xx in the shipper's logs.
- [ ] Shipper retries/backpressure tested by briefly blocking Loki.

## Checked
- 2026-10-28. Confirmed against the Loki lambda-promtail page (forwards AWS logs to any Loki push API endpoint; Promtail EOL 2026-03-02), the Alloy `loki.source.awsfirehose` and `loki.source.gcplog` references (`use_incoming_timestamp`, push and pull), the Fluent Bit Loki output page (`Tenant_ID`, `Label_Keys`, `Remove_Keys`, `Line_Format`, `Structured_Metadata`), the Fluentd page (`fluent-plugin-grafana-loki`, `@type loki`, `<label>`), the Loki OTel page (`otlphttp`) and the Docker driver pages (`plugin install ... --alias loki`, `loki-retries`, `loki-max-backoff`, `loki-timeout`, `keep-file`, deadlock note).
- Removed: lambda-promtail environment variable names (not on the fetched page), `extract_kubernetes_labels`, the `:latest` plugin tag, and the `mode: non-blocking` instruction.
Method: documentation only; no commands were run.
