---
id: computing-software.systems-network-administration.duplicati.duplicati-choosing-package-and-installing
name: duplicati-choosing-package-and-installing
category: computing-software
field: systems-network-administration
product: duplicati
tags: [package-types, gui-package, installation, trayicon, agent-package, deb-rpm-install, appimage]
level: intro
status: draft
description: "Choose between Duplicati's GUI, CLI and Agent packages and install it on Windows, macOS and Linux from MSI, DMG, deb, rpm, zip or AppImage."
sources: ["https://docs.duplicati.com/getting-started/installation", "https://docs.duplicati.com/detailed-descriptions/platform-specific-guides/choosing-duplicati-type"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Choosing a Duplicati type and installing it

Decide what kind of instance you need first. A home user on one desktop machine uses the TrayIcon or the Agent; a headless server, or several machines, uses the Server, the CLI or the Agent.

Package types: the GUI package contains the TrayIcon, Server and CLI; the CLI package contains the Server and CLI; the Agent package contains the Agent and CLI. The TrayIcon is the simplest way to run it: one process that registers with the desktop and shows a status icon, opening the browser UI. The Server runs without a desktop, usually as a system service, writes to the system log and exposes a web server. Beware that running the Server as root or Administrator means the web server has the same privileges. It listens only on the loopback adapter and refuses connections whose hostname is not an IP address, so remote access must be enabled deliberately and protected. A password must be configured.

Installation:
- Windows: download the MSI that matches your processor (x64 for most 64-bit systems) from the download page and run the installer.
- macOS: a DMG with the application to drag into Applications (Arm64 for Apple Silicon, x64 for Intel); a `.pkg` installer also exists and sets up start at login.
- Debian-based Linux: `sudo apt install ./duplicati-version-arch.deb`; RPM-based: `sudo dnf install ./duplicati-version-arch.rpm` (yum on older Red Hat, zypper on SUSE). Packages exist for x64, Arm64 and Arm7 (ArmHF, common in NAS boxes and older Raspberry Pi).
- Other Linux: use the zip for your architecture and place the binaries in a folder; an AppImage runs without installation.
The first start opens the UI in your browser, ready to set up a backup.
