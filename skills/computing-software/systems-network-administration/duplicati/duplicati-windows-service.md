---
id: computing-software.systems-network-administration.duplicati.duplicati-windows-service
name: duplicati-windows-service
category: computing-software
field: systems-network-administration
product: duplicati
tags: [windows-service, windows-installation, service-install-command, no-hosted-server, secure-datafolder, trayicon-connect-service]
level: practitioner
status: docs-checked
description: "Install the Duplicati Server as a Windows service, pass options at install time or via preload settings and connect the TrayIcon to the service."
sources: ["https://docs.duplicati.com/detailed-descriptions/platform-specific-guides/using-duplicati-with-windows"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Running Duplicati as a Windows service

Choose the type (TrayIcon, Server, Agent or CLI) and the CPU (x64, Arm64 or x86; Windows 10 was the last version supporting 32 bit). The default download is the x64 GUI MSI. Run in a user context, the TrayIcon and Server share a data folder under the user's AppData\Local\Duplicati holding the local databases and the Server database.

Service: the installation folder contains `Duplicati.WindowsService.exe`. Run it with `INSTALL` or `UNINSTALL`; installing starts the service automatically and uninstalling stops it. Server options can follow INSTALL, for example `INSTALL --webservice-port=8100 --server-datafolder=<path>`. Alternatively use `preload.json` to change settings without an uninstall and install cycle (a service restart is still needed).

From 2.3.1.0 the Server refuses a data folder that other users can access. If you pass your own `--server-datafolder`, lock it down from an elevated prompt with `Duplicati.CommandLine.ConfigureTool.exe secure-datafolder --for-service --datafolder=<path>`.

Ports: the service defaults to 8200 and fails if that port is taken. A TrayIcon runs a different, separate server instance, usually on port 8300. To point the TrayIcon at the service, edit its shortcut to add `--no-hosted-server --hosturl=http://localhost:8200 --webservice-password=<password>`.

The Agent installs by default as a Windows service in the LocalService account rather than a user, so it only needs to be registered with the Duplicati Console.

## Checked

2026-11-04. Confirmed against the Using Duplicati with Windows page. Nothing removed.

Method: documentation only; no commands were run.
