---
id: computing-software.systems-network-administration.powershell.errorrecord-and-error-variable
name: errorrecord-and-error-variable
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-error-handling, try-catch, errorrecord, error-variable, errorvariable, get-error, exception, fullyqualifiederrorid]
level: practitioner
status: verified
description: "Read ErrorRecord objects and $Error to find the real cause: exception chain, FullyQualifiedErrorId, InvocationInfo, Get-Error, -ErrorVariable and typed catch blocks."
sources:
  - https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-exceptions
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/get-error
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Inspect ErrorRecord and $Error

Every PowerShell error is a `System.Management.Automation.ErrorRecord` wrapping a .NET exception.

| Member | What it tells you |
|---|---|
| `.Exception` / `.Exception.InnerException` | the .NET exception and its cause chain (often the useful message is inner) |
| `.Exception.GetType().FullName` | the type to put in a typed `catch [...]` |
| `.FullyQualifiedErrorId` | stable ID like `PathNotFound,Microsoft.PowerShell.Commands.GetChildItemCommand` |
| `.CategoryInfo` | category (`ObjectNotFound`, `PermissionDenied`), target, activity |
| `.TargetObject` | the item that failed (path, computer name) |
| `.InvocationInfo.PositionMessage` / `.ScriptStackTrace` | script line and call stack |
| `.ErrorDetails.Message` | server response body, e.g. from `Invoke-RestMethod` |

## Look at the last error
```powershell
$Error[0] | Format-List * -Force               # 5.1
$Error[0].Exception | Format-List * -Force
Get-Error                                       # PS 7: full recursive view of the newest error
Get-Error -Newest 3
```
`$Error` is a session-wide ArrayList, newest first, capped at 256 entries (checked: 300 errors leave 256 on 5.1 and 7.6.7). The `$MaximumErrorCount` variable exists on 5.1 (256) but is not defined on 7.6.7.
`$Error.Clear()` before a test run makes counting easy.

## Catch by type, not by message text
```powershell
try {
  Get-Item -Path $path -ErrorAction Stop
}
catch [System.Management.Automation.ItemNotFoundException] {
  Write-Warning "$path not found"
}
catch [System.UnauthorizedAccessException], [System.Security.SecurityException] {
  throw                                         # rethrow the original record unchanged
}
catch {
  Write-Error -Message "Lookup of $path failed: $($_.Exception.Message)" -ErrorId 'ItemLookup' `
              -Category NotSpecified -TargetObject $path
}
```
- Inside `catch`, `$_` is the ErrorRecord. Save it (`$err = $_`) before running other
  commands that reset `$_`.
- Find the type to catch with `$Error[0].Exception.GetType().FullName`. Cmdlets sometimes
  wrap the exception: check `InnerException` too. `ActionPreferenceStopException` was not seen here:
  `Get-Item ... -ErrorAction Stop` surfaced `ItemNotFoundException` and `Write-Error ... -ErrorAction Stop`
  surfaced `WriteErrorException`, on both 5.1 and 7.6.7. If you meet a wrapper type, fall back to a generic
  catch and read `$_.Exception.InnerException` or `$_.CategoryInfo`.
- `.ErrorDetails.Message` held the JSON body of a GitHub 404 from `Invoke-RestMethod` on both versions
  (exception types differ: `WebException` on 5.1, `HttpResponseException` on 7.6.7).

## Collect errors per command without stopping
```powershell
Get-ChildItem <SHARE_PATH> -Recurse -ErrorAction SilentlyContinue -ErrorVariable +walkErr | Out-Null
$walkErr | Group-Object { $_.CategoryInfo.Reason } | Select-Object Count, Name
$walkErr.TargetObject                           # the paths you could not read
```
`-ErrorVariable name` (no `$`) overwrites; `+name` appends.

## Throwing good errors from your own functions
Use `$PSCmdlet.ThrowTerminatingError($record)` or `$PSCmdlet.WriteError($record)` in advanced
functions so the error points at the caller's line, not inside your module:
```powershell
$ex  = [System.IO.FileNotFoundException]::new("Config not found: $Path")
$rec = [System.Management.Automation.ErrorRecord]::new($ex, 'ConfigMissing', 'ObjectNotFound', $Path)
$PSCmdlet.ThrowTerminatingError($rec)
```

Run on 5.1 and 7.6.7: `FullyQualifiedErrorId` `PathNotFound,Microsoft.PowerShell.Commands.GetChildItemCommand`, `CategoryInfo`, `TargetObject`, bare `throw` rethrowing the original record, `Write-Error -ErrorId` and `ThrowTerminatingError` with an `ErrorRecord` (ID `ConfigMissing,T1`).

## Verify
- [ ] Typed catch blocks fire for the intended exception (test by forcing the failure).
- [ ] Error output includes the target object and a stable ErrorId usable in alerts.
