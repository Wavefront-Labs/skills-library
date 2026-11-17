---
id: computing-software.systems-network-administration.jellyfin.basic-network-troubleshooting
name: basic-network-troubleshooting
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, troubleshooting, https, pfx, port-forwarding, networking]
level: intro
status: docs-checked
description: "Diagnose Jellyfin reachability problems: HTTPS certificate password, port forwarding and servers that never see the request."
sources: ["https://jellyfin.org/docs/general/administration/troubleshooting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Basic network and playback troubleshooting

Start with the logs: open the web client's console or read the log directory on the server. If media will not transcode, check the ffmpeg logs first.

Match symptom to cause using the troubleshooting guide:

- **HTTP works, HTTPS does not:** probably a certificate error. Jellyfin uses a PFX file for HTTPS. If you created the file with a password, enter that password on the **Networking** page of the settings.
- **Works on the LAN, fails from outside:** likely router configuration. Check port forwarding so the server is visible outside your network.
- **No log lines for web traffic at all, even from the LAN:** the server has not been reached. Suspect an incorrect address or a problem elsewhere on the network.

Related quick fixes from the same page:
- Text shown as boxes means missing fonts (see `computing-software.systems-network-administration.jellyfin.fallback-and-system-fonts`).
- The dashboard's active devices not showing playback progress can mean the system clock is out of sync. On systemd Linux run `timedatectl set-ntp true`, which enables NTP syncing via `chronyd` or `ntpd`, then restart Jellyfin.

## Checked

2026-11-03. Confirmed against the Jellyfin Troubleshooting page: logs and ffmpeg, PFX password on the Networking page, port forwarding, no-log-lines diagnosis, fonts pointer, timedatectl set-ntp true for out-of-sync clock. Removed: invented self-check step.

Method: documentation only; no commands were run.
