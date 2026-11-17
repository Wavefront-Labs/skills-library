---
id: computing-software.cloud-infrastructure-engineering.azure.arc-server-onboarding-at-scale-with-service-principal
name: arc-server-onboarding-at-scale-with-service-principal
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-arc, arc-at-scale, arc-service-principal, azcmagent, connected-machine-onboarding, group-policy]
level: practitioner
status: docs-checked
description: "Onboard hundreds of servers to Azure Arc: onboarding service principal with least privilege, generated scripts, GPO/ConfigMgr/Ansible distribution and tagging."
sources: ["https://learn.microsoft.com/azure/azure-arc/servers/onboard-service-principal", "https://learn.microsoft.com/azure/azure-arc/servers/onboard-group-policy-powershell", "https://learn.microsoft.com/azure/azure-arc/servers/onboard-ansible-playbooks"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Arc onboarding at scale

**Goal:** connect a server estate to Azure Arc in waves, repeatably, with an identity that can do nothing else.

## 1. Onboarding identity
```bash
az ad sp create-for-rbac --name sp-arc-onboarding --role "Azure Connected Machine Onboarding" \
  --scopes /subscriptions/<sub>/resourceGroups/rg-arc-servers
```
The Azure Connected Machine Onboarding role is the documented role for onboarding (Contributor on the resource group also works); scope it to the target resource group or landing zone. The secret printed by `az ad sp create-for-rbac` is valid for one year, after which you must generate a new one and update the scripts, so store it in your deployment tool's vault and rotate it.

## 2. Generate the script
Portal: Azure Arc > Machines > Add > *Add multiple servers* > choose the service principal, region, RG, tags,
connectivity (public, proxy, or private endpoint). The core command (the `azcmagent connect` reference documents these flags):
```bash
azcmagent connect --service-principal-id "$SP_ID" --service-principal-secret "$SP_SECRET" \
  --tenant-id "$TENANT" --subscription-id "$SUB" --resource-group rg-arc-servers --location westeurope \
  --tags "Datacenter=DC1,Owner=infra" --cloud AzureCloud
```
Optional: `--private-link-scope` takes the private link scope resource ID; `--gateway-id` takes the Arc gateway resource ID and is required when using an Arc gateway; `--resource-name` overrides the machine's resource name.

## 3. Distribute
- **Windows / AD**: Group Policy with PowerShell (see the Group Policy onboarding page); scope the onboarding role to the target landing zone.
- **Linux and mixed estates**: Ansible playbooks. The identity Ansible uses (CLI user, service principal or managed identity) needs the Azure Connected Machine Onboarding role at subscription or resource group scope; a managed identity on an Azure VM or Arc-enabled control node is recommended for production. Dynamic inventory sources such as VMware vSphere, AWS or Azure can group hosts.

## Gotchas
- Don't install Arc on VMs hosted in Azure (use an Azure VM only to simulate on-premises for testing). For clones, restores and golden images, onboard after cloning with automation: two agents with the same source ID behave inconsistently.
- Network/firewall requirements must be in place before the wave - run `azcmagent check --location <REGION>` on a pilot.
- Without `--resource-name`, the resource name defaults to the hostname (the instance ID on AWS servers), so use `--resource-name` where hostnames collide.

## Verify
- [ ] The count of Arc machines in the resource group matches the target list and all show Connected; the onboarding secret is rotated before its expiry.

## Checked
Date: 2026-10-31. Confirmed against Learn pages: Connect hybrid machines at scale with a service principal, Group Policy (PowerShell) onboarding, Ansible onboarding, `azcmagent connect`, `azcmagent check` and Arc-enabled servers prerequisites (onboarding role, one-year secret, connect flags, Arc gateway flag, cloned/golden image guidance, Azure VM guidance).
Removed as unconfirmed: the claims that the role can only create or read machine resources and that the SP is not used afterwards, the ConfigMgr and scheduled-task distribution details, the install script name, VMware/SCVMM agent-install claim, the post-onboarding policy baseline, and the Resource Graph query.
Method: documentation only; no commands were run.
