---
id: computing-software.software-engineering.ktor.ktor-micrometer-metrics
name: ktor-micrometer-metrics
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, micrometer, metrics, prometheus, monitoring, jvm]
level: practitioner
status: docs-checked
description: "Expose Ktor server metrics with MicrometerMetrics: registry setup, default HTTP and JVM metrics, timers tags, distribution statistics, meterBinders, Prometheus endpoint."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-metrics-micrometer.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ktor Micrometer metrics

The `MicrometerMetrics` plugin (package `io.ktor.server.metrics.micrometer`) enables Micrometer metrics and lets you pick a monitoring system (Prometheus, JMX, Elastic, ...). By default it exposes HTTP request metrics plus low-level JVM metrics. Native server targets are not supported.

## Dependencies

- `io.ktor:ktor-server-metrics-micrometer`
- A registry artifact for your system, e.g. `io.micrometer:micrometer-registry-prometheus`.

## Install with a registry

After installing, create a registry for your monitoring system and assign it to the `registry` property. Create the `PrometheusMeterRegistry` outside the `install` block so route handlers can reuse it.

## Default HTTP metrics

- `ktor.http.server.requests.active`: gauge of concurrent requests, no tags.
- `ktor.http.server.requests`: timer per request, with tags such as `address`, `method`, `route`.

Change the `ktor.http.server.requests` prefix with the `metricName` property. Names may differ depending on the monitoring system.

## Configure

```kotlin
install(MicrometerMetrics) {
    timers { call, exception ->
        tag("region", call.request.headers["regionId"])
    }
}
```

- `timers`: called per request to add custom tags.
- `distributionStatisticConfig`: configure distribution statistics.
- `meterBinders`: set the list of JVM/system metrics; assign an empty list to disable them entirely.

## Prometheus scrape endpoint

Add a dedicated GET route (the example uses `/metrics`) and `call.respond` the registry's scrape output to Prometheus.

Full example: `micrometer-metrics` in the ktor-documentation code snippets.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-metrics-micrometer.md.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.
