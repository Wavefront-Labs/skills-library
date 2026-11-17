---
id: computing-software.cloud-infrastructure-engineering.observability.otel-resource-detectors
name: otel-resource-detectors
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [resource-detectors-config, cloud-resource-detection, semantic-conventions, resource-attributes, resourcedetection-processor]
level: practitioner
status: docs-checked
description: "Populate OTel resource attributes automatically: SDK detectors per language, OTEL_RESOURCE_ATTRIBUTES, collector resourcedetection for EC2/EKS/GCP/AKS, precedence."
sources: ["https://opentelemetry.io/docs/concepts/resources/", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/resourcedetectionprocessor", "https://opentelemetry.io/docs/zero-code/java/agent/configuration/", "https://opentelemetry.io/docs/languages/java/configuration/", "https://github.com/open-telemetry/opentelemetry-js/tree/main/experimental/packages/opentelemetry-sdk-node"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resource detectors

A Resource describes the entity producing telemetry (`service.*`, `host.*`, `cloud.*`, `k8s.*`, `container.*`,
`process.*`). Detectors fill it automatically; merge order decides who wins.

## SDK side
- Always: `OTEL_SERVICE_NAME` and `OTEL_RESOURCE_ATTRIBUTES=service.namespace=shop,deployment.environment.name=prod`.
- Java agent: resource providers are enabled by default except the AWS, GCP and Azure ones; enable those with
  `otel.resource.providers.aws.enabled=true` (likewise `gcp`, `azure`). Restrict the list with `otel.java.enabled.resource.providers`
  or `otel.java.disabled.resource.providers`, both comma-separated provider class names, for example
  `-Dotel.java.disabled.resource.providers=io.opentelemetry.instrumentation.resources.OsResourceProvider`. If you set the enabled
  list, include `io.opentelemetry.sdk.autoconfigure.EnvironmentResourceProvider` so `OTEL_RESOURCE_ATTRIBUTES` still applies.
- Node (`@opentelemetry/sdk-node`): default detectors are env, process and host. `OTEL_NODE_RESOURCE_DETECTORS` accepts `env`,
  `host`, `os`, `process`, `serviceinstance` (experimental), `all` or `none`, run in the listed order, and is used only when
  `resourceDetectors` is not set in code. Cloud and container detectors are separate packages (for example
  `@opentelemetry/resource-detector-container`) passed in code.
- Python: `OTEL_EXPERIMENTAL_RESOURCE_DETECTORS` takes entry point names (`otel`, `process`, `os`, `host`, `service_instance` in the SDK,
  plus packages such as `opentelemetry-resource-detector-containerid`, `opentelemetry-resource-detector-azure`,
  `opentelemetry-resourcedetector-gcp` and `opentelemetry-sdk-extension-aws`). Detectors run in order and later ones win on
  conflicts; `otel` (env variables) is appended last unless placed explicitly. The variable is experimental and may change.
- Go: `resource.New(ctx, resource.WithFromEnv(), resource.WithProcess(), resource.WithOS(), resource.WithContainer(), resource.WithHost())`;
  add third-party detectors (for example the AWS detectors in opentelemetry-go-contrib) with `resource.WithDetectors(...)`.
- .NET: `ResourceBuilder.CreateDefault().AddDetector(...)`; contrib packages `OpenTelemetry.Resources.Container`, `.Host`, `.AWS`, `.Azure`, `.Gcp`.

## Collector side (often simpler, one place)
```yaml
processors:
  resource_detection:                # type name; resourcedetection is a deprecated alias
    detectors: [env, eks, ec2, gcp, aks, azure, system]
    timeout: 2s                        # default 5s
    override: false                    # default true; false keeps attributes already on the telemetry
    system: {hostname_sources: [os]}   # default [dns, os]
    ec2: {tags: ["^team$"]}            # regexes of EC2 tag keys to copy
```
EC2 tags are read with the `DescribeTags` API, which needs the `ec2:DescribeTags` IAM permission, unless `tags_from_imds: true`
(needs instance metadata tags enabled, no IAM permission). Detector order matters: if several detectors set the same attribute the
first one wins; the README recommends for AWS the order lambda, elastic_beanstalk, eks, ecs, ec2. On Kubernetes use the `k8s_api`
detector for node and cluster attributes (`k8snode` is deprecated); it needs `node_from_env_var` set and RBAC `get`, `list` on
`nodes`. Pod, namespace and workload attributes come from the separate `k8sattributes` processor. Run detection where the
collector runs on the host or node you want described (an agent), since detectors describe the machine the collector runs on.

## Precedence
SDK: the spec's Resource `Merge` gives precedence to the updating resource, and language SDKs differ in detector order (Node and
Python run detectors in the listed order; Python appends the env detector last). Collector: `override: false` keeps incoming values;
with the default `override: true` detected values replace them.

## Gotchas
- Cloud detectors query metadata services: failed detections are retried with backoff (`retry`, bounded by `timeout`) and a failing
  detector can stop the collector from starting, so list only detectors that apply to the host. `fail_on_missing_metadata`
  (default false) controls whether an unreachable metadata service is a hard failure.
- `refresh_interval` re-runs detection periodically; unset means detection runs once at startup.

## Verify
Collector `debug` exporter shows `Resource attributes:` with cloud.region, k8s.pod.name etc.

## Checked

2026-10-24. OpenTelemetry docs and READMEs (main branch): resourcedetection processor README and metadata.yaml, Java agent and Java SDK configuration pages, opentelemetry-js sdk-node README, opentelemetry-python SDK environment variables and pyproject entry points, Go resources page, opentelemetry-python-contrib, opentelemetry-go-contrib and opentelemetry-dotnet-contrib repository listings, and the Resource SDK specification. Confirmed: processor type `resource_detection` (alias `resourcedetection`), detector names, `timeout` default 5s, `override` default true, `hostname_sources` default, EC2 tags and `ec2:DescribeTags`, detector ordering rule, `k8s_api` replacing `k8snode`, retry and `fail_on_missing_metadata`, Java provider properties, Node and Python variable values, and package names. Corrected: Java AWS/GCP providers are disabled by default, Node `OTEL_NODE_RESOURCE_DETECTORS` has no cloud or container values, and the Python container package is `-containerid`. Removed unconfirmed claims about `host.name` in containers and Prometheus `target_info`.

Method: documentation only; no commands were run.
