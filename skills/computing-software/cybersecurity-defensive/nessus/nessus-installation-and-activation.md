---
id: computing-software.cybersecurity-defensive.nessus.nessus-installation-and-activation
name: nessus-installation-and-activation
category: computing-software
field: cybersecurity-defensive
product: nessus
tags: [nessus, nessus-deployment, nessus-installation, activation-code, nessus-professional, nessus-manager, nessusd, plugin-download, tenable]
level: intro
status: docs-checked
description: "Install and activate Nessus on Linux or Windows, choose the right edition, complete plugin compilation and harden the web UI before first scan."
sources: ["https://docs.tenable.com/nessus/Content/InstallNessusLinux.htm", "https://docs.tenable.com/nessus/Content/InstallNessusWindows.htm", "https://docs.tenable.com/nessus/Content/ConfigureNessus.htm", "https://docs.tenable.com/nessus/Content/HardwareRequirements.htm", "https://docs.tenable.com/nessus/Content/InstallNessusOffline.htm"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nessus installation and activation

**Goal:** a working scanner with current plugins, on adequately sized hardware, reachable only by the people who should run scans.

## Choose the edition
The Nessus 10.12 guide covers installing Nessus Essentials, Professional, Expert or Manager, activating a Professional or Expert trial, or linking the scanner to Tenable One Vulnerability Management or Tenable Security Center. In an enterprise you normally install the package and link it instead of activating standalone (see the linking skill in this folder). Nessus Essentials does not support offline installation.

## Install (Linux)
Example commands from the Tenable guide (run as root; pick the package for your distribution):
```
dpkg -i Nessus-<version number>-debian6_amd64.deb              # Debian/Kali, Ubuntu
dnf install Nessus-<version number>-el8.x86_64.rpm             # Red Hat
sudo zypper install Nessus-<version number>-suse12.x86_64.rpm  # SUSE
systemctl start nessusd
```
Then browse to `https://<host>:8834` (or `https://localhost:8834`) and finish setup in the browser. Rpm installs also need the `hostname` package (the `yum`/`dnf` tools pull it in as a dependency). Installing on a host that already runs nessusd terminates the other nessusd processes and you may lose scan data. Symbolic links for `/opt/nessus/` are not supported.

Windows: run the downloaded installer (InstallShield wizard); the Welcome to Nessus page then opens in the browser on port 8834.

## First-run configuration
The browser warns about the certificate because Nessus ships a self-signed SSL certificate. On the Welcome page, Settings lets you set a proxy server (needed if the scanner will be linked through a proxy), a custom plugin feed host, and an encryption password; if you set the encryption password it encrypts policies, scan results and configurations, must be entered whenever Nessus restarts, and cannot be recovered by an administrator or Tenable Support. Plugin configuration and initialization can take several minutes.

## Sizing (Nessus 10.12 hardware requirements)
Scanning up to 50,000 hosts per scan: 4 cores at 2 GHz, 4 GB RAM (8 GB recommended), 30 GB disk, not counting the operating system. Over 50,000 hosts per scan: 8 cores, 8 GB RAM (16 GB recommended), 30 GB disk. Disk use grows with results, plugin updates and logs; on Linux the disk requirement applies to `/opt`. Complex scans, especially credentialed ones, may need more. Nessus Manager has its own, larger requirements; see the page.

## Hardening
Use the Nessus Advanced Settings and certificate guidance (see the custom TLS certificate skill in this folder) rather than ad hoc changes. Limit who can reach the web port with a host firewall.

## Gotchas
- Proxy environments: configure the proxy on the Welcome page before linking or registering.
- Offline hosts: choose Register Offline during setup (see the offline plugin updates skill).

## Verify
- [ ] Settings > About shows a current plugin set.
- [ ] A basic scan of a lab host completes.
- [ ] The web port is not reachable from user networks.

## Checked
2026-11-02. Confirmed from Tenable Nessus 10.12 pages "Install Tenable Nessus on Linux", "Install Tenable Nessus on Windows", "Configure Tenable Nessus", "Hardware Requirements" and "Install Tenable Nessus Offline". Removed (not stated there): edition feature descriptions (Expert "external attack surface and IaC"), 15-60 minute plugin compile time, Windows service name, certificate directory path and `nessuscli fix` certificate option, EDR exclusion advice, NTP/time-skew claim, activation-code reuse behaviour, the `rpm -ivh` form.

Method: documentation only; no commands were run.
