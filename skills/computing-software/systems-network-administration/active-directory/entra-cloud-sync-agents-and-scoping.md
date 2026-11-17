---
id: computing-software.systems-network-administration.active-directory.entra-cloud-sync-agents-and-scoping
name: entra-cloud-sync-agents-and-scoping
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, entra-cloud-sync, cloud-sync, provisioning-agent, cloud-sync-scoping, gmsa, hybrid-identity, attribute-mapping, on-demand-provisioning]
level: practitioner
status: docs-checked
description: "Deploy Entra Cloud Sync: lightweight provisioning agents (3 for HA) with a gMSA, OU or group scoping, attribute mapping, on-demand provisioning tests and quarantine."
sources:
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/cloud-sync/how-to-install
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/cloud-sync/how-to-configure
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/cloud-sync/how-to-prerequisites
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entra Cloud Sync: agents and scoping

**What:** the sync engine runs in Entra; on-premises you install only small provisioning agents. Good for multi-forest
and disconnected-forest topologies. Provisioning runs on a scheduler about every two minutes.

## Install agents
- On a domain-joined Windows Server (2025 or 2022 recommended; 2016 and 2019 still listed; older versions only with
  paid extended support), 4 GB RAM minimum, .NET 4.7.1 or later. It can run on a domain controller or a dedicated server.
- Outbound 443 (and 80 for CRL downloads) to the Entra endpoints.
- Download the agent from the Entra admin center (Cloud sync > Agents). The installer creates a gMSA for AD access or
  accepts a custom gMSA. gMSA needs the forest schema at Windows Server 2012 or later and at least one 2012 or later DC.
  Domain Admin or Enterprise Admin credentials are needed to create the gMSA.
- Microsoft recommends 3 active agents for high availability; they serve the same configuration.
- Check: the services *Microsoft Entra Provisioning Agent* and *Microsoft Entra Connect Agent Updater* are running and the
  portal shows each agent active.

## Configure
Cloud sync > **New configuration** > **AD to Microsoft Entra ID sync**, choose the domain and whether to enable password
hash sync, then **Create**. The guided screen has five parts: scoping filters, attribute mappings, test, default
properties, enable.
- **Scoping filter:** all users, selected security groups, or selected organizational units. Group scoping does not
  support nested groups and Microsoft advises using it only for pilots; use OUs for production.
- **Attribute mapping:** defaults can be changed, deleted or extended; see the attribute-mapping skill.
- **Default properties:** notification email and accidental deletion prevention.
- Then **Enable configuration**. After a scope change use **Restart sync** to apply it immediately.

## Test without waiting
*Provision on demand* applies the configuration to one user or group and shows each step (import, scoping, matching,
actions) and the resulting attributes.

## Operations
- **Quarantine**: if most calls fail consistently (for example invalid admin credentials) the job is quarantined; fix it,
  then use Clear quarantine or Restart sync.
- Trace logs on agents: `%ProgramData%\Microsoft\Azure AD Connect Provisioning Agent\Trace`.
- A stopped agent shows Inactive after about an hour and is soft-deleted from the portal after about 10 days.

## Verify
- [ ] Agents show active; configuration healthy.
- [ ] Provision-on-demand of a test user succeeds and the user appears with the correct UPN.

## Checked
Checked 2026-10-27 against Microsoft Learn (entra-docs): Cloud Sync prerequisites, installation, configuration
(2026-03-30) and troubleshooting pages. Confirmed OS and gMSA prerequisites, the three-agent recommendation, scoping
options and nested-group limitation, the 2-minute scheduler, quarantine handling and agent removal timeline. Removed the
fixed gMSA name, the KDS root key statement and the sample UPN expression, which the pages do not state.
Method: documentation only; no commands were run.
