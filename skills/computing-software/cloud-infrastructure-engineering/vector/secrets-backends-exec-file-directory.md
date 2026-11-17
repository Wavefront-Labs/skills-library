---
id: computing-software.cloud-infrastructure-engineering.vector.secrets-backends-exec-file-directory
name: secrets-backends-exec-file-directory
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [secrets, secret-backends, exec, file, directory, aws-secrets-manager, vector]
level: sme
status: docs-checked
description: "Keep credentials out of config files with SECRET[backend.name] placeholders and the exec, file and directory backends."
sources:
  - https://vector.dev/docs/reference/configuration/secrets/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Secrets management is the recommended way to supply secrets, preferred over environment interpolation: values never enter the process environment. Define backends under the top-level `secret` key and reference them as `SECRET[<backend>.<name>]`:

```yaml
secret:
  external:
    type: exec
    command: ["/usr/local/bin/read-secrets", "--environment", "production"]
    timeout: 5
sinks:
  datadog:
    type: datadog_logs
    inputs: [logs]
    default_api_key: "SECRET[external.datadog_api_key]"
```

Backends:

- **exec:** Vector writes JSON such as `{"version": "1.0", "secrets": ["datadog_api_key"]}` to stdin; the command must print one JSON object on stdout with `{"value": ..., "error": null}` per secret. Diagnostics go to stderr. Protocol `v1_1` adds `backend_type` and `backend_config`.
- **file:** a UTF-8 JSON object mapping names directly to string values.
- **directory:** one file per secret under a path; nested names such as `database/username` are allowed; `remove_trailing_whitespace: true` strips a final newline.
- **aws_secrets_manager:** has its own guide and auth options.

Rules: backend names allow letters, digits, `_` and `-`; secret names also allow `.` and `/`. A missing backend or secret, an error, or an empty value fails config loading entirely. Secrets are queried when the configuration loads, including on configuration reloads, and substituted before parsing, so a secret containing YAML or TOML syntax can alter the parsed configuration.

Verify with `vector validate`, then reload with SIGHUP after rotating a value.

## Checked

2026-11-03. Read reference/configuration/secrets. Confirmed: recommended over environment interpolation, the `secret` key and `SECRET[<backend>.<name>]` syntax, exec protocol v1 request and response JSON, v1_1 `backend_type` and `backend_config`, stderr as warnings, file and directory backends, `remove_trailing_whitespace`, naming rules, failure on missing or empty values, and the AWS Secrets Manager backend. Reworded: the loading statement, to match the page.

Method: documentation only; no commands were run.
