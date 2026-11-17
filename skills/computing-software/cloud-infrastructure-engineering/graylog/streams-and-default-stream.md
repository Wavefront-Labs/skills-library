---
id: computing-software.cloud-infrastructure-engineering.graylog.streams-and-default-stream
name: streams-and-default-stream
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [streams, default-stream, stream-rules, stream-performance]
level: practitioner
status: docs-checked
description: "How streams route messages: the Default Stream, stream rules versus pipelines, and the Performance view of processing time."
sources:
  - https://go2docs.graylog.org/current/making_sense_of_your_log_data/streams.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# streams and default stream

- **Default Stream**: built-in catch-all that receives messages matching no other stream's rules. It cannot be deleted or paused. Unless a message matches a custom stream rule it lands here.
- **Stream rules** filter messages from inputs into a stream in real time; a stream can have several rules combined with AND or OR. Stream rules are to become a legacy feature: prefer pipelines for routing, since pipeline rules give finer control.
- **Streams page**: Status (Running or Paused), a Routing view to trace how messages reach a stream and where they go next (it includes Data Lake and Archiving columns, both Enterprise features), and a Performance view.

Performance: sort by Avg Processing Time (Last 15min) or Max Processing Time (Last 15min) to find streams whose pipelines are slow.

Data Routing lets you change a stream's destination, for example to a Data Lake or an output.

## Checked

2026-11-04. Confirmed against the Streams page (default stream, stream rules and the pipelines recommendation, Streams page views and columns, Data Routing). Fixed: default stream cannot be paused; Archiving is a Routing-view column and Enterprise-only. Reworded the Data Routing line.

Method: documentation only; no commands were run.
