---
id: computing-software.cloud-infrastructure-engineering.azure.entra-cloud-sync-provisioning-agent
name: entra-cloud-sync-provisioning-agent
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, entra-id, cloud-sync, provisioning-agent, hybrid-identity, active-directory, gmsa, multi-forest, high-availability]
level: practitioner
status: docs-checked
description: "Install and verify the Microsoft Entra provisioning agent for Cloud Sync: gMSA choice, multi-agent HA, disconnected forests, and what runs in the cloud versus on-premises."
sources: ["https://learn.microsoft.com/en-us/entra/identity/hybrid/cloud-sync/what-is-cloud-sync", "https://learn.microsoft.com/en-us/entra/identity/hybrid/cloud-sync/how-to-install"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entra Cloud Sync — lightweight agent-based AD to Entra provisioning

**Goal:** sync a forest (or a disconnected or acquired forest) to Entra ID with a light agent
and cloud-managed configuration, instead of or alongside Entra Connect Sync.

## 1. What it is
Cloud Sync synchronises users, groups and contacts between Active Directory and Entra ID, and
with device sync enabled can sync computer objects for hybrid join. Configuration lives in
the cloud (Entra admin center); the on-premises piece is the provisioning agent, which needs
only outbound connections (via Azure Service Bus) and updates itself. The cloud service uses
SCIM and runs a scheduler-based cycle with synchronisation every two minutes. It also supports
group provisioning from Entra to Active Directory.
Strengths per the docs: multiple active agents give automatic failover without configuration
changes; multiple disconnected forests to one tenant without consolidation; the agent can run
on a domain controller or a dedicated server.
Coming from Connect Sync: follow Microsoft's migration decision guide first, then the guided
migration tool if your installation qualifies, otherwise a documented manual procedure, otherwise stay on Connect Sync.
Device sync is reviewed separately from guided-tool eligibility.

## 2. Install the agent
1. Run `AADConnectProvisioningAgentSetup.exe` from the downloaded package, accept the licence, **Install**, then the configuration wizard opens.
2. Sign in with at least the Hybrid Identity Administrator role.
3. On *Configure Service Account* pick a gMSA: **Create gMSA** (the agent creates `provAgentgMSA$` in the domain) or **Use custom gMSA** you created for this purpose.
4. On *Connect Active Directory* add your domain if it is not already listed, signing in with a domain administrator account whose password is not expired or changing during installation.
5. Install further agents on other servers for availability.
To move an existing agent to a gMSA, upgrade the agent to the latest version and run through the wizard again.

## 3. Verify
In the Entra admin center open Cloud Sync > **Agents**: the agent must appear with status active. On the server, check the local service (see the install page for the verification steps).
After installation the agent must still be configured and enabled (a new configuration) before users sync.
Password writeback for SSPR can be enabled in the portal or with PowerShell (see the install page).

## Gotchas
- Cloud Sync is available in the Commercial, US Government and 21Vianet clouds; SSPR for on-premises identities is not available with Cloud Sync in 21Vianet.
- Check the feature comparison page before choosing it over Connect Sync for a specific feature.

## Verify
- [ ] Cloud Sync > Agents shows each installed agent as active.
- [ ] A new configuration is created and enabled; users appear in Entra ID after a cycle.

## Checked
2026-10-28. Confirmed on the Learn pages "What is Microsoft Entra Cloud Sync?" and "Install the Microsoft Entra provisioning agent": architecture, two-minute cycle, multi-agent HA, disconnected forests, device sync, group provisioning to AD, installer name, role, gMSA options and name, domain-admin sign-in, agent verification, cloud availability note. Removed (not on those pages, or the troubleshooting/prerequisite pages were not fetched): server OS and RAM requirements, endpoint list and TLS, scoping/mapping defaults and limits, 500 deletion default, log and status names, PowerShell module paths and event-log commands, quarantine reasons, Set-AADCloudSyncPermissions, 250k-object and "Connect Sync still required" claims.
Method: documentation only; no commands were run.
