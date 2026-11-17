---
id: computing-software.systems-network-administration.windows-server.arc-agent-troubleshooting
name: arc-agent-troubleshooting
category: computing-software
field: systems-network-administration
product: windows-server
tags: [azure-arc, azcmagent-check, azcmagent, arc-onboarding, proxy]
level: practitioner
status: docs-checked
description: "Troubleshoot the Azure Connected Machine agent: azcmagent check and show, logs, proxy and private link endpoints, expired identity and disconnected status."
sources:
  - https://learn.microsoft.com/en-us/azure/azure-arc/servers/troubleshoot-agent-onboard
  - https://learn.microsoft.com/en-us/azure/azure-arc/servers/manage-agent
  - https://learn.microsoft.com/en-us/azure/azure-arc/servers/agent-overview
  - https://learn.microsoft.com/en-us/azure/azure-arc/servers/azcmagent-check
  - https://learn.microsoft.com/en-us/azure/azure-arc/servers/agent-release-notes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Arc Connected Machine agent troubleshooting

## Status
```cmd
azcmagent show
azcmagent show "Agent Status" "Agent Last Heartbeat"
```
Shows whether the agent is connected, resource information and the status of its dependent services; no admin rights
needed. Services: `himds` (identity and heartbeat), `ExtensionService` and `GCArcService` (machine configuration).

## Connectivity test
```cmd
azcmagent check --location uksouth
azcmagent check --location uksouth --enable-pls-check     :: private link scope
```
`--location` is the Azure region (use `--cloud` for non-public clouds); the check tests the endpoints the agent needs.
Compare failures with the network requirements page.

## Proxy config
```cmd
azcmagent config set proxy.url "http://<proxy-host>:8080"
azcmagent config clear proxy.url
azcmagent config list
```

## Logs
- `%ProgramData%\AzureConnectedMachineAgent\Log\himds.log` (heartbeat and identity) and `azcmagent.log` (output of
  azcmagent commands; add `--verbose` to a command for detail).
- `%ProgramData%\GuestConfig\arc_policy_logs\gc_agent.log` (machine configuration), `%ProgramData%\GuestConfig\ext_mgr_logs\gc_ext.log`
  (extension install/upgrade) and `%ProgramData%\GuestConfig\extension_logs` (per extension).
- `azcmagent logs` collects the logs into a zip (`--full` for everything, `--output` for the path).

## Disconnected or duplicate identity
- Failed or half-finished onboarding: delete the resource in Azure if needed, then clear the local state:
```cmd
azcmagent disconnect --force-local-only
azcmagent connect --resource-group <rg> --tenant-id <tenant> --location <region> --subscription-id <sub> --service-principal-id <id> --service-principal-secret <secret>
```
- Machines cloned after onboarding fight over one resource (HTTP 429 errors): run
  `azcmagent disconnect --force-local-only` on each clone, then connect again with a unique resource name.

## Agent support
Only agent versions released within the last year are supported; update, or use automatic agent upgrade (preview,
`--enable-automatic-upgrade` on connect). The release notes page listed version 1.69 (October 2026) and warns that
from February 2027 the agent no longer accepts certificates with negative serial numbers.

## Verify
- [ ] `azcmagent show` reports connected with a recent heartbeat; extension installs succeed.

## Checked
Date 2026-10-27. Documentation: Azure Connected Machine agent overview (services, log paths), azcmagent show, check,
config, disconnect and logs references, onboarding troubleshooting page, agent release notes. Confirmed: commands and
flags above, log locations, clone remediation, one-year support window.
Method: documentation only; no commands were run.
