---
id: computing-software.systems-network-administration.powershell.splatting
name: splatting
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, splatting, psboundparameters, hashtables, advanced-functions, proxy-functions, psdefaultparametervalues]
level: practitioner
status: verified
description: "Pass parameters with hashtable and array splatting: conditional parameters, forwarding $PSBoundParameters to wrapped cmdlets, and $PSDefaultParameterValues."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_splatting
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_parameters_default_values
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Splatting

Splatting passes a hashtable (named parameters) or array (positional) with `@` instead of `$`.

```powershell
$mail = @{
  To         = 'ops@example.com'
  Subject    = 'Nightly report'
  SmtpServer = '<SMTP_HOST>'
  Port       = 587
  UseSsl     = $true          # switch parameters take $true/$false in a splat
}
Send-Report @mail -Body $body   # Send-Report stands for your own function; splat plus explicit parameters
```

## Build parameters conditionally
```powershell
$p = @{ Path = $HOME; Filter = '*.log' }
if ($Recurse) { $p.Recurse = $true }
if ($Depth)   { $p.Depth = $Depth }
Get-ChildItem @p
```
This replaces the if/else ladder of near-identical calls.

## Forward parameters from a wrapper function
```powershell
function Get-StaleFile {
  [CmdletBinding()]
  param([int]$Days = 90, [string]$Path = '.', [switch]$Recurse)
  $gci = @{} + $PSBoundParameters           # copy; don't mutate the automatic variable
  $gci.Remove('Days') | Out-Null
  $cut = (Get-Date).AddDays(-$Days)
  Get-ChildItem @gci -File | Where-Object LastWriteTime -lt $cut
}
```
- `$PSBoundParameters` holds only parameters the caller actually passed, not defaults. Add
  defaults explicitly if the inner cmdlet needs them.
- Remove keys the inner command does not have, or it throws "A parameter cannot be found".
- Common parameters (`-Verbose`, `-ErrorAction`) are in `$PSBoundParameters` and forward cleanly.

## Array splatting and splatting into externals
```powershell
$gitArgs = '-c', 'user.name=A B', 'config', 'user.name'
& git.exe @gitArgs        # prints "A B": each element becomes one argument, the space is kept inside it
```

## Defaults for a session: $PSDefaultParameterValues
```powershell
$PSDefaultParameterValues['Export-Csv:NoTypeInformation'] = $true
$PSDefaultParameterValues['Get-*:ErrorAction'] = 'SilentlyContinue'   # wildcards allowed in the key
```
Put these in a profile or at the top of a script; they apply to every matching call in scope.

## Gotchas
- `@mail` only works for a variable: `@{...}` inline is a hashtable literal, not a splat.
  PS 7 cannot splat expressions either; assign first.
- An explicit parameter that duplicates a splatted key throws in Windows PowerShell 5.1 ("parameter 'To' is specified more than once").
  Checked on 7.6: the explicit value overrides the splatted one (the 7.1+ change).
- `$PSBoundParameters` and the splat patterns above were run on 5.1 and 7.6 using `Get-ChildItem`; `@{a=1}` written inline is passed as one hashtable argument.

## Verify
- [ ] `Trace-Command ParameterBinding` or `-Verbose` shows the expected parameters bound.
- [ ] The wrapper works with and without every optional parameter.
