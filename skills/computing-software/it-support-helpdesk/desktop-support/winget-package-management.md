---
id: computing-software.it-support-helpdesk.desktop-support.winget-package-management
name: winget-package-management
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, command-line-tools, winget-cli, winget, windows-package-manager, winget-upgrade, winget-export, app-installer, msstore-source]
level: practitioner
status: docs-checked
description: "Use winget for installs and updates on Windows: search/install by ID, silent and scoped installs, upgrade --all, export/import app lists, running as SYSTEM, and source policies."
sources:
  - "https://learn.microsoft.com/en-us/windows/package-manager/winget/install"
  - "https://learn.microsoft.com/en-us/windows/package-manager/winget/upgrade"
  - "https://learn.microsoft.com/en-us/windows/package-manager/winget/export"
  - "https://learn.microsoft.com/en-us/windows/package-manager/winget/import"
  - "https://learn.microsoft.com/en-us/windows/package-manager/winget/source"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# winget-package-management

Goal: install, update and inventory apps from the command line, consistently.

## Basics
```powershell
winget search "7-zip"
winget show --id 7zip.7zip
winget install --id 7zip.7zip --exact --silent --accept-package-agreements --accept-source-agreements
winget upgrade                    # list apps with updates
winget upgrade --all --silent
winget list                       # installed apps
winget uninstall --id Zoom.Zoom --exact
```
Use `--id` with `--exact` in scripts; `--exact` requires an exact
(case-sensitive) match. `--accept-package-agreements` accepts the package's
own licence terms; combine with `--silent` for a fully non-interactive
install. `winget upgrade --all` upgrades every installed app that has an
update available.

## Scope
`--scope` lets you choose whether the installer targets user or machine
scope; some packages support only one (see Microsoft's known issues for
package installation scope).

## Moving a user's apps
```powershell
winget export -o apps.json        # on the old PC
winget import -i apps.json --accept-package-agreements   # on the new PC
```
Review the file before importing.

## Sources
`winget source list` shows the sources. The defaults are `winget` (community
repository), `msstore` (Microsoft Store catalogue) and `winget-font`. A source
can also be a REST source. Community packages are not vetted by your own
security team; approve package IDs through your software catalogue.

## Gotchas
- A failed install can come from an architecture or scope mismatch.
- Keep App Installer updated for new features and fixes.

## Verify
`winget list --id <id>` shows the expected version and the app launches; after
bulk upgrades `winget upgrade` lists nothing pending for approved apps.


## Checked

Date 2026-10-27. Documentation release: Microsoft Learn winget install, upgrade, import, export, list and source pages, as published October 2026. Confirmed: --id, --exact, --silent, --accept-package-agreements, --accept-source-agreements, --scope, upgrade --all, export -o, import -i (--import-file), the three default sources and REST sources. Removed: running as SYSTEM and the WindowsApps resolve path, Intune Store app advice, ADMX/CSP source-policy claims, and the 'no applicable installer' explanation, none of which a readable page covers.

Method: documentation only; no commands were run.
