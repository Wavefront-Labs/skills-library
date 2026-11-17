---
id: computing-software.cloud-infrastructure-engineering.fluentd.multi-process-workers
name: multi-process-workers
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, workers, multi-process, worker-id, in-tail, server-helper]
level: practitioner
status: docs-checked
description: "Scale Fluentd across CPUs with the workers setting: which inputs share ports, which need a worker directive (in_tail), and worker_id in output paths."
sources:
  - https://docs.fluentd.org/deployment/multi-process-workers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd multi-process workers
`<system> workers 4 </system>` launches four worker processes under one supervisor; each runs the full plugin set. Each worker uses memory and disk separately, so size buffers accordingly.

Plugins fall in three groups:
- **Server-helper based inputs** (e.g. `forward`) share one port across workers.
- **Plain plugins** that open their own socket (e.g. `monitor_agent`) get sequential ports: port 25000 gives worker0 25000, worker1 25001.
- **Unsupported** (e.g. `tail`): start fails with `Plugin 'tail' does not support multi workers configuration`. Pin them with `<worker N>`, or `<worker N-M>` (since v1.4.0), where N is a zero-based index.

```
<system>
  workers 4
</system>
<worker 0>
  <source>
    @type tail
  </source>
</worker>
```
Every configured plugin must support multiple workers or be inside a `<worker>` block.

Outputs that write to a path (`file`, `S3`) can collide when workers flush at once; add the id:
```
path "logs/#{worker_id}/${tag}/%Y/%m/%d/"
```
## Checked

2026-11-04. Confirmed against the Fluentd Multi Process Workers page (docs.fluentd.org/deployment/multi-process-workers): workers parameter, worker directive and N-M since v1.4.0, three input plugin types, sequential monitor_agent ports, worker_id in output paths, the tail start error. Removed: the automatic worker subdirectory for file buffer paths (not on this page).

Method: documentation only; no commands were run.
