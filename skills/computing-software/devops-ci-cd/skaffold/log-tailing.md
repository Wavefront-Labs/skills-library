---
id: computing-software.devops-ci-cd.skaffold.log-tailing
name: log-tailing
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [logs, tail, logging, json]
level: intro
status: docs-checked
description: "See container logs during dev and debug, enable them for run, and configure log prefixes and JSON log parsing."
sources:
  - "https://skaffold.dev/docs/log-tailing/"
  - "https://skaffold.dev/docs/references/yaml/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Skaffold tails logs from containers it built and deployed on your cluster to your local machine in `dev`, `debug` or `run` mode.

- Enabled by default for `skaffold dev` and `skaffold debug`.
- Disabled by default for `skaffold run`; enable with `--tail`.

Each log line is prefixed with the pod name and container name if they are not the same, and each container gets a unique color. The schema option `deploy.logs.prefix` (default `auto`) takes `container`, `podAndContainer` or `auto`.

For logs that are JSON objects, list the top-level fields to print under `deploy.logs.jsonParse.fields`:

```yaml
deploy:
  logs:
    jsonParse:
      fields: ["message", "severity"]
  kubectl: {}
```

With this config, a line like `[getting-started] {"severity":"INFO","message":"Hello World!","context":"default"}` is printed as `[getting-started] message: Hello World!, severity: INFO`.

## Checked

2026-11-04. Read the whole Skaffold Log Tailing page and the `LogsConfig` and `JSONParseConfig` definitions in the v4beta14 schema. Confirmed defaults per mode, prefix behaviour, colors, and the JSON parse example. Removed: the claims that logs are suppressed until status checking passes, that `--module` narrows noisy logs, that `--tail=false` is the way to turn tailing off, and the CI advice (none on the page). The schema text for the `auto` prefix value was truncated in my dump, so its exact meaning is not restated.
Method: documentation only; no commands were run.
