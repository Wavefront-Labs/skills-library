---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-instrumentation-inject-annotations
name: opentelemetry-operator-instrumentation-inject-annotations
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, inject-annotation, instrumentation-opentelemetry-io, namespace-injection, pod-template-annotation, inject-java]
level: intro
status: docs-checked
description: "Turn on auto-instrumentation by annotating a namespace or pod template with instrumentation.opentelemetry.io/inject-<language>, using true, a name, namespace/name or false."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/auto-instrumentation/README.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/auto-instrumentation/languages/nodejs.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/auto-instrumentation/languages/sdk-only.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Enable injection with annotations

After creating an `Instrumentation` resource, injection is switched on with an annotation of the form `instrumentation.opentelemetry.io/inject-<language>`, for example `inject-java`, `inject-python`, `inject-nodejs`, `inject-dotnet`, `inject-go`, `inject-php`, `inject-ruby`, `inject-nginx`, `inject-apache-httpd` or `inject-sdk`.

Where to put it:
- On a namespace, so every pod in the namespace gets instrumentation.
- On individual PodSpec templates of a Deployment, StatefulSet and similar resources (the pod template metadata, not the controller's own metadata).

Possible values:
- `"true"`: use the `Instrumentation` resource found in the namespace.
- `"my-instrumentation"`: an Instrumentation named so in the current namespace.
- `"my-other-namespace/my-instrumentation"`: name and namespace of an Instrumentation in another namespace.
- `"false"`: do not inject.

ClusterObservability uses the cross-namespace form, with all apps referencing one shared Instrumentation, for example `opentelemetry-operator-system/default-instrumentation`.

Troubleshooting checklist from the docs set:
1. The language must be enabled in the operator (Go, Nginx, Ruby and PHP are off by default).
2. By default only the first container of the pod is instrumented; use the container-names annotations for others.
3. Go needs the target executable annotation, otherwise injection aborts and leaves the pod unchanged.

The SDK-only variant `inject-sdk` injects environment variables without an agent.

## Checked

2026-11-04. Confirmed against docs/auto-instrumentation/README.md: the supported languages (Apache HTTPD, DotNet, Go, Java, Nginx, NodeJS, PHP, Python, Ruby), the namespace and PodSpec placement, and the four annotation values. Confirmed against languages/nodejs.md and languages/sdk-only.md (read as raw Markdown): `inject-nodejs` and `inject-sdk`, the latter injecting environment variables without providing the SDK. Confirmed against feature-gates.md, configuration.md, multi-container.md and go.md for the troubleshooting list (Go, Nginx and Ruby off by default, PHP off by default in the configuration reference, first container only, Go target executable) and against cluster-observability.md for the cross-namespace form. Nothing removed.

Method: documentation only; no commands were run.
