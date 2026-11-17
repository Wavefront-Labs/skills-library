---
id: computing-software.cloud-infrastructure-engineering.aws.container-insights-enhanced-observability
name: container-insights-enhanced-observability
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudwatch, container-insights, container-insights-enhanced, container-metrics, eks, ecs, amazon-cloudwatch-observability, cloudwatch-agent, fluent-bit, performance-logs, kubernetes-monitoring]
level: practitioner
status: docs-checked
description: "Turn on CloudWatch Container Insights with enhanced observability for EKS (add-on) and ECS (account setting), read the metrics and performance logs, and control the cost."
sources: ["https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ContainerInsights.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/install-CloudWatch-Observability-EKS-addon.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/deploy-container-insights-ECS-cluster.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Container-Insights-metrics-enhanced-EKS.html", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Container-Insights-metrics-ECS.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container Insights with enhanced observability

**Goal:** every EKS and ECS cluster reports CPU, memory, network, restarts and throttling
down to pod/task and container level into CloudWatch, with curated dashboards and alarms,
without running a Prometheus stack — and the bill is understood before enabling it.

## 1. EKS
```bash
# the agent's role needs the CloudWatchAgentServerPolicy managed policy (EKS Pod Identity, node role or IAM role for service accounts)
aws eks create-addon --cluster-name prod --addon-name amazon-cloudwatch-observability \
  --pod-identity-associations serviceAccount=cloudwatch-agent,roleArn=arn:aws:iam::<ACCOUNT_ID>:role/cw-agent
kubectl -n amazon-cloudwatch get pods      # CloudWatch agent and Fluent Bit pods
```
- The add-on (or the Helm chart) enables Container Insights and Application Signals by default; Container Insights with enhanced observability collects pod and container-level metrics and, by default, accelerated compute metrics (NVIDIA GPU from add-on v1.3.0, AWS Neuron from v1.5.0, EFA). From add-on `v6.2.0-eksbuild.1` Container Insights with OpenTelemetry metrics (OTLP, PromQL) can also be enabled. The add-on supports Kubernetes 1.23 or later.
- Configure via add-on configuration values (`--configuration-values file://cfg.json`),
  e.g. disable container logs (`containerLogs.enabled: false`) if you ship logs elsewhere.
- Windows nodes need add-on 1.5.0 or later, Application Signals is not supported on Windows, and some metrics are not collected there; check the metrics table.

## 2. ECS
```bash
aws ecs put-account-setting --name containerInsights --value enhanced   # current principal; add --principal-arn arn:aws:iam::<ACCOUNT_ID>:root for all users
aws ecs update-cluster-settings --cluster prod --settings name=containerInsights,value=enhanced
```
`enabled` collects cluster, service and task level metrics; `enhanced` (recommended by the guide) adds dimensions and metrics down to container level. EC2 instances need ECS agent 1.29 or later; EC2 instance-level metrics need a separately deployed CloudWatch agent. New clusters pick up the account setting; existing clusters need `update-cluster-settings`.

## 3. Where the data lands
- Metrics: EKS in namespace `ContainerInsights` (dimensions such as `ClusterName`, `Namespace`,
  `PodName`, `NodeName`); ECS in namespace `ECS/ContainerInsights` (dimensions such as `ClusterName`, `ServiceName`, `TaskDefinitionFamily`).
- ECS performance log events: `/aws/ecs/containerinsights/<cluster>/performance` — query them with Logs Insights for
  dimensions that are not published as metrics; a customer managed KMS key must be associated with that group.
- Container stdout/stderr (EKS add-on Fluent Bit): `/aws/containerinsights/<cluster>/application`,
  plus `host` and `dataplane` groups.
- Console: CloudWatch → Container Insights → cluster/namespace/workload views with top-N.

Useful alarms: `pod_number_of_container_restarts` > 0 sustained,
`node_cpu_utilization` > 80%, `pod_memory_utilization_over_pod_limit` > 90% (absent for pods whose containers have no memory limit),
`cluster_failed_node_count` > 0, ECS `RunningTaskCount` below `DesiredTaskCount`.

## 4. Cost control
- Enhanced observability for EKS is charged per observation (the earlier version is charged as custom metrics); with OpenTelemetry metrics it is charged per GB ingested. Estimate with the CloudWatch pricing page before enabling everywhere.
- Log ingestion and storage are billed separately: set retention on the `/aws/containerinsights/*` groups and filter noisy namespaces in Fluent Bit, or turn off container logs with `containerLogs.enabled: false`.

## Gotchas
- Missing metrics after install usually means the agent lacks IAM permissions (the add-on needs credentials through Pod Identity, the node role or a service account role); check the agent pod logs.
- Existing resources that conflict with the add-on make creation fail unless the conflict resolution method is set to override; remove or migrate self-managed CloudWatch agent manifests first.
- ECS `enhanced` must be set per existing cluster; the account default only affects new ones.

## Verify
- [ ] `aws cloudwatch list-metrics --namespace ContainerInsights --dimensions Name=ClusterName,Value=prod` returns pod/container-level metrics.
- [ ] Killing a pod in a test deployment increments the restart metric and the alarm fires.
- [ ] Log groups under `/aws/containerinsights/prod/` have retention set.

## Checked
Checked 2026-10-24 against the Amazon CloudWatch User Guide (EKS add-on installation, ECS Container Insights setup, EKS enhanced metrics, ECS metrics).
Confirmed: add-on name and Pod Identity association form (serviceAccount=cloudwatch-agent), CloudWatchAgentServerPolicy, default enabling of Container Insights and Application Signals, accelerated compute defaults and versions, OpenTelemetry metrics from v6.2.0, Windows requirements, containerLogs.enabled option, ECS commands (put-account-setting, update-cluster-settings), namespaces ContainerInsights and ECS/ContainerInsights, EKS log groups (application, dataplane, host), ECS performance log group, alarm metric names, pricing basis for EKS.
Corrected: the ECS namespace is ECS/ContainerInsights; the account setting command is put-account-setting. Removed as unconfirmed: AWSXrayWriteOnlyAccess, control-plane metric claim, EKS performance log group name, retention examples.

Method: documentation only; no commands were run.
