---
id: computing-software.systems-network-administration.active-directory.entra-connect-health
name: entra-connect-health
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, entra-connect, entra-connect-health, connect-health-agent, ad-ds-health, adfs-health, sync-health, alerts, hybrid-identity, monitoring]
level: practitioner
status: docs-checked
description: "Monitor hybrid identity with Microsoft Entra Connect Health: sync, AD FS and AD DS agents, alert routing, sync error reports and what each alert means."
sources:
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-health-agent-install
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-health-sync
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/connect/how-to-connect-health-alert-catalog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entra Connect Health

**Requires** Microsoft Entra ID P1 or P2. Registering agents needs a Global Administrator or Hybrid Identity
Administrator (less-privileged identities can be allowed through Azure RBAC). The agent supports Windows Server 2016, 2019,
2022 and 2025, needs PowerShell 5.0 or later, and uses outbound TCP 443 (older agent versions also need 5671; the latest
version does not). Open Connect Health from the Entra admin center (aka.ms/aadconnecthealth).

| Agent | Installed on | What you get |
|---|---|---|
| Sync | with Entra Connect (active when Connect was installed by a Hybrid Identity Administrator) | sync service overview, alerts, object-level sync error report, latency and export statistics charts |
| AD FS | each AD FS and Web Application Proxy server | usage, failed sign-ins, security reports including the Risky IP report, certificate alerts |
| AD DS | each domain controller | domain controller summary, alerts, replication status dashboard, LDAP bind, NTLM and Kerberos performance charts |

## Install the AD DS / AD FS agents
Download from the portal and run the agent setup (`AdHealthAddsAgentSetup.exe` for AD DS), then register with a Global
Administrator or Hybrid Identity Administrator account. A silent AD DS install uses
`AdHealthAddsAgentSetup.exe /quiet AddsMonitoringEnabled=1 SkipRegistration=1`, followed by registration with the
`AdHealthConfiguration` module. For AD FS usage data, AD FS auditing must be enabled: the "AD FS Auditing is disabled"
alert gives the steps (including granting the AD FS service account the "Generate security audits" right).

## Alerts
- Configure notification email to a monitored mailbox or ticket queue, not just Global Administrators.
- Catalog examples: Password Hash Synchronization heartbeat skipped in the last 120 minutes; Password Hash
  Synchronization stopped; AD FS TLS and token-signing certificates expiring within 90 days; AD FS auditing disabled.
  The full list is in the Connect Health alert catalog.
- Review the alert history after incidents.

## Reports to use
- **Sync errors**: object-level error report. Connect Health does not upload these events if Connect uses a non-default
  configuration such as changed attribute filtering.
- **Risky IP** (AD FS): IPs with many failed sign-ins, useful where an attacker stays under the extranet lockout threshold.

## Verify
- [ ] Every DC and AD FS server shows healthy with recent data.
- [ ] Alert routing works: confirm a test or real alert reaches the intended mailbox.

## Checked
Checked 2026-10-27 against Microsoft Learn (entra-docs): Connect Health agent install, operations, sync, AD DS and AD FS
pages and the alert catalog. Confirmed the P1/P2 requirement, supported server versions, ports, installer name, the
120-minute and 90-day alerts, and the sync-error caveat. Removed the `Set-AzureAdConnectHealthProxySettings` cmdlet and
the `auditpol` and `Set-AdfsProperties` commands (not on the cited pages), and the "stop the scheduler to test alerting"
step.
Method: documentation only; no commands were run.
