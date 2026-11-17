---
id: computing-software.cloud-infrastructure-engineering.kubernetes.log-pipelines-vector-otel-to-cloud-and-opensearch
name: log-pipelines-vector-otel-to-cloud-and-opensearch
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, logging, vector, otel-logs, cloud-log-shipping, cloudwatch-logs, fluent-bit-cloudwatch, efk, opensearch, elasticsearch-logging]
level: practitioner
status: docs-checked
description: "Build node-level log pipelines with Vector or the OTel Collector filelog receiver, add Kubernetes metadata, and ship to CloudWatch/Cloud Logging or OpenSearch/Elasticsearch."
sources: ["https://vector.dev/docs/reference/configuration/sources/kubernetes_logs/", "https://opentelemetry.io/docs/platforms/kubernetes/collector/components/#filelog-receiver", "https://opentelemetry.io/docs/platforms/kubernetes/helm/collector/", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter/awscloudwatchlogsexporter", "https://docs.fluentbit.io/manual/data-pipeline/outputs/cloudwatch", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Log pipelines: Vector / OTel Collector to cloud and OpenSearch

All read container logs from `/var/log/pods/*/*/*.log` (CRI format) via a DaemonSet with a
read-only hostPath, add pod metadata from the API, buffer, and ship.

## Vector (DaemonSet "agent" role)
```yaml
sources:
  k8s: {type: kubernetes_logs}              # reads /var/log/pods and enriches with pod/namespace metadata
transforms:
  parse:
    type: remap
    inputs: [k8s]
    source: |
      parsed, err = parse_json(.message)
      if err == null { . = merge!(., parsed) }
      del(.kubernetes.pod_labels."pod-template-hash")
sinks:
  opensearch:
    type: elasticsearch
    inputs: [parse]
    endpoints: [https://opensearch.logging:9200]
    mode: bulk
    bulk: {index: "k8s-%Y.%m.%d"}
    auth: {strategy: basic, user: vector, password: "${OS_PASSWORD}"}
    buffer: {type: disk, max_size: 1073741824, when_full: block}
  cloudwatch:
    type: aws_cloudwatch_logs
    inputs: [parse]
    region: eu-west-1
    group_name: "/k8s/prod/{{ kubernetes.pod_namespace }}"
    stream_name: "{{ kubernetes.pod_name }}"
    encoding: {codec: json}
```
Helm: `helm install vector vector/vector --set role=Agent -f values.yaml` (`Agent` runs a
DaemonSet; the chart's default role is `Aggregator`). Disk buffers survive restarts; memory
buffers lose data on OOM. CloudWatch allows one writer per log stream, so stream names must be
unique per writer.

## OTel Collector (logs alongside traces/metrics)
```yaml
receivers:
  file_log:                                 # formerly filelog
    include: [/var/log/pods/*/*/*.log]
    exclude: [/var/log/pods/*/otel-collector/*.log]   # don't ingest yourself
    include_file_path: true
    start_at: end
    operators: [{type: container, id: container-parser}]
processors:
  k8s_attributes: {}                        # formerly k8sattributes
  batch: {}
exporters:
  awscloudwatchlogs: {log_group_name: /k8s/prod, log_stream_name: otel, region: eu-west-1}
service: {pipelines: {logs: {receivers: [file_log], processors: [k8s_attributes, batch], exporters: [awscloudwatchlogs]}}}
```
Recent Collector releases renamed several components (`file_log`, `k8s_attributes`, `otlp_http`)
and keep the old names as deprecated aliases; match the names to your Collector version. With
the Helm chart, `presets.logsCollection.enabled: true` adds the receiver and host mounts and
`presets.kubernetesAttributes.enabled: true` adds the processor and RBAC.

## Cloud destinations
- **CloudWatch**: Fluent Bit `cloudwatch_logs` output, the Vector sink or the Collector
  exporter; IAM via Pod Identity/IRSA (Fluent Bit documents `logs:CreateLogStream`,
  `logs:CreateLogGroup`, `logs:PutLogEvents` and `logs:PutRetentionPolicy`). Set retention on
  log groups: by default CloudWatch keeps log data indefinitely.
- **Other managed clouds**: check whether the platform already ships container logs, and
  filter to control cost.

## OpenSearch/Elasticsearch (the "EFK" back end)
Run via the OpenSearch operator/Helm or ECK; index templates with explicit mappings (arbitrary
JSON keys cause field explosions), lifecycle policies for hot, warm and delete phases, and a
quorum-safe set of cluster-manager nodes. Elasticsearch/OpenSearch on Kubernetes is a stateful
service you now operate; managed offerings often win.

## Verify
- [ ] Logs from a test pod appear within 30s with namespace/pod/container fields.
- [ ] Agent buffer/backpressure metrics flat; no `429`/bulk rejections from OpenSearch.

## Checked
2026-10-27 against Vector docs and source (vectordotdev/vector master: kubernetes_logs reference,
elasticsearch and aws_cloudwatch_logs sink references and config source; helm-charts values),
opentelemetry.io (main: Kubernetes components, Helm collector chart), the
opentelemetry-collector(-contrib) component metadata and READMEs, Fluent Bit's CloudWatch output
page and the AWS CloudWatch Logs guide. Confirmed: Vector `mode: bulk` default, `bulk.index`,
`auth.strategy: basic` with `user`/`password`, `group_name`/`stream_name`/`region`/`encoding`,
`role: Agent`; the filelog example, Helm presets, exporter settings, Fluent Bit plugin name and
IAM actions, and CloudWatch's indefinite default retention. Fixed: the component renames
(`file_log`, `k8s_attributes`, `otlp_http`), a Loki exporter path that was not checked, and
unchecked GKE/Azure and OpenSearch setting claims.
Method: documentation only; no commands were run.
