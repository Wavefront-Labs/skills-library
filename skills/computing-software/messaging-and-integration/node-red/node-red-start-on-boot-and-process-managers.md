---
id: computing-software.messaging-and-integration.node-red.node-red-start-on-boot-and-process-managers
name: node-red-start-on-boot-and-process-managers
category: computing-software
field: messaging-and-integration
product: node-red
tags: [node-red, systemd, pm2, autostart, boot, nssm, raspberry-pi, linux-installers]
level: practitioner
status: docs-checked
description: "Start Node-RED at boot with the Pi/Debian install script systemd service, the RPM installer, or PM2 with pm2 save and pm2 startup, plus the Windows NSSM alternative."
sources: ["https://nodered.org/docs/faq/starting-node-red-on-boot"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Starting Node-RED on boot

Raspberry Pi, Debian, Ubuntu: the official Raspberry Pi install script works on any Debian-like system and installs Node-RED as a systemd service. If you are not using Raspberry Pi OS you may need to edit the service file for your user id and environment. An install script for RPM based Linux (RedHat, Fedora, CentOS) also sets up systemd.

Other Linux and OS X: use PM2.
1. `sudo npm install -g pm2` (an Administrator shell without `sudo` on Windows).
2. Find the node-red command: a global install is probably `/usr/bin/node-red` or `/usr/local/bin/node-red` (`which node-red` confirms); a local install is `node_modules/node-red/bin/node-red`.
3. `pm2 start /usr/bin/node-red -- -v`. The `--` must come before arguments for Node-RED. On memory-constrained devices such as a Raspberry Pi or BeagleBone Black add `--node-args="--max-old-space-size=128"`. To run as root you must pass `--userDir` to say where Node-RED stores data.
4. `pm2 info node-red` and `pm2 logs node-red` show status and log output.
5. `pm2 save` then `pm2 startup` (or `pm2 startup systemd` on newer systemd Linux) and follow the instructions it prints.
6. Reboot and check everything starts.

PM2 does not autorun as a service on Windows; the page points to a community example using NSSM. It also lists community alternatives: systemd and init.d scripts, a launchd script for OS X.

## Checked

2026-11-04. Confirmed against the Node-RED FAQ page Starting Node-RED on boot. Removed: the node-red-log remark (belongs to the logging page) and the vague 'extra memory option' wording, now the page's exact flag.

Method: documentation only; no commands were run.
