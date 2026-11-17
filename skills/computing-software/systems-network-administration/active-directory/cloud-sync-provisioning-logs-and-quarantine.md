---
id: computing-software.systems-network-administration.active-directory.cloud-sync-provisioning-logs-and-quarantine
name: cloud-sync-provisioning-logs-and-quarantine
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, entra-cloud-sync, cloud-sync-quarantine, provisioning-logs, provisioning-agent]
level: practitioner
status: docs-checked
description: "Troubleshoot Entra Cloud Sync: read provisioning logs, clear quarantine, check agent health and gMSA permissions, and use on-demand provisioning."
sources:
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/cloud-sync/how-to-troubleshoot
  - https://learn.microsoft.com/en-us/entra/identity/app-provisioning/application-provisioning-quarantine-status
  - https://learn.microsoft.com/en-us/entra/identity/hybrid/cloud-sync/how-to-gmsa-cmdlets
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Sync provisioning logs and quarantine

## Where to look
- Entra admin center > Cloud sync > the configuration > **Logs** (provisioning logs): every object action with step
  details. Filter by date, or search by the AD object's `ObjectGuid`. A `Skipped` entry showing only a source ID usually
  means the agent filtered an out-of-scope object (by default, objects with `IsCriticalSystemObject` set to TRUE, which
  includes many built-in users and groups, and replication victim objects are excluded).
- Agent server: trace logs are in `%ProgramData%\Microsoft\Azure AD Connect Provisioning Agent\Trace`. For more
  detail install the AADCloudSyncTools module and run `Export-AADCloudSyncToolsLogs` (options `SkipVerboseTrace`,
  `TracingDurationMins` with a 3-minute default, and `OutputPath`).

## Quarantine
If most or all calls to the target consistently fail (for example invalid admin credentials), the job is marked
quarantined. Select the status for the error code and message. There are two ways to resolve it once the cause is fixed:
- **Clear quarantine** (right-click the status): clears the watermark and runs a delta sync.
- **Restart sync** on the configuration page (or the Graph `restart` call, which can clear escrows, quarantine and
  watermarks selectively).
Typical causes: the agent's gMSA lost permissions in AD, the agents cannot reach the required endpoints, or a deletion
threshold was hit. Error `AzureDirectoryServiceAuthorizationFailed` usually means the tenant lacks the "Microsoft Entra
AD Synchronization Service" service principal; the troubleshooting page shows how to restore it, and errors can take up
to 24 hours to clear.

## Agent health
Check on the server that the services **Microsoft Entra Provisioning Agent** and **Microsoft Entra Connect Agent
Updater** are running, and in the portal that each agent shows active (green). Microsoft recommends 3 active agents for
high availability. Outbound ports 80 (CRL downloads) and 443 must be open; allow `*.msappproxy.net` and
`*.servicebus.windows.net` on 443 and avoid TLS inspection on that traffic. The agent supports an outbound proxy set in
`AADConnectProvisioningAgent.exe.config` under the agent install folder.

## gMSA permissions
Grant the agent's service account rights again with the agent PowerShell cmdlets:
```powershell
$credential = Get-Credential
Set-AADCloudSyncPermissions -PermissionType All -TargetDomain "<DOMAIN_FQDN>" -TargetDomainCredential $credential
```
Supported permission types: BasicRead, PasswordHashSync, PasswordWriteBack, HybridExchangePermissions,
ExchangeMailPublicFolderPermissions, UserGroupCreateDelete and All.

## Provision on demand
Configuration > Provision on demand > enter an object distinguished name: runs one object through the pipeline and
shows each step, the fastest way to debug scoping and attribute mapping.

## Verify
- [ ] Status Healthy, no quarantine, last cycle time recent.
- [ ] On-demand provisioning of a test user succeeds end to end.

## Checked
Checked 2026-10-27 against Microsoft Learn (entra-docs): Cloud Sync troubleshooting (dated 2026-08-21), the agent gMSA
cmdlet page and the prerequisites page. Confirmed service display names, ports and URLs, the trace folder,
`Export-AADCloudSyncToolsLogs`, Clear quarantine versus Restart sync, and the permission types. Replaced the service
names `AADConnectProvisioningAgent` and `WAUpdaterService`, the unsourced Event Viewer path and the parameter set for
`Set-AADCloudSyncPermissions`, and dropped the claim that Restart sync always forces a full cycle.
Method: documentation only; no commands were run.
