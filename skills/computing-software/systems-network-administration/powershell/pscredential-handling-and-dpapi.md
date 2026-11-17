---
id: computing-software.systems-network-administration.powershell.pscredential-handling-and-dpapi
name: pscredential-handling-and-dpapi
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-security, pscredential, export-clixml-credentials]
level: practitioner
status: docs-checked
description: "Handle credentials in scripts safely: PSCredential parameters, Export-Clixml DPAPI scope limits, avoiding plain text and ConvertFrom-SecureString keys."
sources:
  - https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/add-credentials-to-powershell-functions
  - https://learn.microsoft.com/en-us/dotnet/api/system.security.securestring
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/export-clixml
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/convertfrom-securestring
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PSCredential handling and DPAPI

## Accept credentials properly
```powershell
function Invoke-Thing {
  [CmdletBinding()]
  param(
    [Parameter()]
    [System.Management.Automation.PSCredential]
    [System.Management.Automation.Credential()]
    $Credential = [System.Management.Automation.PSCredential]::Empty
  )
  $p = @{}; if ($Credential -ne [pscredential]::Empty) { $p.Credential = $Credential }
  Get-CimInstance Win32_OperatingSystem -ComputerName SRV01 @p
}
```
`[System.Management.Automation.Credential()]` lets callers pass a user name string and get a password prompt; the
`PSCredential::Empty` default avoids passing a null credential to cmdlets. Some legacy cmdlets do not accept `Empty`
(see the cited article's legacy section). Do not take passwords as plain `[string]` parameters.

## Storing for unattended scripts
```powershell
Get-Credential | Export-Clixml -Path "$env:LOCALAPPDATA\creds\svc-app.xml"
$cred = Import-Clixml "$env:LOCALAPPDATA\creds\svc-app.xml"
```
`Export-Clixml` encrypts credential objects with the Windows Data Protection API (DPAPI): only your user account on
that computer can decrypt the file, and it cannot be used on a different computer or by a different user. Create the
file while running as the account that will read it. On Linux and macOS, `Export-Clixml` does **not** encrypt: the
password is stored as a Unicode character array, which is obfuscation only.

## ConvertFrom-SecureString -Key (portable, weaker)
Without a key, `ConvertFrom-SecureString` uses DPAPI. With `-Key` (or `-SecureKey`) it uses AES, and the key must be
128, 192 or 256 bits (16, 24 or 32 bytes). Anyone holding the key can decrypt, so the key becomes the secret to protect.
For vault-backed storage see the secretmanagement-and-secretstore skill.

## Leaks to avoid
- `$cred.GetNetworkCredential().Password` returns the plain-text password; keep it out of logs and transcripts.
- `ConvertTo-SecureString -AsPlainText -Force` with a literal password: PowerShell requires both switches because the
  plain-text password gets recorded in various logs. Do not commit such scripts; in CI/CD, take the value from the
  tool's secret variable at run time.
- On non-Windows, SecureString does not encrypt its internal storage, and on all platforms the value is converted to
  plain text whenever it is used.

## Verify
- [ ] No plain-text passwords in repos; unattended scripts read DPAPI-bound files created by the same account, or a
      vault.

## Checked
2026-11-09. Read the Learn articles on credentials in functions, Export-Clixml, ConvertFrom-SecureString and the
.NET SecureString API page. Confirmed the Credential attribute and Empty default, DPAPI scope, non-Windows behaviour,
AES key lengths, AsPlainText/Force warning, GetNetworkCredential. Removed as unconfirmed: PSScriptAnalyzer rule name,
runas and scheduled-task creation tips, gMSA, managed identity and vault product lists, event 4688 remark.
Method: documentation only; no commands were run.
