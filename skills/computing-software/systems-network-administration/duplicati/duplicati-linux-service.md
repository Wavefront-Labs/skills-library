---
id: computing-software.systems-network-administration.duplicati.duplicati-linux-service
name: duplicati-linux-service
category: computing-software
field: systems-network-administration
product: duplicati
tags: [systemd-service, linux-install, etc-default-duplicati, duplicati-server-linux, arm-architecture]
level: practitioner
status: draft
description: "Choose the Duplicati type, package and CPU architecture on Linux and run the Server as a systemd service configured through the defaults file."
sources: ["https://docs.duplicati.com/detailed-descriptions/platform-specific-guides/using-duplicati-with-linux"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Using Duplicati on Linux

Decide three things: the type (TrayIcon/GUI, Server, Agent or CLI), the package format (`.deb` for Debian-based, `.rpm` for Red Hat-based and SUSE, `.zip` for others or check your package manager) and the CPU (x64, Arm64 for Raspberry Pi 4 and some servers, Arm7 for 32-bit Pi 3 and older and some NAS devices). FreeBSD is not yet supported. Packages come from the download page under Other versions.

TrayIcon: recommended for desktops with no special needs; launch from the program menu or with `duplicati`. Run as a user it keeps the Server database and local databases in `~/.config/Duplicati`.

Server: run `duplicati-server`; as a regular user it shares the same `~/.config/Duplicati` folder and configuration as the TrayIcon. For a service, the `.deb` and `.rpm` packages include a systemd service; for a zip install, take the service file from the source repository. Pass server options by editing the defaults file only: `/etc/default/duplicati` for deb packages or `/etc/sysconfig/duplicati` for rpm packages, because the service file is overwritten on upgrade. Running the Server as root means its web server has root's privileges, so lock down access as described in the Server security options. Docker is an alternative.
