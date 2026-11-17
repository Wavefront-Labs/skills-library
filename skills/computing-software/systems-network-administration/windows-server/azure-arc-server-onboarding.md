---
id: computing-software.systems-network-administration.windows-server.azure-arc-server-onboarding
name: azure-arc-server-onboarding
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, azure-arc, arc-enabled-servers, azcmagent, arc-onboarding, service-principal, connected-machine-agent, proxy, private-link, hybrid]
level: practitioner
status: docs-checked
description: "Onboard Windows servers to Azure Arc at scale: Connected Machine agent, service principal script, proxy and private link options, tags, and azcmagent checks."
sources:
  - https://learn.microsoft.com/en-us/azure/azure-arc/servers/onboard-service-principal
  - https://learn.microsoft.com/en-us/azure/azure-arc/servers/prerequisites
  - https://learn.microsoft.com/en-us/azure/azure-arc/servers/manage-agent
  - https://learn.microsoft.com/en-us/azure/azure-arc/servers/security-extensions
  - https://learn.microsoft.com/en-us/azure/azure-arc/servers/azcmagent
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Onboard servers to Azure Arc

**Goal:** on-prem/other-cloud Windows servers appear as Azure resources so Azure Policy,
Update Manager, Monitor, Defender and other Azure services can manage them.

## Prepare
- Resource group(s) per environment; resource providers registered in the subscription:
  `Microsoft.HybridCompute`, `Microsoft.GuestConfiguration`, `Microsoft.HybridConnectivity` (and
  `Microsoft.AzureArcData` only for SQL Server).
- OS: Windows Server Desktop and Server Core editions are supported (see the prerequisites matrix for versions; the
  agent is not tested on CIS-hardened images). Windows Server 2012/2012 R2 ESUs ended on 13 Oct 2026.
- Network: outbound 443 to the documented Arc endpoints (or via proxy, or Azure Private Link Scope). Run
  `azcmagent check` to validate.
- **Service principal for at-scale onboarding** with only the *Azure Connected Machine Onboarding* role. The secret
  created by `az ad sp create-for-rbac` is valid for one year; the principal is used only for onboarding.

## Onboard
Portal > Azure Arc > Machines > Add > "Add multiple servers" generates a script. Core of it:
```powershell
# download and install the agent (latest installer)
Invoke-WebRequest -Uri https://aka.ms/AzureConnectedMachineAgent -OutFile AzureConnectedMachineAgent.msi
msiexec /i AzureConnectedMachineAgent.msi /qn /l*v arc-install.log
& "$env:ProgramFiles\AzureConnectedMachineAgent\azcmagent.exe" connect `
  --service-principal-id <APP_ID> --service-principal-secret <SECRET> `
  --tenant-id <TENANT_ID> --subscription-id <SUB_ID> --resource-group <rg> `
  --location <region> --tags "env=prod,site=lon" --cloud AzureCloud
```
Deliver at scale with a Group Policy scheduled task (Microsoft documents this), Configuration Manager, or other
tooling. Never leave the secret in a world-readable share. `--enable-automatic-upgrade` (preview) opts into
automatic agent upgrades.

Proxy: `azcmagent config set proxy.url http://<proxy-host>:8080`.

## After
```powershell
azcmagent show            # status, resource ID
azcmagent check           # connectivity tests
azcmagent config list
```
Lock down on sensitive servers (domain controllers, payment data): allow only the extensions you expect, locally,
because anyone with the right Azure RBAC role could otherwise push an extension (Custom Script and Run Command run as
Local System):
`azcmagent config set extensions.allowlist "Microsoft.Azure.Monitor/AzureMonitorWindowsAgent"`.
Allow lists cannot be overridden from Azure, even by an Owner.

## Verify
- [ ] Servers show Connected in Azure Arc with correct tags.
- [ ] The SP secret is rotated or removed after onboarding.
- [ ] Extension allowlist set on sensitive servers.

## Checked
Date 2026-10-27. Documentation: Arc service principal onboarding page, prerequisites (resource providers, OS support,
ESU note), manage-agent (installer URL, automatic upgrade), security-extensions page (allow lists), azcmagent
reference. Confirmed: providers, role name, secret lifetime, agent path, connect flags, allow list behaviour.
Method: documentation only; no commands were run.
