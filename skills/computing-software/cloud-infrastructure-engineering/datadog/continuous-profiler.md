---
id: computing-software.cloud-infrastructure-engineering.datadog.continuous-profiler
name: continuous-profiler
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, profiler, continuous-profiling, flame-graph, code-hotspots]
level: practitioner
status: draft
description: "Enable the Datadog Continuous Profiler to find CPU and memory hot spots and link profiles to traces."
sources: ["https://docs.datadoghq.com/", "https://docs.datadoghq.com/agent/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Continuous Profiler
Goal: reduce CPU and memory waste.

```
DD_PROFILING_ENABLED=true DD_SERVICE=checkout DD_ENV=prod DD_VERSION=1.4.2 ddtrace-run python app.py
```

```
# Java example
java -javaagent:dd-java-agent.jar -Ddd.profiling.enabled=true -jar app.jar
```

- Flame graphs show CPU time, allocations, wall time and lock contention by language.
- Compare profiles between versions with the comparison view.
- Code Hotspots links a slow trace span to the profile.
- Overhead is generally low (confirm for your language in the docs).

Gotcha: profiles upload via the Agent; if the Agent cannot receive them (blocked port 8126) nothing shows. Version tags are essential for before/after comparisons.

Use the Profile comparison view after each release and pair it with a performance budget; share flame graphs in pull requests when a change affects hot paths. Sample production only, and compare with a staging profile to separate real hotspots from test artefacts.

## Verify
- The service page's Profiles tab shows recent profiles; a flame graph loads.
