---
id: computing-software.cloud-infrastructure-engineering.datadog.agent-install
name: agent-install
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, agent-install, datadog-agent, install-script, agent-versions]
level: practitioner
status: docs-checked
description: "Install the Datadog Agent 7 on Linux with the official install script or package manager, set site, and check the service."
sources: ["https://docs.datadoghq.com/agent/supported_platforms/linux/", "https://docs.datadoghq.com/agent/guide/upgrade/", "https://docs.datadoghq.com/agent/configuration/network/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing the Datadog Agent
Goal: get a host reporting to Datadog with the Agent running as a service.

The Linux page says to follow the in-app instructions in Fleet Automation and run the generated script on your hosts. The documented install script (also used in the upgrade and tracing guides) is:

```
DD_API_KEY=<DD_API_KEY> DD_SITE="datadoghq.com" bash -c "$(curl -L https://install.datadoghq.com/scripts/install_script_agent7.sh)"
sudo systemctl status datadog-agent
sudo datadog-agent status
```

Windows: download `datadog-agent-7-latest.amd64.msi` (linked from the upgrade guide), run it as Administrator, and enter your API key when prompted.

- `DD_SITE` must match your Datadog region (`site` in `/etc/datadog-agent/datadog.yaml`; examples in the docs include `datadoghq.com` and `datadoghq.eu`); a wrong site shows the host never arriving.
- To upgrade an existing install with the same script, set `DD_UPGRADE="true"` (upgrade guide).
- For fleets, use configuration management or Fleet Automation rather than hand-run scripts.
- The Agent files include the `dd-agent` user. By default the IPC API listens on 5001/TCP, the APM receiver on 8126/TCP and DogStatsD on 8125/UDP (local only unless `dogstatsd_non_local_traffic` is set).

Gotcha: pasting the API key into shell history. Use a secrets manager or environment injection, and never commit the key. Most Agent data uses outbound port 443, so it must be allowed.

## Verify
- `sudo datadog-agent status` shows the Agent running and the host appears in Infrastructure List within a few minutes.

## Checked
2026-11-09. Confirmed against the Linux Agent page (config path, `site`, systemctl and status commands, `dd-agent` user, Fleet Automation install flow), the Agent 7 upgrade guide (install script URL, `DD_UPGRADE`, the Windows MSI name) and the network page (ports 5001, 8125, 8126, 443). Removed: `datadog-agent version` command, `us3.datadoghq.com` example, `DD_AGENT_MINOR_VERSION` pinning, the msiexec silent-install parameters, and the "API key valid / Forwarder" status wording, none of which appear in the fetched pages.
Method: documentation only; no commands were run.
