---
id: computing-software.systems-network-administration.windows-server.disable-unneeded-services-and-features
name: disable-unneeded-services-and-features
category: computing-software
field: systems-network-administration
product: windows-server
tags: [os-hardening, windows-server-hardening, disable-unneeded-services, print-spooler, attack-surface-reduction]
level: practitioner
status: docs-checked
description: "Reduce Windows Server attack surface by role: services Microsoft lists as candidates to disable (Spooler, Remote Registry, SSDP) and verifying nothing breaks."
sources:
  - https://learn.microsoft.com/en-us/windows-server/security/windows-services/security-guidelines-for-disabling-system-services-in-windows-server
  - https://learn.microsoft.com/en-us/windows-server/security/osconfig/osconfig-overview
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Disabling unneeded services and features

## Principles
- Disable services per server role by GPO so the setting is enforced, not just set once.

## Commonly disabled
| Service | Name | Where |
|---|---|---|
| Print Spooler | Spooler | see the DC print-pruning caveat below |
| Xbox Live Auth Manager | XblAuthManager | check the guidance page |
| Remote Registry | RemoteRegistry | only if no tooling needs it |
| SSDP Discovery | SSDPSRV | check the guidance page |
| Downloaded Maps Manager | MapsBroker | check the guidance page |

Domain controller caveat from Microsoft's guidance: the DC role adds a thread to the spooler service that prunes stale print queue objects from Active Directory. If the spooler is not running on at least one DC in each site, AD cannot remove old queues.

Microsoft's guidance document classifies each Desktop Experience service as OK to disable or not.

## Apply
```powershell
Stop-Service Spooler; Set-Service Spooler -StartupType Disabled
```
Enforce the same setting by GPO, scoped to the server OUs that do not need the service.

## Test before broad rollout
Pilot each change per role before broad rollout.

## Verify
```powershell
Get-Service Spooler | Select-Object Status, StartType
```
- [ ] Spooler state matches the role baseline, keeping it running on at least one DC per site if print pruning is needed.

## Checked
2026-10-28: Confirmed on Learn page security-guidelines-for-disabling-system-services-in-windows-server: service names Spooler, RemoteRegistry, SSDPSRV, MapsBroker, XblAuthManager are listed in the guidance, and the Print Spooler comment about DC print pruning (this corrects the earlier advice to disable Spooler on all DCs). `Set-Service -StartupType` confirmed on its Learn page. Also removed: Server Core claim, the System Services GPO path and the Get-ADDomainController command (page not found). Removed: WebClient, Fax, WerSvc, upnphost, lfsvc, PhoneSvc, RetailDemo and the other Xbox services (not found in the fetched page), Uninstall-WindowsFeature -Remove claim, feature removal examples, rationale text (PrintNightmare, coercion), side-effect claims.
Method: documentation only; no commands were run.
