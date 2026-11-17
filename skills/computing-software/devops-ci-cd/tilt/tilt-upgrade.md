---
id: computing-software.devops-ci-cd.tilt.tilt-upgrade
name: tilt-upgrade
category: computing-software
field: devops-ci-cd
product: tilt
tags: [upgrade, tilt, install, package-managers]
level: intro
status: docs-checked
description: "Upgrade Tilt to the latest version using the install script or the method matching your original install: Homebrew, Scoop, Conda, asdf or manual."
sources:
  - "https://docs.tilt.dev/upgrade.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrading Tilt

Goal: move to the latest Tilt release. Usually rerunning the install script is enough; otherwise use the method you installed with. Releases are listed on the tilt-dev/tilt GitHub Releases page.

## Install script

macOS or Linux:

```bash
curl -fsSL https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh | bash
```

Windows (PowerShell):

```powershell
iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.ps1'))
```

## Other methods

```bash
# Homebrew (macOS or Linux)
brew update && brew upgrade tilt-dev/tap/tilt

# Scoop
scoop update tilt

# Conda
conda update -c conda-forge tilt

# asdf (example version from the page)
asdf plugin add tilt
asdf install tilt 0.37.8
asdf global tilt 0.37.8
```

## Manual install

If you installed by downloading a release binary into your PATH, you may need to do the same to upgrade. The page's example uses version 0.37.8.

macOS:

```bash
curl -fsSL https://github.com/tilt-dev/tilt/releases/download/v0.37.8/tilt.0.37.8.mac.x86_64.tar.gz | tar -xzv tilt && \
  sudo mv tilt /usr/local/bin/tilt
```

Linux: same, with the asset `tilt.0.37.8.linux.x86_64.tar.gz`.

Windows:

```powershell
Invoke-WebRequest "https://github.com/tilt-dev/tilt/releases/download/v0.37.8/tilt.0.37.8.windows.x86_64.zip" -OutFile "tilt.zip"
Expand-Archive "tilt.zip" -DestinationPath "tilt"
Move-Item -Force -Path "tilt\tilt.exe" -Destination "$home\bin\tilt.exe"
```

## Checked

2026-11-07. Pages read from the tilt-dev/tilt.build source of docs.tilt.dev. Read the Upgrade page in full. Confirmed the install script commands, the Homebrew, Scoop, Conda and asdf commands, and the manual install commands for macOS, Linux and Windows, including the 0.37.8 example version on the page. Softened: the manual upgrade sentence (the page says "may need to"). 

Method: documentation only; no commands were run.
