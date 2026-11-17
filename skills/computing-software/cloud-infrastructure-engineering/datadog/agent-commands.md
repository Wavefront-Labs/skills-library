---
id: computing-software.cloud-infrastructure-engineering.datadog.agent-commands
name: agent-commands
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, agent-status, agent-flare, health, diagnose]
level: practitioner
status: docs-checked
description: "Use datadog-agent status, health, check, configcheck, diagnose, stream-logs and flare to troubleshoot collection and connectivity."
sources: ["https://docs.datadoghq.com/agent/configuration/agent-commands/", "https://docs.datadoghq.com/agent/configuration/agent-status-page/", "https://docs.datadoghq.com/agent/troubleshooting/send_a_flare/", "https://docs.datadoghq.com/agent/troubleshooting/agent_check_status/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Agent CLI: status, flare, health, diagnose
Goal: diagnose an Agent that is not reporting.

```
sudo datadog-agent status
sudo datadog-agent health
sudo -u dd-agent datadog-agent check <CHECK_NAME>
sudo -u dd-agent datadog-agent check <CHECK_NAME> --check-rate
sudo datadog-agent configcheck
sudo datadog-agent diagnose
sudo datadog-agent stream-logs
sudo datadog-agent flare <CASE_ID>
```

In a container use `agent` instead: `docker exec -it <CONTAINER_NAME> agent status`, `kubectl exec -it <POD_NAME> -- agent status`. For the Cluster Agent the command is `datadog-cluster-agent status`.

- `status` prints the Agent status page: running checks (Metric Samples, Events, Service Checks, Last Run and Total), the Forwarder (transactions and Errors, plus whether each API key is valid) and, when enabled, the Logs Agent section.
- `check <CHECK_NAME>` runs a check once; add `--check-rate` to include rate metrics.
- `configcheck` prints all configurations loaded and resolved by the running Agent; `health` prints the Agent health; `diagnose` runs a connectivity diagnosis; `stream-logs` streams the logs a running Agent is processing.
- `flare <CASE_ID>` gathers configuration files and logs into an archive, removes sensitive information (passwords, API keys, proxy credentials, SNMP community strings), and prompts for confirmation before uploading, so you can review it first. It is not supported on the gov sites; use manual submission there. With Fleet Automation and Remote Configuration enabled a flare can also be sent from the Datadog site.

## Verify
- `datadog-agent check <CHECK_NAME>` runs without errors and the status page lists the check under running checks.

## Checked
2026-11-03. Confirmed against the Agent Commands, Agent Status Page, Send a Flare and Agent check status pages. Removed: `flare --email` (docs use a case ID argument), `stream-event-platform` (not in the command table), the "15 s interval" healthy-status claim, and the "Instances: 1" verification text.
Method: documentation only; no commands were run.
