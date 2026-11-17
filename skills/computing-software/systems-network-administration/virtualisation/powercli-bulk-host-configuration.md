---
id: computing-software.systems-network-administration.virtualisation.powercli-bulk-host-configuration
name: powercli-bulk-host-configuration
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [powercli, powercli-host-config, get-vmhost, get-esxcli, advanced-settings, ntp, idempotent-scripts, vmware, esxi, vsphere, powershell]
level: practitioner
status: draft
description: "Configure many ESXi hosts consistently with PowerCLI: Get-VMHost pipelines, advanced settings, NTP/syslog/services, Get-EsxCli -V2, WhatIf runs and idempotent scripts."
sources:
  - https://developer.broadcom.com/powercli
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bulk ESXi host configuration with PowerCLI

**Goal:** apply the same settings to every host in a cluster in one idempotent script,
and prove the result.

## Pattern: desired state table
```powershell
$desired = @{
  'Syslog.global.logHost'          = 'ssl://siem.<domain>:1514'
  'UserVars.ESXiShellTimeOut'      = 900
  'Security.AccountLockFailures'   = 5
  'Config.HostAgent.plugins.solo.enableMob' = $false
}
$hosts = Get-Cluster Prod | Get-VMHost
foreach ($h in $hosts) {
  foreach ($k in $desired.Keys) {
    $s = Get-AdvancedSetting -Entity $h -Name $k
    if ($s.Value -ne $desired[$k]) {
      $s | Set-AdvancedSetting -Value $desired[$k] -Confirm:$false -WhatIf:$WhatIfPreference
    }
  }
}
```
Run with `$WhatIfPreference = $true` first; only changes are applied, so reruns are safe.

## Services, NTP, DNS
```powershell
$hosts | Get-VMHostService | Where Key -eq 'TSM-SSH' | Stop-VMHostService -Confirm:$false
$hosts | Get-VMHostService | Where Key -eq 'TSM-SSH' | Set-VMHostService -Policy Off
$hosts | Add-VMHostNtpServer -NtpServer ntp1.<domain>,ntp2.<domain> -ErrorAction SilentlyContinue
$hosts | Get-VMHostService | Where Key -eq 'ntpd' | Set-VMHostService -Policy On -PassThru | Restart-VMHostService -Confirm:$false
$hosts | Get-VMHostNetwork | Set-VMHostNetwork -DnsAddress 10.0.0.10,10.0.0.11 -SearchDomain <domain>
```

## When cmdlets don't exist: Get-EsxCli -V2
```powershell
$esxcli = Get-EsxCli -VMHost $h -V2
$args = $esxcli.system.syslog.config.set.CreateArgs()
$args.loghost = 'ssl://siem.<domain>:1514'
$esxcli.system.syslog.config.set.Invoke($args)
$esxcli.storage.nmp.device.list.Invoke() | Select Device, PathSelectionPolicy
```

## Discipline
- Host profiles or vLCM are the long-term enforcement; scripts are for bulk changes and
  checks between profile runs.
- Log every change (`Start-Transcript`), and commit scripts to Git with reviews.
- Run against one host first (`$hosts = Get-VMHost esx01`).

## Verify
A companion check script prints host, setting, actual, desired and reports zero drift
after the run.
