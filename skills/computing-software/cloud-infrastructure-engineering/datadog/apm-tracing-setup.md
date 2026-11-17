---
id: computing-software.cloud-infrastructure-engineering.datadog.apm-tracing-setup
name: apm-tracing-setup
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, apm, tracing, ddtrace, dd-trace]
level: practitioner
status: docs-checked
description: "Instrument an app with the Datadog tracer (ddtrace) and send traces through the Agent on port 8126."
sources: ["https://docs.datadoghq.com/tracing/trace_collection/automatic_instrumentation/dd_libraries/python/", "https://docs.datadoghq.com/tracing/trace_collection/automatic_instrumentation/dd_libraries/java/", "https://docs.datadoghq.com/tracing/other_telemetry/connect_logs_and_traces/python/", "https://docs.datadoghq.com/agent/configuration/network/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# APM tracing setup
Goal: get distributed traces for a service.

```
# Python
pip install ddtrace
ddtrace-run python app.py
ddtrace-run --info          # check the configuration took effect
```

```
# Java: download dd-java-agent.jar, then add the JVM argument
java -javaagent:/path/to/dd-java-agent.jar -Ddd.logs.injection=true -Ddd.service=my-app -Ddd.env=staging -Ddd.version=1.0 -jar path/to/your/app.jar
```

- Python: prefix the entry-point command with `ddtrace-run`. `ddtrace-run --info` shows configuration, but not changes made at runtime in code.
- Java: the tracer is `dd-java-agent.jar` (latest from `https://dtdg.co/latest-java-tracer`), loaded with `-javaagent`. Each option has an environment variable and a system property form, for example `DD_SERVICE` / `dd.service` and `DD_LOGS_INJECTION` / `dd.logs.injection`. `DD_SERVICE` is the name of a set of processes that do the same job.
- The Agent's APM receiver listens on TCP 8126 by default (`receiver_port` in `datadog.yaml`, env `DD_APM_RECEIVER_PORT`); setting it to 0 disables the HTTP receiver. This port covers tracing and the profiler.
- Log correlation: logs need `dd.env`, `dd.service`, `dd.version`, `dd.trace_id` and `dd.span_id`. For Python with `ddtrace` older than 3.11 set `DD_LOGS_INJECTION=true`.
- If logs are not parsed by a Datadog log integration, custom parsing must treat `dd.trace_id` and `dd.span_id` as strings and remap them with the Trace Remapper.

Gotcha: a tracer that cannot reach the Agent receiver on port 8126 sends nothing, so check network reachability of that port from the application host or container.

## Verify
- The service appears in APM after traffic, and `ddtrace-run --info` reports the expected configuration.

## Checked
2026-11-09. Confirmed against the Python and Java tracing setup pages, the Python logs and traces correlation page, and the Agent network page (commands, `--info` caveat, JVM argument and options, jar download URL, port 8126 and `receiver_port`, log correlation attributes, `ddtrace<3.11` rule, Trace Remapper note). Removed: the `DD_SERVICE=... DD_ENV=... DD_VERSION=... DD_AGENT_HOST=localhost` command line and the claim that an unset `DD_AGENT_HOST` loses traces (not on the fetched pages), `apm_config.enabled: true`, the Node and Go snippets, the Admission Controller claim, the import-order gotcha, and the one-service-at-a-time, overhead, version currency and health-check filtering advice.
Method: documentation only; no commands were run.
