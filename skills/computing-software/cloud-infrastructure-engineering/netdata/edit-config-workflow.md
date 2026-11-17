---
id: computing-software.cloud-infrastructure-engineering.netdata.edit-config-workflow
name: edit-config-workflow
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, edit-config, netdata-conf, config-directory]
level: intro
status: docs-checked
description: "Change Netdata Agent settings with the edit-config script from the config directory, then restart the Agent so the change applies."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/netdata-agent/configuration/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use the `edit-config` script in the Agent's config directory for configuration changes.

```
cd /etc/netdata 2>/dev/null || cd /opt/netdata/etc/netdata
sudo ./edit-config netdata.conf
```

Config directories: `/etc/netdata/` on Linux, `/opt/netdata/etc/netdata/` on some operating systems, the `etc\netdata` folder under the Netdata install directory (Program Files) on Windows.

Steps:
1. `cd` into the config directory (the docs assume scripts run from inside it).
2. Run `sudo ./edit-config <file>`, edit and save.
3. Restart the Agent for your platform (see the start-stop-restart skills).

Gotchas:
- A fresh `netdata.conf` contains only comments; the Agent runs on built-in defaults, so change only what you need to override.
- Not sure of the directory? Open `http://NODE:19999/netdata.conf` and read the `# config directory =` value.
- On Windows run `edit-config` from the bundled MSYS2 shell with Administrator rights, because the Program Files Netdata directory is protected.

The running configuration can be downloaded from `http://agent-ip:19999/netdata.conf`. Configuration can also be changed on the fly through Netdata Cloud's Dynamic Configuration Manager.

## Checked

2026-11-04: edit-config usage, config directory locations, comment-only netdata.conf, the netdata.conf URL, the Windows MSYS2 and Administrator note, and the Dynamic Configuration pointer confirmed against the Netdata Agent Configuration page. Replaced the placeholder drive letter with the page's C: path and removed the unsourced verify step.

Method: documentation only; no commands were run.
