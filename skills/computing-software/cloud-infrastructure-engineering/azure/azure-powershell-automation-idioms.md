---
id: computing-software.cloud-infrastructure-engineering.azure.azure-powershell-automation-idioms
name: azure-powershell-automation-idioms
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, az-powershell, az-module, connect-azaccount, set-azcontext, azure-powershell, automation-scripts]
level: practitioner
status: docs-checked
description: "Write reliable Az PowerShell automation: non-interactive Connect-AzAccount (MI, SP, OIDC), context per subscription, parallel loops, error handling, paging and module pinning."
sources: ["https://learn.microsoft.com/powershell/azure/authenticate-noninteractive", "https://learn.microsoft.com/powershell/azure/context-persistence", "https://learn.microsoft.com/powershell/azure/install-azps-windows", "https://learn.microsoft.com/powershell/module/az.accounts/connect-azaccount"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure PowerShell automation idioms

**Goal:** scripts that run unattended (pipelines, runbooks, scheduled tasks) across many
subscriptions without prompts, context leaks or silent partial failures.

## Install and pin
```powershell
Install-Module Az -Scope CurrentUser   # pin the version you tested
Import-Module Az.Accounts, Az.Compute, Az.Resources
```
Pin versions in CI; check with `Get-InstalledModule Az`.

## Non-interactive sign-in
```powershell
Connect-AzAccount -Identity                                            # system MI
Connect-AzAccount -Identity -AccountId <uami-client-id>                # user-assigned MI
Connect-AzAccount -ServicePrincipal -Tenant $t -ApplicationId $a -CertificateThumbprint $thumb
Connect-AzAccount -ServicePrincipal -Tenant $t -ApplicationId $a -FederatedToken $env:ID_TOKEN   # OIDC
Disable-AzContextAutosave -Scope Process   # CI: don't persist tokens to the profile
```

## Context per subscription (never rely on the default)
```powershell
$subs = Get-AzSubscription -TenantId $t | ? State -eq 'Enabled'
foreach ($s in $subs) {
  $ctx = Set-AzContext -SubscriptionId $s.Id -Tenant $t
  Get-AzVM -Status -DefaultProfile $ctx | ? PowerState -ne 'VM running' | Select Name, ResourceGroupName
}
```

## Error handling
```powershell
$ErrorActionPreference = 'Stop'
try { Remove-AzResourceGroup -Name $rg -Force -AsJob | Wait-Job | Receive-Job }
catch { Write-Error "Failed $rg : $($_.Exception.Message)"; $failed += $rg }
```
Set `$ErrorActionPreference = 'Stop'` so failures raise terminating errors that `try/catch` can handle.

## Idioms
- `-WhatIf` support on most `New-/Remove-` cmdlets for dry runs.

## Gotchas
- Check the Az and AzureRM coexistence note before installing Az next to AzureRM.

## Verify
- [ ] Script runs in a clean container with only the pinned modules and a managed identity.
- [ ] Failure in one subscription is reported and the exit code is non-zero.

## Checked
2026-10-28. Confirmed on the Connect-AzAccount, non-interactive authentication and context persistence pages: `Connect-AzAccount -Identity`, `-Identity -AccountId` for a user-assigned identity, `-CertificateThumbprint`, `-FederatedToken`, `Set-AzContext`, `-DefaultProfile`, `Disable-AzContextAutosave`, Az and AzureRM coexistence note.
Removed (not confirmed): the Az 14 version pin, pipeline task names, parallel and Search-AzGraph examples, Invoke-AzRestMethod, Get-AzAccessToken SecureString note, Update-AzConfig switches, non-terminating error and tenant-listing claims.

Method: documentation only; no commands were run.
