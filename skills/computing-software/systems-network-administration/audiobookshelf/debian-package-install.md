---
id: computing-software.systems-network-administration.audiobookshelf.debian-package-install
name: debian-package-install
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [debian, apt, deb, systemd, etc-default, amd64]
level: practitioner
status: docs-checked
description: "Install Audiobookshelf from the official Debian apt repository on amd64 and configure it in /etc/default/audiobookshelf."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/linux/3.linux-install-deb.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Debian package is for **amd64** only. Activate the repository:

```bash
sudo apt install gnupg curl
wget -O- https://advplyr.github.io/audiobookshelf-ppa/KEY.gpg | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/adb-archive-keyring.gpg 1>/dev/null
sudo curl -s -o /etc/apt/sources.list.d/audiobookshelf.list https://advplyr.github.io/audiobookshelf-ppa/audiobookshelf.list
sudo apt update
sudo apt install audiobookshelf
```

The service reads `/etc/default/audiobookshelf`. Defaults:

```bash
METADATA_PATH=/usr/share/audiobookshelf/metadata
CONFIG_PATH=/usr/share/audiobookshelf/config
FFMPEG_PATH=/usr/lib/audiobookshelf-ffmpeg/ffmpeg
FFPROBE_PATH=/usr/lib/audiobookshelf-ffmpeg/ffprobe
PORT=13378
```

After editing the file, apply it with `sudo systemctl restart audiobookshelf.service`.

Caution from the page: a backup from another installation method cannot be loaded after installation without losing progress. Use Docker if you plan to switch drives or OS.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: Debian install page.

Method: documentation only; no commands were run.
