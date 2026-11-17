---
id: computing-software.cloud-infrastructure-engineering.netdata.windows-msi-install-channels
name: windows-msi-install-channels
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, windows-msi, msiexec, nightly-channel]
level: practitioner
status: docs-checked
description: "Install, switch release channel or uninstall the Netdata Windows MSI silently with msiexec, passing TOKEN and ROOMS to claim, with data-loss gotchas."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/install/windows-release-channels.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Channels: Stable (`https://github.com/netdata/netdata/releases/latest/download/netdata-x64.msi`, major and patch releases) and Nightly (`https://github.com/netdata/netdata-nightlies/releases/latest/download/netdata-x64.msi`, daily builds).

Stable, in elevated PowerShell:

```
$ProgressPreference = 'SilentlyContinue'
Invoke-WebRequest https://github.com/netdata/netdata/releases/latest/download/netdata-x64.msi -OutFile "$env:TEMP\netdata-x64.msi"
msiexec /qn /i "$env:TEMP\netdata-x64.msi" REINSTALL=ALL
```

Use the nightlies URL for Nightly. Claim during install:

```
msiexec /qn /i "$env:TEMP\netdata-x64.msi" TOKEN="$TOKEN" ROOMS="$ROOMS"
```

Uninstall: `msiexec /qn /x netdata-x64.msi`. Check service: `Get-Service netdata | Select-Object Name, Status, DisplayName`.

Gotchas:
- Silent install is not supported on Windows Server earlier than 2019 (TLS issues); use the GUI installer.
- `REINSTALL=ALL` is recommended for channel switches and troubleshooting; normal upgrades work without it.
- Configs, metrics, alert configs and Cloud settings survive a switch; temporary cache and old logs do not.
- Nightly versions carry a `-nightly` suffix.
- The page's "Service Won't Start" fix recursively deletes the Netdata install and ProgramData directories; back up first.
- After a switch that loses the Cloud connection, reinstall with `TOKEN` and `ROOMS`.

## Checked

2026-11-04: channel URLs, the PowerShell install and `REINSTALL=ALL` commands, claiming with `TOKEN` and `ROOMS`, the uninstall and service check commands, the Windows Server 2019 note, preserved and non-preserved data, and the Service Won't Start deletion steps confirmed against the Netdata Windows release channels page.

Method: documentation only; no commands were run.
