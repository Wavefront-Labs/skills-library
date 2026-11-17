---
id: computing-software.cloud-infrastructure-engineering.observability.otel-collector-config-providers-and-merging
name: otel-collector-config-providers-and-merging
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [config-env-provider, confmap-providers, config-merging, collector-config, otel-collector]
level: practitioner
status: docs-checked
description: "Use OTel Collector config providers: env, file, yaml, http(s) URIs, defaults, escaping, merging multiple --config files and --set overrides."
sources: ["https://opentelemetry.io/docs/collector/configuration/", "https://github.com/open-telemetry/opentelemetry-collector/tree/main/confmap", "https://github.com/open-telemetry/opentelemetry-collector-releases/blob/main/distributions/otelcol-contrib/manifest.yaml", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/confmap/provider"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Collector config providers and merging

## URI providers
| Syntax | Meaning |
|---|---|
| `${env:OTLP_TOKEN}` | environment variable |
| `${env:REGION:-eu-west-1}` | with default |
| `${file:/etc/otel/token}` | file contents |
| `--config "yaml:exporters::debug::verbosity: normal"` | inline YAML on the command line, `::` separates sub-paths |
| `${http://config-svc/otel.yaml}` / `https:` | remote file |
The `--config` flag takes a file path or a `<scheme>:<opaque_data>` URI; the documented schemes are `file`, `env`, `yaml`, `http`
and `https`. The otelcol-contrib manifest also includes the `aes`, `s3`, `secretsmanager` and `googlesecretmanager` providers
(alpha): `${secretsmanager:<arn or name>}` (needs `secretsmanager:GetSecretValue`; `#json-key` selects a key of a JSON secret),
`${aes:<encrypted, base64 value>}` (key from `OTEL_AES_CREDENTIAL_PROVIDER`), and `s3://` URIs.
A bare `${VAR}` is only expanded when the distribution sets a default URI scheme (`conf_resolver.default_uri_scheme: env` in the
builder manifest); the otelcol-contrib manifest does not, so write `${env:VAR}`. The resolver limits a configuration to 100 embedded URIs.
Use `$$` for a literal `$` (docs example: `namespace: $$DataVisualization`).

## Multiple config files
```bash
otelcol-contrib --config file:base.yaml --config file:prod-overrides.yaml --set=processors.batch.timeout=2s
```
Each file may be a partial configuration and the files are merged; if the result is incomplete the collector reports an error.
By default a list from a later source replaces the earlier list (so `service.pipelines.traces.processors` in an override replaces
the base list). The experimental feature gate `confmap.enableMergeAppendOption` (`--feature-gates=confmap.enableMergeAppendOption`)
appends lists in source order. `--set` takes `key.path=value` (dots become `::`), has higher precedence than the config files,
overrides arrays and joins maps; the component must already be defined in the config.

## Patterns
- Base config in an image, per-environment overrides via ConfigMap.
- Secrets from env injected by Kubernetes Secrets: `api_key: ${env:DD_API_KEY}`.
- Validate with `otelcol-contrib validate --config=...`.
- Print the effective configuration with `otelcol-contrib print-config --config=...`; `--mode` is `redacted` (default) or `unredacted`, and `--validate` defaults to true.

## Gotchas
- An embedded URI cannot contain a `$` character unless it embeds another URI (confmap limitation).
- Use a default (`${env:NAME:-default}`) deliberately: the docs show `${env:OPERATION:-}` for an empty default.
- `--set` examples use dots for key paths, so component keys that themselves contain dots (such as metric names) need the
  `yaml:` form with `::` instead.

## Checked

2026-10-24. OpenTelemetry docs collector/configuration.md, collector confmap README, otelcol flags.go and command_print.go, confmap expand.go and resolver.go, otelcol-contrib manifest at v0.163.1 and contrib provider READMEs (main branch). Confirmed: config URI schemes, yaml `::` paths, multiple `--config` merging, experimental append gate and default list replacement, `--set` semantics and example, `print-config` and `validate`, `$$` escape, default-scheme rule for bare `${VAR}`, 100 URI limit, and contrib provider list and usage. Removed the claim that the old `$VAR` syntax is removed and the SIGHUP reload claim (not documented in these sources).

Method: documentation only; no commands were run.
