---
id: computing-software.cloud-infrastructure-engineering.aws.adot-collector-on-eks-and-ecs
name: adot-collector-on-eks-and-ecs
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, x-ray, adot-collector, opentelemetry, aws-distro-for-opentelemetry, eks-add-on, ecs-sidecar, otlp]
level: practitioner
status: docs-checked
description: "Deploy the AWS Distro for OpenTelemetry collector on EKS (add-on or operator) and ECS (sidecar) to send traces to X-Ray and metrics to CloudWatch or Prometheus."
sources: ["https://aws-otel.github.io/docs/getting-started/adot-eks-add-on", "https://aws-otel.github.io/docs/getting-started/adot-eks-add-on/requirements", "https://aws-otel.github.io/docs/setup/ecs/config-through-ssm", "https://aws-otel.github.io/docs/setup/ecs/task-definition-for-ecs-fargate", "https://github.com/aws-observability/aws-otel-collector/tree/main/config/ecs", "https://docs.aws.amazon.com/eks/latest/userguide/opentelemetry.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ADOT collector on EKS and ECS

**Goal:** applications emit OTLP; a collector you control batches, samples and exports traces to
X-Ray and metrics to CloudWatch (EMF) or Amazon Managed Service for Prometheus.

## Collector config (core)
```yaml
receivers:
  otlp:
    protocols: {grpc: {endpoint: 0.0.0.0:4317}, http: {endpoint: 0.0.0.0:4318}}
processors:
  batch: {}
  resourcedetection: {detectors: [env, system, ecs, ec2]}
exporters:
  awsxray: {region: eu-west-1}
  awsemf: {region: eu-west-1, namespace: Orders, log_group_name: /otel/metrics}
service:
  pipelines:
    traces:  {receivers: [otlp], processors: [resourcedetection, batch], exporters: [awsxray]}
    metrics: {receivers: [otlp], processors: [resourcedetection, batch], exporters: [awsemf]}
```
Prometheus remote write: `prometheusremotewrite` exporter with the `sigv4auth` extension to AMP.

## EKS
- Install the `adot` EKS add-on (`aws eks create-addon --addon-name adot --cluster-name <cluster>`), which installs the ADOT Operator; then create `OpenTelemetryCollector` custom resources. Prerequisites: Kubernetes 1.21 or later, no Windows nodes, and a TLS certificate for the operator's admission webhooks (the guide's default is to install cert-manager first).
- Give the collector's service account the AWS permissions it needs for its exporters (X-Ray, CloudWatch EMF, Amazon Managed Service for Prometheus remote write); the ADOT EKS pages do not prescribe specific policy names.
- Apps send to `http://<collector-svc>.<ns>:4318` (OTLP over HTTP; gRPC is 4317); set `OTEL_EXPORTER_OTLP_ENDPOINT`.
- Alternative: the CloudWatch Observability add-on (CloudWatch agent with Container Insights and Application Signals) if you want AWS-managed defaults.

## ECS (sidecar)
```json
{"name":"aws-otel-collector","image":"public.ecr.aws/aws-observability/aws-otel-collector:<TAG>",
 "command":["--config=/etc/ecs/ecs-default-config.yaml"],"essential":true,
 "logConfiguration":{"logDriver":"awslogs","options":{"awslogs-group":"/ecs/otel","awslogs-region":"eu-west-1","awslogs-stream-prefix":"otel"}}}
```
- Bundled configs in the image: `/etc/ecs/ecs-default-config.yaml` (OTLP, StatsD and X-Ray SDK traces to X-Ray, metrics to CloudWatch EMF), `ecs-xray.yaml`, `ecs-amp.yaml`, and `/etc/ecs/container-insights/otel-task-metrics-config.yaml` (adds container resource metrics). To use your own config, set the environment variable `AOT_CONFIG_CONTENT` with `ValueFrom` pointing at an SSM parameter holding a full collector configuration; it overrides the config file in the entrypoint command. Do not store credentials in the config; use `${env:NAME}` placeholders.
- App containers send to `localhost:4317` (OTLP gRPC) or `localhost:4318` (HTTP) in awsvpc mode. The task role needs permissions for the exporters you use.
- Pin the image tag in production (replace `<TAG>` with a release from the aws-otel-collector GitHub releases).

## Sampling and propagation
- X-Ray remote sampling is configured in the SDK (for example the Java `AwsXrayRemoteSampler` pointed at the collector's port 2000, or `OTEL_TRACES_SAMPLER=xray` with ADOT auto-instrumentation) so X-Ray sampling rules apply.
- Include `xray` last in `OTEL_PROPAGATORS` (for example `tracecontext,baggage,xray`) so traces continue across services that use X-Ray trace headers; a later propagator overrides earlier ones.

## Verify
- [ ] Collector logs show successful exports; X-Ray trace map includes OTel-instrumented services.
- [ ] Collector health endpoint (`health_check` extension, as in the bundled configs) monitored.

## Checked
Checked 2026-10-24 against the ADOT documentation (aws-otel.github.io EKS add-on and ECS pages), the aws-observability/aws-otel-collector repository config files (release v0.50.0 current at this date) and the EKS User Guide.
Confirmed: add-on name adot and creation command, ADOT Operator and OpenTelemetryCollector CR, Kubernetes 1.21+ and no Windows nodes, cert-manager as the default TLS method, OTLP ports 4317 and 4318, bundled ECS config names and the entrypoint --config path, AOT_CONFIG_CONTENT via SSM ValueFrom, awsxray and awsemf exporter options, prometheusremotewrite with sigv4auth, health_check extension, OTEL_PROPAGATORS with xray last, SDK-side X-Ray remote sampling.
Removed as unconfirmed: managed policy names for the collector role, Instrumentation auto-instrumentation claim, deployment/daemonset/sidecar mode list, tail sampling advice, memory_limiter recommendation, the eks resource detector.

Method: documentation only; no commands were run.
