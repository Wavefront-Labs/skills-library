---
id: computing-software.cloud-infrastructure-engineering.datadog.agent-config-yaml
name: agent-config-yaml
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, datadog-yaml, agent-configuration, api-key, site]
level: practitioner
status: docs-checked
description: "Edit datadog.yaml (tags, logs_enabled, process_config, secrets), set the same options with DD_ variables, then restart and inspect the Agent."
sources: ["https://docs.datadoghq.com/agent/configuration/agent-configuration-files/", "https://docs.datadoghq.com/agent/guide/environment-variables/", "https://docs.datadoghq.com/agent/configuration/secrets-management/", "https://docs.datadoghq.com/getting_started/tagging/assigning_tags/", "https://docs.datadoghq.com/agent/supported_platforms/linux/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Agent configuration file datadog.yaml
Goal: configure the Agent declaratively.

Locations: `datadog.yaml` is `/etc/datadog-agent/datadog.yaml` on Linux and AIX, `/opt/datadog-agent/etc/datadog.yaml` on macOS and `%ProgramData%\Datadog\datadog.yaml` on Windows. Check and integration configs live in `conf.d` next to it (`/etc/datadog-agent/conf.d/` on Linux; each check has a `<CHECK_NAME>.d/` folder and you rename `conf.yaml.example` to `conf.yaml` to enable it; the Agent loads every valid YAML file in that folder).

```yaml
# /etc/datadog-agent/datadog.yaml
tags:
  - <KEY_1>:<VALUE_1>
  - <KEY_2>:<VALUE_2>
logs_enabled: true
process_config:
  process_collection:
    enabled: true
```

```
sudo datadog-agent configcheck
sudo systemctl restart datadog-agent
```

- `tags:` sets host tags applied to all metrics, traces and logs from the Agent; the hostname (tag key `host`) is assigned automatically and can be overridden in this file.
- `logs_enabled: true` turns on log collection; `process_config.process_collection.enabled: true` turns on Live Processes collection.
- Environment variables: most options can be set as `DD_` plus the uppercase option name (`hostname` becomes `DD_HOSTNAME`); list values are space separated; nested options with predefined keys join with underscores (`cluster_agent.cmd_port` becomes `DD_CLUSTER_AGENT_CMD_PORT`); nested options with user-defined keys must be JSON.
- Secrets: reference values as `ENC[<secret_id>]` in config and set `secret_backend_command` to the fetch executable. The `ENC[]` syntax cannot be used inside `secret_*` settings themselves.
- `configcheck` prints all configurations loaded and resolved by the running Agent.

Gotcha: restart the Agent after editing; changes in `datadog.yaml` are not applied to a running Agent.

## Verify
- `sudo datadog-agent status` lists the Logs Agent section after enabling logs.

## Checked
2026-11-03. Confirmed against the Agent Configuration Files, Environment Variables, Secrets Management, Assigning Tags, Live Processes and Linux platform pages. Removed: the `site`/`api_key`/`apm_config` sample block (apm_config is enabled by default per the tracing docs, `site` and `api_key` not re-verified here), `datadog-agent config` output claims, journalctl advice, and version-control advice.
Method: documentation only; no commands were run.
