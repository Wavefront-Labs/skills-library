---
id: computing-software.systems-network-administration.powershell.native-command-errors-and-lastexitcode
name: native-command-errors-and-lastexitcode
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-error-handling, lastexitcode, native-command-errors, psnativecommanduseerroractionpreference]
level: practitioner
status: verified
description: "Handle exit codes from native executables in PowerShell: $LASTEXITCODE, $?, stderr behaviour in 5.1 vs 7, and PSNativeCommandUseErrorActionPreference."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_automatic_variables
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Native command errors and $LASTEXITCODE

try/catch does not catch a failing `robocopy`, `git` or `msiexec`: native commands signal failure through exit codes.

## Check exit codes
```powershell
& msiexec.exe /i app.msi /qn /l*v install.log
if ($LASTEXITCODE -notin 0,3010) { throw "msiexec failed with $LASTEXITCODE" }
```
- `$LASTEXITCODE` = exit code of the last native program.
- `$?` = success of the last command: `cmd /c "exit 3"` left `$?` False and `$LASTEXITCODE` 3; a native writing to stderr but
  exiting 0 left `$?` True in both editions, but in 5.1 `$?` became False once that stderr was redirected with `2>&1`.
- Know each tool's codes: robocopy 0-7 are success variants (8 and above = at least one failure, per the robocopy docs;
  a copy returned 1 and a missing source 16 here), msiexec 3010 = ERROR_SUCCESS_REBOOT_REQUIRED ("indicates success" per the Windows
  Installer error-code list).

## Wait for GUI/async executables
`Start-Process -Wait -PassThru` gives `.ExitCode` (7 for `cmd /c exit 7`); the call operator `&` waited for a console app (1 s `ping`)
but returned after about 8 ms for a GUI app (`charmap.exe`, closed afterwards).
```powershell
$p = Start-Process setup.exe -ArgumentList '/quiet' -Wait -PassThru
$p.ExitCode
```

## stderr
- Windows PowerShell 5.1: redirecting stderr (`2>&1`) wraps lines as ErrorRecords and with `$ErrorActionPreference =
  'Stop'` can terminate on harmless warnings written to stderr (git, curl).
- PowerShell 7.6.7: redirected stderr lines are still `ErrorRecord` objects (`$e = cmd /c "echo e 1>&2" 2>&1; $e.GetType()`), but
  they no longer set `$?` to false and `$ErrorActionPreference = 'Stop'` did not terminate on them.

## Make natives honour ErrorActionPreference (experimental in 7.3, no flag needed in 7.6.7)
```powershell
$PSNativeCommandUseErrorActionPreference = $true
$ErrorActionPreference = 'Stop'
cmd /c "exit 5"   # raised: NativeCommandExitException: Program "cmd.exe" ended with non-zero exit code: 5 (0x00000005).
```
The variable defaults to `$false` (`$PSNativeCommandUseErrorActionPreference` printed False). It first appeared as the experimental
feature `PSNativeCommandErrorActionPreference` (7.3 changelog) and is absent from the 7.4 experimental-feature table, i.e. mainstream by 7.4.
Windows PowerShell 5.1 has no such variable.
Opt out per call for tools with non-zero success codes (robocopy) by temporarily setting it to `$false`.

## Arguments
Quote and pass arrays to avoid parsing surprises: `& $exe @('--path', $path)`. 7.3 made native argument passing stable
(`$PSNativeCommandArgumentPassing`, `Windows` mode in 7.6.7); empty strings and embedded quotes now pass correctly: a Python
printing `sys.argv` showed `['', 'a"b', 'c d']` in 7.6.7 but `['ab c', 'd']` in 5.1 for the arguments `''`, `'a"b'`, `'c d'`.

## Verify
- [ ] Scripts check exit codes for every native call; CI fails when a native tool fails.

## Checked
Ran on PowerShell 7.6.7 and Windows PowerShell 5.1.26100: exit code and `$?` for `cmd /c` with and without stderr and with `2>&1`,
`$ErrorActionPreference = 'Stop'` with redirected stderr (7: survived; 5.1: RemoteException), `PSNativeCommandUseErrorActionPreference`
(NativeCommandExitException text), `Start-Process -Wait -PassThru`, `&` with a console and a GUI executable, robocopy exit codes
(1 and 16), the type of redirected stderr, and argument passing through a Python `sys.argv` probe. The robocopy "8 or greater" rule and
msiexec 3010 were read on Microsoft Learn; the experimental-feature history is from the 7.3/7.4 changelogs and the experimental
features table in the PowerShell docs. `msiexec` itself was not run.
The `msiexec` switches in the first example (`/i`, `/qn`, `/l*v`) were checked against the msiexec page on Microsoft Learn.
