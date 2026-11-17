---
id: computing-software.systems-network-administration.healthchecks.powershell-ping
name: powershell-ping
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, powershell, task-scheduler, invoke-restmethod, windows]
level: intro
status: docs-checked
description: "Monitor Windows scheduled tasks with Healthchecks by sending pings from PowerShell using Invoke-RestMethod, inline or from a .ps1 script."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/powershell.md
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/resources.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
PowerShell scripts run by Windows Task Scheduler can ping Healthchecks.

Script file (save with a `.ps1` extension, for example `healthchecks.ps1`):

```
Invoke-RestMethod <ping-url>
```

Command to run it from Task Scheduler:

```
powershell.exe -ExecutionPolicy bypass -File /path/to/healthchecks.ps1
```

Extend the script with the real work; when Task Scheduler runs it regularly, each ping is an "I'm alive" message.

Diagnostics in a POST body:

```
Invoke-RestMethod -Uri <ping-url> -Method Post -Body "temperature=-7"
```

Inline without a file, using PowerShell's `-Command` argument:

```
powershell.exe -Command "&{Invoke-RestMethod <ping-url>}"
```

Other `Invoke-RestMethod` parameters are in Microsoft's documentation.

Community modules listed on the Healthchecks resources page: HealthChecksIOStatusReport (pinging) and healthchecks-pwsh (pinging and all Management API calls).

## Checked

2026-11-04: confirmed against the PowerShell page (script, Task Scheduler command, POST body, -Command form) and the Third-Party Resources page (the two modules).
Method: documentation only; no commands were run.
