---
id: computing-software.ai-ml-engineering.seldon-core-2.seldonconfig-resource
name: seldonconfig-resource
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, seldonconfig, crd, kafkaconfig, tracingconfig, agentconfig, serviceconfig, components]
level: advanced
status: docs-checked
description: "SeldonConfig fields: component PodSpecs, KafkaConfig, TracingConfig, AgentConfiguration rclone secrets and ServiceConfig, used as the base for every SeldonRuntime."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/kubernetes/resources/seldonconfig.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# SeldonConfig resource

SeldonConfig defines the core components Seldon installs in each namespace. It is advanced usage: core DevOps normally keep the default SeldonConfig or customise it once, and individual namespaces then use a SeldonRuntime with a few overrides.

## Spec
The spec has two parts, `components` and `config`.

- `components`: each entry has `name`, optional `labels`, `annotations`, `replicas`, `podSpec` and `volumeClaimTemplates`. Labels and annotations merge with those on the SeldonConfig and are added to the component Deployment or StatefulSet.
- `config.kafkaConfig`: `bootstrap.servers`, `consumerGroupIdPrefix`, `topicPrefix`, `debug`, plus `consumer`, `producer` and `streams` maps of settings.
- `config.tracingConfig`: `disable`, `otelExporterEndpoint`, `otelExporterProtocol`, `ratio`.
- `config.agentConfig.rclone`: `config_secrets` and `config` lists, which become the Agent ConfigMap holding rclone defaults.
- `config.serviceConfig`: `grpcServicePrefix` and `serviceType`.

The PodSpecs cover each core component, and the general configuration includes the ConfigMaps created for the Agent (rclone defaults), Kafka and Tracing (OpenTelemetry).

## Overrides
Some of these values can be overridden per namespace through the SeldonRuntime resource. The default configuration lives in `operator/config/seldonconfigs/default.yaml` in the repository. Changing a SeldonConfig updates all SeldonRuntimes that reference it, unless they set `disableAutoUpdate`.

## Checked

Confirmed against the Seldon Config page: components fields, the kafkaConfig, tracingConfig, agentConfig.rclone and serviceConfig field names, label and annotation merging, per-namespace overrides via SeldonRuntime, the default.yaml location, and update propagation (taken with the SeldonRuntime page).

Method: docs-checked 2026-11-09 against the Seldon Core v2 docs-gb kubernetes/resources/seldonconfig.md and seldonruntime.md pages (raw markdown).
