---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.config-sources-and-providers
name: config-sources-and-providers
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, configuration, config-provider, file, env, http]
level: practitioner
status: docs-checked
description: "Load Collector configuration from files, environment variables, YAML strings and HTTP(S) URLs using --config schemes."
sources:
  - https://opentelemetry.io/docs/collector/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `--config` flag accepts either a file path or a config URI of the form `<scheme>:<opaque_data>`. The page lists these providers:

- `file`: reads a file, for example `file:path/to/config.yaml`.
- `env`: reads configuration from an environment variable, for example `env:MY_CONFIG_IN_AN_ENVVAR`.
- `yaml`: reads a YAML string, with `::` delimiting subpaths, for example `yaml:exporters::debug::verbosity: detailed`.
- `http`: for example `http://www.example.com`.
- `https`: for example `https://www.example.com`.

Combine several in one command:

```shell
otelcol --config=env:MY_CONFIG_IN_AN_ENVVAR --config=https://server/config.yaml
otelcol --config="yaml:exporters::debug::verbosity: normal"
```

Further points from the page:

- By default the configuration lives at `/etc/<otel-directory>/config.yaml`, where the directory is `otelcol`, `otelcol-contrib` or another value, depending on the distribution.
- Nested YAML paths use double colons so they are not confused with dotted names.
- A configuration may also include another file inline with `${file:exporters.yaml}`, which the Collector merges into one in-memory YAML.
- `otelcol validate --config=...` checks a configuration, and `otelcol components` lists what a build contains.

## Checked

2026-11-03. Claims were read against these official pages:

- https://opentelemetry.io/docs/collector/configuration/

Removed or reworded where the pages did not confirm them.

Method: documentation only; no commands were run.
