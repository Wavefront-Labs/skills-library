---
id: computing-software.systems-network-administration.syncthing.privacy-and-information-leakage
name: privacy-and-information-leakage
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, security, global-discovery, usage-reporting]
level: practitioner
status: docs-checked
description: "Know what Syncthing discloses through global discovery, local discovery, upgrade checks and usage reporting, and how to switch each off."
sources: ["https://docs.syncthing.net/users/security.html", "https://docs.syncthing.net/users/config.html", "https://docs.syncthing.net/users/syncthing.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# What Syncthing discloses

## Protection
All device to device traffic is protected by TLS. At connection establishment the certificate fingerprint of each device is compared to a preset list of acceptable devices. The fingerprint is the SHA-256 hash of the certificate, shown in a human-friendly encoding called Device ID.

## Global discovery (default on)
An announcement with the device ID and listening port(s) goes to the global discovery servers every 30 minutes, so they can keep a mapping between the device ID and external IP. When connecting to devices not seen on the local network, a query with the requested device ID is sent. The connection is encrypted with TLS and the server certificate is verified. An eavesdropper on the Internet can deduce which machines run Syncthing with global discovery and their device IDs; the server operator can map device addresses to IP addresses and deduce which devices are connected to each other. When turned off, devices with dynamic addresses not on the local network cannot be found. If a different global discovery server is configured, no data is sent to the default ones.

## Local discovery (default on)
Broadcast (IPv4) and multicast (IPv6) packets are sent to the local network every 30 seconds, containing the device ID and listening port. An eavesdropper on the local network can deduce which machines run Syncthing and their device IDs. When turned off, devices with dynamic addresses on the local network cannot be found.

## Upgrade checks (default on)
An HTTPS check for a new version at startup and then every twelve hours. Even with automatic upgrades disabled, a check is made when the GUI loads (to show the Upgrade button); that can only be disabled by compiling Syncthing with upgrades disabled. The download itself comes from GitHub. The requests contain no identifiable information about the user or device. The config page says `autoUpgradeIntervalH` set to `0` disables automatic upgrades; the command line has `--no-upgrade`.

## Usage reporting (default off)
If enabled, usage data is reported at startup and then every 24 hours as an HTTPS POST. The contents can be seen behind the Preview link in settings. The GUI asks once about enabling it, shortly after first install. `urAccepted` of `-1` means no; the default `0` means no choice has been made.

## Checked
2026-11-04. Read Security Principles (Information Leakage sections), the config page (`autoUpgradeIntervalH`, `urAccepted`) and Command Line Operation (`--no-upgrade`): TLS and device ID, 30-minute and 30-second announcement intervals, upgrade check timing, GUI-load check, GitHub download, usage report timing and defaults. Reworded to the page text.
Method: documentation only; no commands were run.
