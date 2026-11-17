---
id: computing-software.it-support-helpdesk.remote-support-tools.rmm-scripting-and-components
name: rmm-scripting-and-components
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, rmm-scripting, rmm, script-components, system-context, exit-codes, automation-policies]
level: practitioner
status: draft
description: "Write scripts that behave inside RMM agents: SYSTEM context, no UI, exit codes and output the RMM reads, variables/parameters, timeouts, idempotence, and safe rollout."
sources:
  - "https://rmm.datto.com/help/en/Content/4WEBPORTAL/Components/Components.htm"
  - "https://www.connectwise.com/platform/rmm"
  - "https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-exceptions"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# rmm-scripting-and-components

RMM tools (Datto RMM components, NinjaOne scripts, ConnectWise Automate/RMM, N-able,
Kaseya agent procedures) run scripts through their agent. The agent's environment is
not your interactive admin session, which trips up most first scripts.

## The execution environment
- Runs as **SYSTEM** (Windows) or root (macOS/Linux) by default: no mapped drives, no
  user HKCU, `$env:USERPROFILE` is the system profile, no network credentials to shares
  (computer account only).
- **No interactive UI**: message boxes or prompts hang until timeout.
- 32-bit agent on 64-bit Windows in some products: `%SystemRoot%\System32` redirects to
  SysWOW64; call `%SystemRoot%\Sysnative\WindowsPowerShell\v1.0\powershell.exe` or check
  `[Environment]::Is64BitProcess`.
- Timeout per script (often 5-30 min) and output size limits.

## What the RMM reads
- **Exit code**: 0 = success, non-zero = failure (alerting/ticketing keys off this).
- **stdout/stderr**: stored in the job result; keep it short and parseable.
- Monitor-type components often need specific markers, e.g. Datto RMM monitors write
  `<-Start Result->` / `<-End Result->` blocks and exit 1 to alert.
- Variables: site/global variables and component input variables arrive as environment
  variables (`$env:usrVariable` style names vary per product).

## Template (PowerShell)
```powershell
$ErrorActionPreference = 'Stop'
try {
    $svc = Get-Service -Name 'Spooler'
    if ($svc.Status -ne 'Running') { Start-Service 'Spooler'; Write-Output 'Spooler started' }
    else { Write-Output 'Spooler already running' }
    exit 0
} catch {
    Write-Output "FAILED: $($_.Exception.Message)"
    exit 1
}
```
Idempotent (safe to run twice), explicit exit codes, one-line results.

## Running as the logged-on user
Needed for per-user settings: use the RMM's "run as logged-in user" option if present, or
create a scheduled task for the interactive user (`New-ScheduledTaskPrincipal -GroupId
"BUILTIN\Users"`) and trigger it; or edit HKU hives by loading each profile's
`NTUSER.DAT`.

## Rollout
Test on one device -> a pilot site -> all. Scope by device filter/policy, not "All
devices". Keep scripts in a version-controlled repo with change history; the RMM library
is not a source of truth.

## Gotchas
- Credentials in script bodies end up in job logs and RMM databases; use the RMM's secure
  variables.
- `Write-Host` output may not be captured in older PowerShell hosts; use `Write-Output`.
- Reboots inside scripts cut off result reporting; schedule them separately.

## Verify
Job result shows exit 0 with the expected one-line output on a pilot device; a second run
reports the "already done" path; failures raise the intended alert.
