---
id: computing-software.systems-network-administration.home-assistant.check-config-script
name: check-config-script
category: computing-software
field: systems-network-administration
product: home-assistant
tags: [check-config, hass, fail-on-warnings]
level: practitioner
status: docs-checked
description: "Validate configuration.yaml from the shell with hass --script check_config, including config directory, files list, secrets, JSON output and warning exit codes."
sources:
  - https://www.home-assistant.io/docs/tools/check_config/
  - https://www.home-assistant.io/docs/configuration/troubleshooting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: test configuration changes before launching or restarting Home Assistant.

Basic run:

```bash
hass --script check_config
```

Options as printed by the script's help:

```text
usage: hass [-h] [--script {check_config}] [-c CONFIG] [-i [INFO]] [-f] [-s] [--json] [--fail-on-warnings]

  -c CONFIG, --config CONFIG   Directory that contains the Home Assistant configuration
  -i [INFO], --info [INFO]     Show a portion of the config
  -f, --files                  Show used configuration files
  -s, --secrets                Show secret information
  --json                       Output JSON format
  --fail-on-warnings           Exit non-zero if warnings are present
```

Examples:

```bash
hass --script check_config -c /path/to/config
hass --script check_config -c /path/to/config --files
hass --script check_config -c /path/to/config --json --fail-on-warnings
```

Use `-c` when the configuration is not in the default directory. Use `--secrets` for debugging only, since it shows secret information. `--fail-on-warnings` makes the exit code non-zero on warnings, which suits CI or a pre-restart script.

On Home Assistant OS and Container installs, the docs point to their own CLI and container configuration-check sections; in the UI use Settings > Tools > YAML > Check configuration.

## Checked

2026-11-04. Confirmed against the Check configuration page and the Troubleshooting page (Home Assistant OS and Container CLI sections). Changed the UI path to Settings > Tools > YAML > Check configuration.

Method: documentation only; no commands were run.
