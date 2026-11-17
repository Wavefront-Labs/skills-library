---
id: computing-software.cloud-infrastructure-engineering.netdata.start-stop-restart-windows-macos
name: start-stop-restart-windows-macos
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, windows-service, homebrew, brew-services]
level: intro
status: docs-checked
description: "Manage the Netdata Agent service on Windows with PowerShell and on macOS with Homebrew services, including the Homebrew no-autostart caveat."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/netdata-agent/start-stop-restart.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Windows (run PowerShell as Administrator):

```
Get-Service Netdata
Start-Service Netdata
Stop-Service Netdata
Restart-Service Netdata
```

You can also start, stop and restart the `Netdata` service from the Services tab in Task Manager.

macOS with Homebrew:

```
brew services start netdata
brew services stop netdata
brew services restart netdata
brew services info netdata
```

Gotchas:
- Unlike other install methods, a Homebrew install does not start after `brew install` or at boot. Run `brew services start netdata`, which also registers it to launch at login.
- `brew services stop` also unregisters it from launching at login or boot.

Verify:

```
curl http://localhost:19999/api/v1/info
```

or open `http://localhost:19999` in a browser.

## Checked

2026-11-04: the PowerShell service commands, Administrator requirement, Task Manager Services tab, `brew services` commands, the Homebrew no-autostart behaviour and the status check confirmed against the Netdata Service Control page.

Method: documentation only; no commands were run.
