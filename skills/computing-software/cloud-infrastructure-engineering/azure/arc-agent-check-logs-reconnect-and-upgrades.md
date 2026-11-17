---
id: computing-software.cloud-infrastructure-engineering.azure.arc-agent-check-logs-reconnect-and-upgrades
name: arc-agent-check-logs-reconnect-and-upgrades
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-arc, azcmagent-check, arc-agent-upgrade, arc-troubleshooting, connected-machine-agent, proxy]
level: practitioner
status: docs-checked
description: "Troubleshoot the Azure Connected Machine agent: azcmagent check, verbose log paths, himds service errors, reconnect and agent upgrade methods."
sources: ["https://learn.microsoft.com/azure/azure-arc/servers/troubleshoot-agent-onboard", "https://learn.microsoft.com/azure/azure-arc/servers/azcmagent-check", "https://learn.microsoft.com/azure/azure-arc/servers/manage-agent"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Arc agent troubleshooting and upgrades

**Goal:** get an Arc server that fails to connect healthy again and keep agents current.

## Connectivity check (on the server, as admin)
```bash
azcmagent check
azcmagent check --location "eastus"
azcmagent check --location "centralindia" --enable-pls-check
azcmagent check --extensions all
```
- `azcmagent check` prints a table of results per required endpoint, including whether a private endpoint, proxy server or Arc gateway was used.
- With no flags it uses the agent's configured cloud and region. `--location` picks a region to test; `--cloud` (AzureCloud, AzureUSGovernment, AzureChinaCloud) must be used with `--location`.
- `--enable-pls-check` checks that Arc endpoints resolve to private IP addresses; use it when connecting through an Azure Arc private link scope.
- `--extensions` (`all` or `sql`) adds extension endpoint checks; it needs agent version 1.41 or later. `--include-all` adds checks for extended use cases.

## Logs and errors
- The verbose log (written by `azcmagent` commands run with `-v`/`--verbose`) is at `%ProgramData%\AzureConnectedMachineAgent\Log\azcmagent.log` on Windows and `/var/opt/azcmagent/log/azcmagent.log` on Linux.
- Run azcmagent as administrator/root. Errors such as AZCM0061 and exit code 4 or 61/64 mean the Hybrid Instance Metadata Service (HIMDS, `himds`) is not running or not responding: start or restart it and retry.
- "Machine already connected" (AZCM0067, exit code 67): run `azcmagent disconnect`, then connect again.
- AZCM0063 (error while disconnecting): if it persists, delete the resource in Azure and run `azcmagent disconnect --force-local-only` on the server.
- Exit code 44, resource already exists: use a different `--resource-name` or delete the existing Arc server resource and rerun `azcmagent connect`.

## Upgrades
- Microsoft supports officially only agent versions released within the last year. You do not need to restart the server to install, upgrade or uninstall the agent.
- Automatic Agent Upgrade: Microsoft manages the rollout in batches during off-peak hours.
- Windows: Microsoft Update, Microsoft Update Catalog, the MSI from `https://aka.ms/AzureConnectedMachineAgent`, or Azure Update Manager. Windows Server does not check Microsoft Update by default: enable "other Microsoft products" (Group Policy: Configure Automatic Updates, "Install updates for other Microsoft products"). For WSUS/Configuration Manager, synchronize the product "Azure Connected Machine Agent" with classifications Critical Updates and Updates.
- Silent MSI upgrade: `msiexec.exe /i AzureConnectedMachineAgent.msi /qn /l*v "<log path>"`.
- Linux (root or sudo): `sudo apt update` then `sudo apt upgrade azcmagent`; `sudo yum check-update` then `sudo yum update azcmagent`; `sudo zypper refresh` then `sudo zypper update azcmagent`. Azure Update Manager also works.
- To install a specific version, uninstall the current one and install the target (apt: `sudo apt install azcmagent=VERSION`); no disconnect is needed.
- Azure Advisor flags machines that are not on the latest agent version.

## Verify
- [ ] `azcmagent check` reports every required endpoint reachable and the machine shows Connected in Azure.

## Checked

Method: docs-checked 2026-11-09 against the Learn pages troubleshoot-agent-onboard, azcmagent-check and manage-agent (read in full). Removed unconfirmed claims: azcmagent show/logs --full, himds.log path, the 45-day Expired rule, proxy config commands, cloned-machine advice, the Resource Graph version query and the --only-upgrade form.
