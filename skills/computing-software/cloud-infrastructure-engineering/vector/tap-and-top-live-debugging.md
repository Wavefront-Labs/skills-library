---
id: computing-software.cloud-infrastructure-engineering.vector.tap-and-top-live-debugging
name: tap-and-top-live-debugging
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [tap, top, graph, debugging, observability-api, vector-top, vector]
level: advanced
status: docs-checked
description: "Inspect live events and component throughput with vector tap, vector top and vector graph."
sources:
  - https://vector.dev/docs/reference/cli/
  - https://vector.dev/docs/setup/going-to-prod/rollout/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Three CLI subcommands help while a pipeline runs. `tap` and `top` talk to the observability API of a running instance, a gRPC endpoint that is disabled by default (`api.enabled` defaults to false; `api.address` defaults to `127.0.0.1:8686`).

```yaml
api:
  enabled: true
```

**vector top** displays topology and metrics in the console for a local or remote instance. `-H` (`--human-metrics`) humanises numbers; `--url` selects the endpoint.

**vector tap** samples events flowing through components:

```bash
vector tap --outputs-of my_source --limit 20
vector tap --inputs-of my_sink --format yaml
```

- `components` argument or `--outputs-of`: sources and transforms whose output you want; default `*` when no other pattern is given. Glob patterns work.
- `--inputs-of`: transforms and sinks whose input you want.
- `--interval` (default 500 ms) and `--limit` (default 100 events per interval).
- `--duration_ms` (`-d`) stops after a period; `--meta` adds `component_id`; `--format` is json (default), yaml or logfmt.
- `--url` selects a remote API endpoint.

**vector graph** prints the topology in DOT format: `vector graph --config /etc/vector/vector.yaml | dot -Tsvg > graph.svg`.

Security: the API currently does not support authentication, so enable it only in isolated environments or for debugging, and never expose it to untrusted clients.

Verify that events seen with `tap` and in `top` match what you expect at each hop, as the rollout guide suggests when streaming a copy of data to Vector.

## Checked

2026-11-03. Read reference/cli, reference/configuration/api and setup/going-to-prod/rollout. Confirmed: `vector tap` flags and defaults (`--outputs-of`, `--inputs-of`, `--interval` 500, `--limit` 100, `--duration_ms`, `--meta`, `--format` json/yaml/logfmt, `--url`, default `*` components), `vector top` and `-H`, `vector graph` DOT piping, the API default, bind address and no-authentication warning, and the rollout page's use of top and tap. Fixed: the API is a gRPC endpoint, and the previous `api.enabled: false` config-example attribution and YAML block were removed.

Method: documentation only; no commands were run.
