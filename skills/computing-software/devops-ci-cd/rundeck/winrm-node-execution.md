---
id: computing-software.devops-ci-cd.rundeck.winrm-node-execution
name: winrm-node-execution
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, winrm, windows-nodes, password-storage-path, powershell-remoting]
level: advanced
status: docs-checked
description: "Run Rundeck commands on Windows nodes with the WinRM Node Executor Python and File Copier plugins: auth modes, node attributes, password storage and WinRM setup."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/manual/projects/node-execution/powershell.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The two plugins, WinRM Node Executor Python and WinRM File Copier, only work when Runbook Automation (or an Enterprise Runner) is installed on Windows. Select both as the project's default Node Executor and File Copier.

Auth: in a trusted domain only `username` is needed and the account running the Rundeck process is used. Otherwise supply username and password.

Node attributes: `hostname`, `username`, `password-storage-path` (starts with `keys/`), `connectionUri` (for example `https://hostname:port`), `output-charset` (default `utf-8`).

Project-level Password Storage Path can reference context data:

```
keys/nodes/${node.name}.password
```

Credentials at run time need job options named `username` and `winrmpassword` (use the Secure input type).

Server setup:

```
winrm quickconfig
winrm set winrm/config/client @{TrustedHosts="*"}
```

Remote node setup:

```
winrm quickconfig
winrm set winrm/config/service/Auth @{Basic="true"}
winrm set winrm/config/service @{AllowUnencrypted="true"}
winrm set winrm/config/winrs @{MaxMemoryPerShellMB="1024"}
```

PowerShell: `Set-ExecutionPolicy RemoteSigned`; grant a user access with `Set-PSSessionConfiguration -ShowSecurityDescriptorUI -Name Microsoft.PowerShell`.

Security gotcha: `TrustedHosts="*"`, Basic auth and AllowUnencrypted are broad and unencrypted; tighten them on production networks.

## Checked

2026-11-04: plugins, auth modes, node attributes, credentials job options, project path example and WinRM/PowerShell setup commands confirmed against the WinRM Node Execution page. Removed the unsourced Verify line.
Method: documentation only; no commands were run.
