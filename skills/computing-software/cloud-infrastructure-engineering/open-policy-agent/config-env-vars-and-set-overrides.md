---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.config-env-vars-and-set-overrides
name: config-env-vars-and-set-overrides
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [configuration, set-file, environment-variables, opa-run, secrets]
level: practitioner
status: docs-checked
description: "Inject values into OPA configuration with ${ENV} substitution, --set and --set-file overrides for secrets, and the list-override limitation."
sources:
  - https://www.openpolicyagent.org/docs/configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: one configuration file, with per-environment values and secrets supplied at run time. These features work only with the OPA runtime (`opa run`).

Environment variables: `${...}` in the config file is replaced when the file loads.

```yaml
services:
  acmecorp:
    url: "${BASE_URL}"
    credentials:
      bearer:
        token: "${BEARER_TOKEN}"
```

Substitution does not take place if the variable is undefined, so check that every variable is set.

CLI overrides: `--set` and `--set-file` take `key=value`, where the key is a selector into the YAML structure. They override values in the config file. `decision_logs.reporting.min_delay_seconds=300` is equivalent to `{"decision_logs": {"reporting": {"min_delay_seconds": 300}}}`. Pass several values comma-separated or with repeated flags:

```
opa run \
  --set "default_decision=/http/example/authz/allow" \
  --set "services.acmecorp.url=https://test-env/control-plane-api/v1" \
  --set "labels.app=myapp,labels.region=west"
```

`--set-file` reads the value from a file, which keeps secrets out of the command line:

```
opa run --set-file "services.acmecorp.credentials.bearer.token=/path/to/bearer_token.txt"
```

List limitation: overrides cannot patch sub-objects of a list entry; they overwrite the entire index with the new object. Rewrite the whole list element when overriding something inside a list.

Hot reload: `opa run -s -c opa-config.yaml --watch-config` restarts the server's configuration-driven parts when the file changes (server mode only). Overrides are re-applied on each reload, but `--set-file` files are re-read only when the config file next changes.

Check: start with `--set` overriding a service URL and confirm the override wins over the file value in the bundle download logs.

## Checked

2026-11-04. Confirmed against the OPA docs Configuration page sections Using Environment Variables in Configuration, Setting Configuration via CLI Arguments (--set, --set-file, comma separation, list override limitation) and Reloading Configuration (--watch-config, server mode only, overrides re-applied, --set-file files re-read but not watched). Removed the claim that an undefined variable leaves literal ${...} text, because the page only says substitution does not take place.

Method: documentation only; no commands were run.
