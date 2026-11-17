---
id: computing-software.systems-network-administration.powershell.wsman-quotas-and-timeouts
name: wsman-quotas-and-timeouts
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, ps-remoting, wsman-quotas, maxenvelopesize, winrm]
level: advanced
status: docs-checked
description: "Tune WSMan quotas and timeouts: documented WinRM defaults for envelope size, shell memory, shells per user, idle timeout; quota and timeout errors; PSSessionOption."
sources:
  - https://learn.microsoft.com/en-us/windows/win32/winrm/installation-and-configuration-for-windows-remote-management
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_remote_troubleshooting
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# WSMan quotas and timeouts

## Documented defaults (win32 WinRM configuration page)
| Setting | Default | Meaning |
|---|---|---|
| MaxEnvelopeSizekb | 150 | Max SOAP data; behaviour unsupported above 1039440 |
| MaxTimeoutms | 60000 | Max timeout for any request except Pull |
| MaxBatchItems | 32000 | Max elements in a Pull response |
| MaxProviderRequests | 25 | Concurrent requests; deprecated and read-only from WinRM 2.0 |
| MaxConcurrentOperations | 100 | Deprecated in WinRM 2.0, replaced by MaxConcurrentOperationsPerUser |
| MaxConcurrentOperationsPerUser | 1500 | Per-user concurrent operations on a system |
| EnumerationTimeoutms | 60000 | Idle time between Pull messages |
| MaxConnections | 300 (25 in WinRM 2.0) | Active requests processed at once |
| MaxPacketRetrievalTimeSeconds | 120 | Time to retrieve a packet |
| NetworkDelayms (client) | 5000 | Extra wait for network delay |
| Winrs IdleTimeout | WinRM 2.0: 180000 ms, minimum 60000 | Idle remote shell removed after this |
| Winrs MaxConcurrentUsers | 5 | Users concurrently running remote shell operations |
| Winrs MaxShellRunTime | 28800000 ms | Read-only in WinRM 2.0, changing it has no effect |
| Winrs MaxProcessesPerShell | 15 (0 = unlimited) | Processes per shell operation |
| Winrs MaxMemoryPerShellMB | 150 | Memory per shell including children |
| Winrs MaxShellsPerUser | 5 when policy is disabled or unset | Concurrent shells per user |

These defaults are as documented on that page; verify the live values on your build before relying on them.

## Errors and fixes (about_Remote_Troubleshooting)
- Quota conflict: "The total data received from the remote client exceeded allowed maximum". Change the command to fit or raise the quota. Settings: MaxEnvelopeSizeKB and MaxProviderRequests in the `WSMan:<ComputerName>` node; MaxConcurrentOperations, MaxConcurrentOperationsPerUser and MaxConnections under `...\Service`. Protect the client with `New-PSSessionOption -MaximumReceivedDataSizePerCommand / -MaximumReceivedObjectSize` or `$PSSessionOption`; protect the server via `MaximumReceivedDataSizePerCommandMB` and `MaximumReceivedObjectSizeMB` on `Register-PSSessionConfiguration`. The page's example raises the object size quota in `Microsoft.PowerShell` from 10 MB to 11 MB:
```powershell
Set-PSSessionConfiguration -Name Microsoft.PowerShell -MaximumReceivedObjectSizeMB 11 -Force
```
- Timeout: "The WS-Management service cannot complete the operation within the time specified in OperationTimeout". When both ends set timeouts, the shortest applies. Server settings: MaxTimeoutMs; EnumerationTimeoutMs and MaxPacketRetrievalTimeSeconds under Service. Client: `New-PSSessionOption` parameters CancelTimeout, IdleTimeout, OpenTimeout, OperationTimeout, for example:
```powershell
$pso = New-PSSessionOption -OperationTimeout 240000
New-PSSession -ComputerName Server01 -SessionOption $pso
```
- Group Policy: the Windows Remote Management and Windows Remote Shell objects under Computer Configuration, Administrative Templates, Windows Components.

## Checked
Method: 2026-11-08 docs-only read of the win32 WinRM installation and configuration page (MicrosoftDocs/win32 markdown) and about_Remote_Troubleshooting. Corrected the old default values (they contradicted the page) and dropped the unsupported per-plugin quota path, Restart-Service and 200 MB client default claims. Unchanged: the Set-PSSessionConfiguration and New-PSSessionOption examples come straight from the troubleshooting page.
