---
id: computing-software.cloud-infrastructure-engineering.fluentd.worker-directive-and-include
name: worker-directive-and-include
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, worker, include, multi-worker, config-reuse]
level: practitioner
status: docs-checked
description: "Restrict plugins to specific workers with the worker directive and reuse configs with @include, including glob, URL and section-level includes."
sources:
  - https://docs.fluentd.org/configuration/config-file
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd worker directive and @include
**worker**: with `<system> workers 4 </system>`, a plugin outside any `<worker>` block runs on all workers. Wrap sources in `<worker 0>` or `<worker 0-1>` (zero-based indexes) to limit them; useful for plugins that do not support multiple workers. `"#{worker_id}"` yields the worker's id in embedded Ruby.

**@include** accepts an absolute path, a path relative to the including file's directory, a glob, or an http URL:
```
@include /path/to/config.conf
@include extra.conf
@include config.d/*.conf
@include http://example.com/fluent.conf
```
Globs expand alphabetically, but do not depend on that order. If `a.conf` and `z.conf` matter, include them explicitly and glob the rest between them.

`@include` also works inside a section to share parameters, such as a common `<buffer>` tail:
```
<buffer>
  @type file
  path /path/to/buffer/forward
  @include /path/to/out_buf_params.conf
</buffer>
```
where the included file holds lines like `flush_interval 5s`.

## Checked

2026-11-04. Confirmed against the Fluentd Config File page (docs.fluentd.org/configuration/config-file), worker directive and @include sections: zero-based worker indexes, N-M form, worker_id in embedded Ruby, include path forms, glob order warning, section-level include. Nothing removed.

Method: documentation only; no commands were run.
