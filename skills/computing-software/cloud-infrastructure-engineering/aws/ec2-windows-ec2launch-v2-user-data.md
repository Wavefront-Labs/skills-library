---
id: computing-software.cloud-infrastructure-engineering.aws.ec2-windows-ec2launch-v2-user-data
name: ec2-windows-ec2launch-v2-user-data
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, ec2, windows, ec2launch, windows-user-data, sysprep, powershell, ami]
level: practitioner
status: docs-checked
description: "Bootstrap Windows EC2 with EC2Launch v2: YAML and PowerShell user data, persist and frequency, agent-config.yml tasks, logs, and Sysprep when creating custom Windows AMIs."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2launch-v2.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2launch-v2-settings.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2launch-v2-task-definitions.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/sysprep-using-ec2launchv2.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2launchv2-troubleshooting.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows EC2: EC2Launch v2 user data and Sysprep

EC2Launch v2 is the launch agent on current Windows Server AMIs (replacing EC2Config and
EC2Launch v1). Config: `%ProgramData%\Amazon\EC2Launch\config\agent-config.yml`.

## 1. User data formats
Classic script blocks:
```powershell
<powershell>
$ErrorActionPreference = 'Stop'
Install-WindowsFeature Web-Server -IncludeManagementTools
Rename-Computer -NewName "web-$((Invoke-RestMethod http://169.254.169.254/latest/meta-data/instance-id -Headers @{'X-aws-ec2-metadata-token'=(Invoke-RestMethod -Method Put http://169.254.169.254/latest/api/token -Headers @{'X-aws-ec2-metadata-token-ttl-seconds'='60'})}).Substring(2,8))" -Restart
</powershell>
<persist>false</persist>
```
- `<persist>true</persist>` runs user data on every reboot or start (default: once, at launch).
- `<script>` for cmd, `<powershell>` for PowerShell; `<powershellArguments>` for flags;
  `<detach>true</detach>` (EC2Launch v2 only) runs the script as a detached process. If both batch and PowerShell blocks exist, the batch script runs first.

YAML format (v2 native) with ordered tasks:
```yaml
version: 1.1
tasks:
- task: executeScript
  inputs:
  - frequency: once
    type: powershell
    runAs: localSystem
    content: |-
      New-Item -Path "$env:SystemDrive\bootstrap.txt" -ItemType File
```
`frequency` is `once` or `always` (every boot); `runAs` is `admin` or `localSystem`; `type` is `batch` or `powershell`.
Scripts run one at a time by default (`detach: false`); with `detach: true` script exit codes (including 3010) have no effect. If user data restarts the computer or is
interrupted, its run state stays pending and it runs again at the next boot, so make it idempotent.

## 2. Logs and rerun
- `%ProgramData%\Amazon\EC2Launch\log\agent.log` (rotated at 1 MB) and `telemetry.log`.
- Script output files (`UserScript.ps1`, `Output.tmp`, `Err.tmp`) go to a folder `%LocalAppData%\Temp\EC2Launch<digits>`; the exact path is written to `agent.log`.
- `& "$env:ProgramFiles\Amazon\EC2Launch\EC2Launch.exe" reset` (optionally `-c` to clean logs) deletes the agent state so the agent starts fresh the next time it runs; `EC2Launch.exe status` reports the agent state through its exit code; `validate` checks `agent-config.yml`.

## 3. Sysprep for custom AMIs
Before creating an AMI from a configured instance that will be cloned (domain joins, unique
SIDs):
```powershell
& "$env:ProgramFiles\Amazon\EC2Launch\EC2Launch.exe" sysprep --shutdown=true
```
This resets the agent state, disables RDP until it is re-enabled, runs Windows Sysprep (the generalize phase removes the computer name and SID, and removes the machine from its domain), and shuts the instance down; then create the image. The Administrator password is scrambled unless you configure the `setAdminAccount` task. The `-s`/`--shutdown` flag shuts the instance down after Sysprep.

## Gotchas
- Sysprep's generalize phase is what removes the SID and domain membership; images made without it carry the source machine's identity.
- Set the ASG health-check grace period long enough for first-boot tasks to finish.
- For PowerShell scripts EC2Launch v2 passes `-ExecutionPolicy Unrestricted` by default when no arguments are given.

## Verify
- [ ] `agent.log` shows user data executed with exit code 0 on a fresh launch.
- [ ] Instances from the custom AMI have unique SIDs (`whoami /user`) and new admin passwords.
- [ ] Persisted scripts run on reboot only when intended.

## Checked

Checked 2026-10-27 against the Amazon EC2 User Guide (EC2Launch v2 overview, settings and CLI commands, task definitions, troubleshooting, Sysprep with EC2Launch v2, user data for Windows instances).
- `<persist>`, `<script>`, `<powershell>`, `<powershellArguments>` and `<detach>` behaviour, and the run-again-if-interrupted rule for EC2Launch v2, confirmed.
- `executeScript` inputs (`frequency`, `type`, `runAs`, `content`, `detach`), YAML `version: 1.1`, the 3010 note, log locations and script output folder confirmed.
- `ec2launch sysprep --shutdown=true`, `reset`, `status` and `validate` and what Sysprep does (RDP disabled, generalize removes name and SID, Administrator password scrambled unless `setAdminAccount`) confirmed. The `agent-config.yml` path is confirmed on the validate command entry.
- Removed the `err.log` file name, the "exit 3010 to reboot and continue" claim and the Image Builder remark, which the pages read do not support. The sources entry for Sysprep now points to the live page `sysprep-using-ec2launchv2.html`.

Method: documentation only; no commands were run.
