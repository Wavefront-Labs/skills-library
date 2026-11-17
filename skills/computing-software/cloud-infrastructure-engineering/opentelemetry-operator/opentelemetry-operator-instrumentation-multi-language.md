---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-instrumentation-multi-language
name: opentelemetry-operator-instrumentation-multi-language
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, multi-instrumentation, java-container-names, language-specific-annotations, polyglot-pod]
level: advanced
status: docs-checked
description: "Instrument containers written in different languages in one pod with per-language container-names annotations, available while enable-multi-instrumentation is true."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/auto-instrumentation/multi-instrumentation.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/reference/feature-gates.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Multiple language instrumentations in one pod

Multi-instrumentation works only when the operator flag `enable-multi-instrumentation` is true, which is the default (set it to false to disable).

You still add an `inject-<language>` annotation for each language, and then name the containers per language:

- `instrumentation.opentelemetry.io/java-container-names: "java1,java2"`
- `.../nodejs-container-names`, `.../python-container-names`, `.../dotnet-container-names`
- `.../go-container-names: "go1"`
- `.../apache-httpd-container-names`
- `.../inject-nginx-container-names` (the page spells the Nginx one with the `inject-` prefix, unlike the other languages; check your operator version)
- `.../sdk-container-names`

Example: a pod with `myapp`, `myapp2`, `myapp3` and annotations `inject-java: "true"`, `java-container-names: "myapp,myapp2"`, `inject-python: "true"`, `python-container-names: "myapp3"` instruments the first two with Java and the third with Python. The container names may also be init containers for Java, Python, Node.js, .NET and SDK.

Rules and limits:
- If a language-specific list is not given, injection falls back to the first regular container, but only if single instrumentation injection is configured.
- A container cannot receive several language instrumentations.
- The plain `instrumentation.opentelemetry.io/container-names` annotation is not used by this feature.
- Go does not support multi-container pods, so name exactly one Go container.

## Checked

2026-11-04. Confirmed against docs/auto-instrumentation/multi-instrumentation.md: the flag default, the per-language container-names annotations (including the `inject-nginx-container-names` spelling), the Java and Python example, init container support for Java, Python, Node.js, .NET and SDK, the first-container fallback, one language per container, and the plain `container-names` annotation not being used. Confirmed against docs/reference/feature-gates.md: `enable-multi-instrumentation` default true. Confirmed against multi-container.md for the Go single-container note. Nothing removed.

Method: documentation only; no commands were run.
