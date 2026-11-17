---
id: computing-software.systems-network-administration.restic.shell-completion
name: shell-completion
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, autocompletion, bash, zsh, fish, powershell, man-pages]
level: intro
status: docs-checked
description: "Generate bash, zsh, fish and PowerShell completion scripts and man pages with restic generate."
sources:
  - https://restic.readthedocs.io/en/stable/020_installation.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Autocompletion and man pages

`restic generate` writes completion scripts and man pages. List its options with `restic generate --help`.

## Flags

- `--bash-completion file`
- `--zsh-completion file`
- `--fish-completion file`
- `--powershell-completion file`
- `--man directory`

Passing `-` as the file writes the script to stdout.

## Install examples

```
sudo restic generate --bash-completion /etc/bash_completion.d/restic
sudo restic generate --zsh-completion /usr/local/share/zsh/site-functions/_restic
```

The bash target directory differs by system; the docs give `/usr/share/bash-completion/completions/restic` as the Debian location.

## PowerShell

Create your profile if it does not exist, generate the script, then source it from the profile:

```
If (!(Test-Path $PROFILE.CurrentUserAllHosts)) {New-Item -Path $PROFILE.CurrentUserAllHosts -Force}
$ProfileDir = (Get-Item $PROFILE.CurrentUserAllHosts).Directory
restic generate --powershell-completion "$ProfileDir\restic-completion.ps1"
Add-Content -Path $PROFILE.CurrentUserAllHosts -Value "`r`nImport-Module $ProfileDir\restic-completion.ps1"
```

`restic generate --man directory` writes man pages to the given directory.

## Checked

2026-11-03. Confirmed in the restic docs page Installation (Autocompletion): the `generate` flags, `-` for stdout, the sudo bash and zsh examples, the Debian bash path note, and the PowerShell profile example (now matching the docs). Removed: the advice to copy man pages into a search path and to open a new shell (not in the docs).

Method: documentation only; no commands were run.
