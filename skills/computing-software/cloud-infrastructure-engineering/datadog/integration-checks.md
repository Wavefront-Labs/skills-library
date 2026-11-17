---
id: computing-software.cloud-infrastructure-engineering.datadog.integration-checks
name: integration-checks
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, conf-d, integrations, check-config, yaml-check]
level: practitioner
status: docs-checked
description: "Enable an Agent integration by creating conf.d/<name>.d/conf.yaml, with init_config, instances, tags and validation."
sources: ["https://docs.datadoghq.com/getting_started/integrations/", "https://docs.datadoghq.com/agent/configuration/agent-commands/", "https://docs.datadoghq.com/extend/custom_checks/write_agent_check/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Integration checks and conf.d
Goal: collect metrics from a service such as Apache.

```yaml
# conf.d/apache.d/conf.yaml (minimum from the docs)
init_config:
  service: apache

instances:
    - apache_status_url: http://localhost/server-status?auto

logs:
    - type: file
      path: /var/log/apache2/access.log
      source: apache
      sourcecategory: http_web_access
```

- In the Agent's configuration directory, `conf.d` holds one `<INTEGRATION_NAME>.d` folder per integration containing `conf.yaml.example`, which lists every option. To activate: rename it to `conf.yaml`, set the parameters for your environment, then restart the Agent.
- Monitor several instances in one check by adding more entries under `instances`.
- Setting `service` in the config is the recommended setup for separate, independent systems. Metrics from containerised checks carry auto-detected tags such as `image_name`; set `ignore_autodiscovery_tags: true` to turn that off.
- Validate with the Agent `status` subcommand (`sudo datadog-agent status` on Linux) and look for the new configuration under Checks. `datadog-agent configcheck` prints the loaded and resolved configurations, and `check` runs a named check.
- Custom checks: put `custom_<name>.py` in `checks.d` (class extending `AgentCheck`) and a config file with the same name, `conf.d/custom_<name>.yaml`. The docs advise the `custom_` prefix to avoid clashing with an existing integration.
- Custom check `min_collection_interval` defaults to 15 seconds and is set per instance. The Agent may queue a check behind others, and if a run takes longer than the interval the next execution is skipped.

Gotcha: a custom check with a mismatched config file name will not load, and a custom name that equals an existing integration conflicts with it.

## Verify
- `sudo datadog-agent status` lists the check under Checks after the restart.

## Checked
2026-11-09. Confirmed against the Integrations getting started, Agent commands and Write a custom Agent check pages (conf.d layout, rename and restart steps, apache example, multiple instances, service setting, autodiscovery tags, status validation, configcheck and check subcommands, custom check file naming, interval behaviour). Removed: the nginx example and `tags: service:web`, `systemctl restart`, `grep -A8` and `datadog-agent check nginx` invocations, the `conf.d/<name>.d/conf.yaml` form for custom checks (docs use `conf.d/<name>.yaml`), the `ENC[]` credentials claim, the "files are ignored without the .d directory" claim, the dedicated read-only database user advice, the enable-the-tile advice, the `[OK]` status text and `nginx.net.connections` metric, and the roll-out-to-one-host advice.
Method: documentation only; no commands were run.
