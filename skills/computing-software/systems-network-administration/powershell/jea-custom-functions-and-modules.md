---
id: computing-software.systems-network-administration.powershell.jea-custom-functions-and-modules
name: jea-custom-functions-and-modules
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, jea, jea-module, role-capabilities, visiblefunctions, module-packaging]
level: advanced
status: docs-checked
description: "Package custom functions for JEA role capabilities: inline FunctionDefinitions versus a script module, RoleCapabilities layout, language-mode caveats, visibility."
sources:
  - https://learn.microsoft.com/en-us/powershell/scripting/security/remoting/jea/role-capabilities
  - https://learn.microsoft.com/en-us/powershell/scripting/security/remoting/jea/security-considerations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom functions and modules for JEA

Custom functions can simplify complex tasks for end users and add validation logic for cmdlet parameter values, per the role-capabilities page.

## Inline: FunctionDefinitions
```powershell
VisibleFunctions = 'Get-TopProcess'
FunctionDefinitions = @{
    Name        = 'Get-TopProcess'
    ScriptBlock = {
        param($Count = 10)
        Get-Process | Sort-Object -Property CPU -Descending |
            Microsoft.PowerShell.Utility\Select-Object -First $Count
    }
}
```
- A function must also be named in `VisibleFunctions`, or JEA users cannot run it.
- Inside role-capability functions, constrained cmdlets keep their JEA constraints. `Select-Object` is constrained in all JEA sessions and cannot select arbitrary properties, so the example calls it by its fully qualified module name to get the full implementation.

## Module: several functions
With several functions, put them in a PowerShell script module and expose them through `VisibleFunctions` like built-in or third-party module functions. The module holding role capabilities needs a `RoleCapabilities` folder, sits on `$Env:PSModulePath`, and must not be in `$Env:SystemRoot\System32` or a folder untrusted users can modify:
```powershell
$modulePath = Join-Path $Env:ProgramFiles "WindowsPowerShell\Modules\ContosoJEA"
New-Item -ItemType Directory -Path $modulePath
New-Item -ItemType File -Path (Join-Path $modulePath "ContosoJEAFunctions.psm1")
New-ModuleManifest -Path (Join-Path $modulePath "ContosoJEA.psd1") -RootModule "ContosoJEAFunctions.psm1"
New-Item -ItemType Directory (Join-Path $modulePath "RoleCapabilities")
Copy-Item -Path .\MyFirstJEARole.psrc -Destination (Join-Path $modulePath "RoleCapabilities")
```
At least one file in the module folder must have the same name as the folder. (The doc's example module is empty; add your functions to the `.psm1`.)

## Security caveat
The function body runs in the system's default language mode and is not subject to JEA's language constraints. It can reach the file system and registry and run commands not made visible in the role. The role-capabilities page says to avoid running arbitrary code through parameters, and not to pipe user input into `Invoke-Expression`. The security page adds that commands such as `*-Job` can create runspaces without restrictions and that you should not write your own versions of the restricted proxy commands (`Exit-PSSession`, `Get-Command`, `Get-FormatData`, `Get-Help`, `Measure-Object`, `Out-Default`, `Select-Object`).

## Deployment and updates
- New JEA sessions started after a `.psrc` edit reflect the change; restrict who can write to the module folder.
- For many machines, the register-jea page describes a DSC configuration where the File resource copies the module from a read-only file share and the JEA DSC resource defines the endpoint.

## Checked
Method: 2026-11-08 docs-only read of the JEA role-capabilities and security-considerations pages (MicrosoftDocs/PowerShell-Docs markdown) plus register-jea for DSC deployment. Dropped unsupported claims: Pester testing, versioned manifest example, "module changes load only in new sessions", Enter-PSSession verification. Unchanged: the idea of wrapping risky operations in your own functions.
