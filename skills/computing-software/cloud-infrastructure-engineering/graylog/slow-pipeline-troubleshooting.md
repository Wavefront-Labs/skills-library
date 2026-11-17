---
id: computing-software.cloud-infrastructure-engineering.graylog.slow-pipeline-troubleshooting
name: slow-pipeline-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [slow-pipeline, high-cpu, pipeline-performance, grok-regex, processing-time]
level: advanced
status: docs-checked
description: "Find the pipeline rule behind high CPU: causes, the stream Performance view and fixes such as scoping pipelines and caching lookups."
sources:
  - https://go2docs.graylog.org/current/making_sense_of_your_log_data/slow_pipeline_processing_and_high_cpu_usage.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# slow pipeline troubleshooting

One inefficient rule on a busy stream can raise CPU for the whole cluster. Common causes:
- A rule uses a costly function, such as a complex regular expression or Grok pattern, in its condition, running against every message.
- A pipeline is connected to a high-volume stream like the Default Stream although its rules match few messages.
- A rule calls a lookup table whose data adapter is slow or has no cache.
- Several pipelines on the same stream repeat the same expensive work.

Locate it: on **Streams > Performance**, sort by Avg or Max Processing Time (Last 15min); note the top streams and their pipelines. Then find the rule: on **System > Pipelines** click Enable debug metrics, wait a few minutes (values are smoothed over 15 minutes and sampled from one in 100 messages, so they are approximate), sort by Pipeline Load, open the top pipeline and compare rule loads. The Manage rules tab shows a shared rule's combined load. Debug metrics add overhead and memory use, so disable them afterwards with the banner button.

Fixes from the page:
- Narrow the condition and put a cheap check such as `has_field` or `from_input` first, joined with `&&` to the expensive check.
- Replace complex regular expressions with `contains` or `starts_with` where the result is the same.
- If a pipeline on a high-volume stream handles only a subset, route that subset to a dedicated stream and connect the pipeline there.
- Test changes with rule simulation, then recheck Pipeline Load.
- If still stuck, attach a Cluster Support Bundle (enable debug metrics first so `metrics.json` includes the load data).

## Checked

Method: docs-checked 2026-11-09 against https://go2docs.graylog.org/current/making_sense_of_your_log_data/slow_pipeline_processing_and_high_cpu_usage.htm (read in full, Graylog 7.2 docs). The page lists slow or uncached lookup adapters only as a cause, not as a separate fix, so the earlier "add caches" fix was dropped.
