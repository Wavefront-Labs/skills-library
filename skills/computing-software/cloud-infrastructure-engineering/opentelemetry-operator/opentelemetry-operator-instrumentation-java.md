---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-instrumentation-java
name: opentelemetry-operator-instrumentation-java
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, java, javaagent, java-extensions, java-tool-options, inject-java]
level: practitioner
status: docs-checked
description: "Inject the Java agent with the inject-java annotation and add extension JARs through spec.java.extensions, which copies them into a shared directory via init containers."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/auto-instrumentation/languages/java.md", "https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/api/instrumentations.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Java auto-instrumentation and agent extensions

Enable with the pod annotation:

```
instrumentation.opentelemetry.io/inject-java: "true"
```

Agent extensions. Use `spec.java.extensions` in the `Instrumentation` resource to add extension JARs to the Java agent. Each entry has an `image` containing the JARs and a `dir` pointing to the directory inside that image (it is not a path in the application container).

```yaml
apiVersion: opentelemetry.io/v1alpha1
kind: Instrumentation
metadata:
  name: java-instrumentation
spec:
  java:
    extensions:
      - image: registry.example.com/java-agent-extensions:1.0
        dir: /extensions
```

How it works: the operator creates an init container for each extension image and runs `cp -r` to copy the contents of `dir` into the shared Java instrumentation volume. Therefore the extension image must provide the `cp` command. The operator adds `-Dotel.javaagent.extensions=<instrumentation-directory>/extensions` to the application container's `JAVA_TOOL_OPTIONS` so the agent loads the JARs.

All extension images copy into the same directory, and the API reference notes that a JAR with the same name is overwritten. Use distinct JAR filenames across images.

Other `spec.java` fields: `image` (the javaagent image), `env`, `resources`, `volumeClaimTemplate` (ephemeral volume; an emptyDir is used if omitted) and the deprecated `volumeLimitSize` (default 200Mi) which is being replaced by `spec.<lang>.volume.size`.

## Checked

2026-11-04. Confirmed against docs/auto-instrumentation/languages/java.md: `inject-java`, `spec.java.extensions` with `image` and `dir` (not an application container path), the init container per extension image with `cp -r` and the `cp` requirement, the `-Dotel.javaagent.extensions=` entry in `JAVA_TOOL_OPTIONS`, and the shared directory with distinct JAR names. Confirmed in the Instrumentation API reference (docs/api/instrumentations.md, read as raw Markdown because the GitHub page view is a stub): the overwrite note for same-named JARs, `volumeClaimTemplate` with the emptyDir fallback, and `volumeLimitSize` (default 200Mi, deprecated in favour of `spec.<lang>.volume.size`). Nothing removed.

Method: documentation only; no commands were run.
