---
id: computing-software.systems-network-administration.powershell.argument-completers-and-dynamic-parameters
name: argument-completers-and-dynamic-parameters
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, advanced-functions, argument-completer, dynamic-parameters, register-argumentcompleter, argumentcompletions, tab-completion, dynamicparam]
level: advanced
status: verified
description: "Add tab completion with ArgumentCompleter, ArgumentCompletions and Register-ArgumentCompleter, and build dynamicparam blocks only when completion cannot do the job."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_functions_argument_completion
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/register-argumentcompleter
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_functions_advanced_parameters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Argument completers and dynamic parameters

Prefer, in order: `[ValidateSet()]` (static, validated) -> `[ArgumentCompletions()]` (static
suggestions, PS 6+; Windows PowerShell 5.1 ignores it and offers file names instead) -> `[ArgumentCompleter()]` (computed suggestions) -> `dynamicparam`
(parameters that appear conditionally). Dynamic parameters are hard to discover and test.

## Computed completion on a parameter
```powershell
function Restart-AppPool {
  param(
    [Parameter(Mandatory)]
    [ArgumentCompleter({
      param($commandName, $parameterName, $wordToComplete, $commandAst, $fakeBoundParameters)
      Get-IISAppPool | Where-Object Name -like "$wordToComplete*" | ForEach-Object {
        $n = if ($_.Name -match '\s') { "'$($_.Name)'" } else { $_.Name }
        [System.Management.Automation.CompletionResult]::new($n, $_.Name, 'ParameterValue', "$($_.State)")
      }
    })]
    [string]$Name
  )
  Restart-WebAppPool -Name $Name
}
```
- `$fakeBoundParameters` holds already-typed parameters, so completion can depend on them
  (for example list shares only on the `-ComputerName` already given).
- Quote completions that contain spaces yourself.
- Keep completers fast and silent: wrap in `try {} catch {}`; errors break completion invisibly.

## Add completion to commands you do not own
```powershell
Register-ArgumentCompleter -CommandName Get-ADUser, Set-ADUser -ParameterName Server -ScriptBlock {
  param($c, $p, $word)
  (Get-ADDomainController -Filter *).HostName | Where-Object { $_ -like "$word*" }
}
# Native executables:
Register-ArgumentCompleter -Native -CommandName winget -ScriptBlock {
  param($wordToComplete, $commandAst, $cursorPosition)
  winget complete --word $wordToComplete --commandline "$commandAst" --position $cursorPosition
}
```
Put these in the profile or module's `.psm1`.

## Dynamic parameters (only when the parameter itself must vary)
```powershell
function Get-LogTail {
  [CmdletBinding()]
  param([Parameter(Mandatory)][string]$LogName)
  dynamicparam {
    $dict = [System.Management.Automation.RuntimeDefinedParameterDictionary]::new()
    if ($LogName -eq 'Security') {
      $attrs = [System.Collections.ObjectModel.Collection[System.Attribute]]::new()
      $attrs.Add([System.Management.Automation.ParameterAttribute]@{ Mandatory = $false })
      $attrs.Add([System.Management.Automation.ValidateSetAttribute]::new('4624','4625','4740'))
      $dict.Add('EventId', [System.Management.Automation.RuntimeDefinedParameter]::new('EventId', [string], $attrs))
    }
    $dict
  }
  end {
    $id = $PSBoundParameters['EventId']      # dynamic params are not variables
    Get-WinEvent -LogName $LogName -MaxEvents 50 | Where-Object { -not $id -or $_.Id -eq $id }
  }
}
```
- With `dynamicparam` you must use named blocks (`begin/process/end`).
- Read values from `$PSBoundParameters`; no `$EventId` variable is created.
- Static parameters that the `dynamicparam` block reads must be bound from the command line; a value arriving by
  pipeline is not available yet when the block runs (piping `LogName` and passing `-EventId` failed).

## Verify
- [ ] `$c = 'Restart-AppPool -Name '; (TabExpansion2 $c $c.Length).CompletionMatches` returns the expected matches
      (the cursor position must not exceed the string length: 24 on this 22-character string throws).
- [ ] `Get-Command Get-LogTail -ArgumentList Security` lists `EventId` in its parameters.

## Checked
Ran on PowerShell 7.6.7 and Windows PowerShell 5.1: the ArgumentCompleter function with a stub `Get-IISAppPool`
(TabExpansion2 gave `'Default AppPool'` quoted, `api`, with the State as tooltip), the dynamicparam function
(`EventId` appears only with `-LogName Security`, ValidateSet rejects `1`, `$PSBoundParameters['EventId']` works, no
`$EventId` variable, `Get-Command ... -ArgumentList Security` lists it), `[ArgumentCompletions()]` (works in 7, ignored in
5.1), `Register-ArgumentCompleter` on an inbox command and with `-Native` (3-parameter block), and the 24-versus-22 cursor
error. IIS, ActiveDirectory and winget names (`Get-IISAppPool`, `Restart-WebAppPool`, `Get-ADUser -Server`,
`Get-ADDomainController -Filter`, `winget complete --word --commandline --position`) were confirmed on their Microsoft
Learn pages; those modules and winget are not installed here, so the calls themselves were stubbed.
