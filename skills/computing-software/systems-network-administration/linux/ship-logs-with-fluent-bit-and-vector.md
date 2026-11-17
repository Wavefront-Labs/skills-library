---
id: computing-software.systems-network-administration.linux.ship-logs-with-fluent-bit-and-vector
name: ship-logs-with-fluent-bit-and-vector
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, fluent-bit, vector-agent, log-shipping, vrl, loki, elasticsearch]
level: practitioner
status: docs-checked
description: "Ship Linux host logs with Fluent Bit or Vector agents: journald and file inputs, parsing, buffering to disk, outputs to Loki, Elasticsearch or S3, and checking delivery."
sources:
  - https://docs.fluentbit.io/manual/
  - https://vector.dev/docs/
  - https://docs.fluentbit.io/manual/administration/buffering-and-storage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Ship logs with Fluent Bit or Vector

Both are single-binary agents with small footprints. Vector has a transform language (VRL).

## Fluent Bit
```ini
# /etc/fluent-bit/fluent-bit.conf (classic format; YAML also supported)
[SERVICE]
    flush           5
    storage.path    /var/lib/fluent-bit/
    storage.sync    normal
    http_server     on
    http_port       2020
[INPUT]
    name            systemd
    tag             host.journal
    db              /var/lib/fluent-bit/journal.db     # cursor so restarts don't resend
    storage.type    filesystem
[INPUT]
    name            tail
    path            /var/log/nginx/access.log
    # parser <name>   (selects a parser defined in your parsers file)
    db              /var/lib/fluent-bit/tail.db
    storage.type    filesystem
[OUTPUT]
    name            loki
    match           host.*
    host            loki.example.com
    port            3100
    labels          job=host, hostname=${HOSTNAME}
    retry_limit     no_limits
```
- `storage.type filesystem` buffers chunks on disk while the output is down; cap with `storage.total_limit_size` on the output.
- `db` files keep track of monitored files and offsets (tail) or the journald cursor (systemd) across restarts.
- Health/metrics: `curl -s localhost:2020/api/v1/metrics/prometheus | grep -E 'output_(retries|errors|proc_records|dropped)'` (the built-in HTTP server must be on).

## Vector
```yaml
# /etc/vector/vector.yaml
data_dir: /var/lib/vector
sources:
  journal: { type: journald }
  nginx: { type: file, include: [/var/log/nginx/access.log] }
transforms:
  parsed:
    type: remap
    inputs: [nginx]
    source: |
      # VRL goes here: parse .message and reshape the event (see the VRL function reference)
      .source_file = "nginx"
sinks:
  es:
    type: elasticsearch
    inputs: [journal, parsed]
    endpoints: [https://es.example.com:9200]
    # authentication and buffer settings: see the sink's reference page (buffer type disk keeps events across restarts)
```
```bash
vector validate /etc/vector/vector.yaml
vector tap parsed            # watch events flowing through a component
vector top                   # throughput per component
```

## Choosing
- Heavy reshaping, routing to several sinks, or metrics-from-logs: Vector's VRL can be tried in the `vector vrl` REPL.
- Both read the journal directly; you don't need rsyslog in the middle.

## Pitfalls
- File permissions: the agent user needs read access to the log files and the journal.
- Log rotation with `copytruncate` can lose lines; prefer rename rotation.
- Keep Loki labels low-cardinality (host, job, level); put request or user IDs in the log line.

## Verify
- [ ] Stop the destination for 10 minutes, restart: no gap in timestamps at the destination.
- [ ] Agent metrics show zero dropped records.

## Checked

Checked 2026-10-27 against Fluent Bit documentation sources (fluent/fluent-bit-docs: systemd and tail inputs, Loki output, buffering, backpressure, monitoring, scheduling and retries) and Vector reference sources (vectordotdev/vector cli.cue, journald, file and Elasticsearch components), current main, 2026-10-27. Confirmed: Fluent Bit service keys flush, http_server, http_port, storage.path/type/sync, per-output storage.total_limit_size, systemd input db and tag, tail input path/parser/db, Loki output host, port and labels, retry_limit no_limits, Prometheus metrics endpoint and output metric names, Vector journald and file sources, elasticsearch sink endpoints key, and the vector validate, tap, top and vrl commands. Removed or softened: nginx parser name, VRL parse_nginx_log example, Vector auth and disk-buffer option values, adoption claims for Kubernetes charts and AWS, group names, Loki cardinality figures.

Method: documentation only; no commands were run.
