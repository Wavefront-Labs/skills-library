---
id: computing-software.systems-network-administration.powershell.scheduled-jobs-psscheduledjob
name: scheduled-jobs-psscheduledjob
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-jobs, register-scheduledjob, scheduled-tasks, psscheduledjob]
level: practitioner
status: docs-checked
description: "Use PSScheduledJob: Register-ScheduledJob with triggers and options, read saved results with Get-Job and Receive-Job, and where definitions and output are stored."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/psscheduledjob/about/about_scheduled_jobs
  - https://learn.microsoft.com/en-us/powershell/module/psscheduledjob/register-scheduledjob
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scheduled jobs (PSScheduledJob)

A scheduled job is a hybrid of a PowerShell background job and a Task Scheduler task: it is saved to disk,
registered in Task Scheduler, and each run creates a job instance whose results are also saved to disk. The
PSScheduledJob module was introduced in PowerShell 3.0. The pages checked are the Windows PowerShell 5.1 docs.

## Register
```powershell
$O = New-ScheduledJobOption -WakeToRun -StartIfIdle -MultipleInstancePolicy Queue
$T = New-JobTrigger -Weekly -At "9:00 PM" -DaysOfWeek Monday -WeeksInterval 2
Register-ScheduledJob -Name UpdateVersion -FilePath <script.ps1> -ScheduledJobOption $O -Trigger $T
```
- Every call needs `-ScriptBlock` or `-FilePath`, and a unique `-Name`.
- Triggers are optional. With none, the job never starts by itself: add one with `Add-JobTrigger`, use `-RunNow`,
  or `Start-Job -DefinitionName <name>`.
- `-Trigger` and `-ScheduledJobOption` also accept hashtables (for example `Frequency`, `At`, `DaysOfWeek`, `Interval`;
  `WakeToRun`, `StartIfNotIdle`, `MultipleInstancePolicy`).
- Option defaults when given as a hashtable include `RunElevated=$false`, `RunWithoutNetwork=$false`,
  `StartIfOnBattery=$false` and `MultipleInstancePolicy="IgnoreNew"`. The page says to review options carefully
  because they can prevent the job running.
- `-Credential` sets the account (default: current user). `-InitializationScript` runs before the job; an error in it,
  even non-terminating, fails that instance. `-RunAs32`, `-RunEvery <TimeSpan>` and `-ArgumentList` also exist.
- `-Authentication CredSSP` is shown for remote work, with a caution that CredSSP increases the security risk
  if the remote computer is compromised.

## Results
```powershell
Import-Module PSScheduledJob   # Get-Job sees scheduled job instances only when the module is imported
Get-Job -Name UpdateVersion
Receive-Job -Id <id>
```
- Scheduled job cmdlets manage the definition; the job cmdlets (`Get-Job`, `Receive-Job`) manage instances.
- Results stay on disk until deleted or until `-MaxResultCount` (default 32) is exceeded, then the oldest is dropped.
  They are available again in a new session. `Set-ScheduledJob -ClearExecutionHistory` clears them.
- Definitions (XML) are under `$HOME\AppData\Local\Microsoft\Windows\PowerShell\ScheduledJobs`, one directory per job;
  results under `<JobName>\Output\<Timestamp>`. Triggers and options are saved inside each job's XML.
- A job started with `Start-Job -DefinitionName` is a plain background job: it ignores triggers and options and its
  output is not saved in the scheduled job directory.

## Manage
```powershell
Get-ScheduledJob; Get-JobTrigger -Name <name>
Get-ScheduledJob -Name <name> | Set-ScheduledJobOption -ContinueIfGoingOnBattery -PassThru
Unregister-ScheduledJob <name>      # also deletes all saved results
```
Jobs are visible and manageable in Task Scheduler, but the PowerShell job cmdlets only work on jobs created in PowerShell.

## Remote registration
The page shows `Invoke-Command` running `Register-ScheduledJob` on many computers with `$Using:` variables for
the trigger and options.

## Checked
Method: 2026-11-08, read both cited learn.microsoft.com pages in full from the 5.1 markdown sources (about page in full; the cmdlet page through its parameter list up to ScriptBlock, with syntax, examples, Authentication, Credential, MaxResultCount, ScheduledJobOption and RunNow read). Rewritten to what they state. Removed unsupported claims from the earlier draft: "not in PowerShell 7", the Task Scheduler folder path, `-RequireNetwork`, and the advice on when to use ScheduledTasks instead. Not executed.
