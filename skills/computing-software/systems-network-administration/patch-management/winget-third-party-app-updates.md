---
id: computing-software.systems-network-administration.patch-management.winget-third-party-app-updates
name: winget-third-party-app-updates
category: computing-software
field: systems-network-administration
product: patch-management
tags: [third-party-patching, winget, winget-upgrade, microsoft-store, private-source, system-context, windows, patch-management]
level: practitioner
status: docs-checked
description: "Patch third-party Windows apps with winget: upgrade --all in system context, pinning versions, private REST sources, exit codes for scripting, and limits vs commercial catalogues."
sources:
  - https://learn.microsoft.com/en-us/windows/package-manager/winget/upgrade
  - https://learn.microsoft.com/en-us/windows/package-manager/winget/pinning
  - https://learn.microsoft.com/en-us/windows/package-manager/winget/source
  - https://learn.microsoft.com/en-us/windows/package-manager/winget/troubleshooting
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Third-party app updates with winget

**Goal:** keep common third-party applications (browsers, PDF readers, 7-Zip, runtimes)
current on Windows endpoints and servers without hand-packaging every release.

## Commands
```powershell
winget upgrade                                 # list available upgrades
winget upgrade --all --silent --accept-package-agreements --accept-source-agreements --disable-interactivity
winget upgrade --id <Publisher.Package> --exact --silent --scope machine
winget pin add --id <Publisher.Package> --version 8.*   # hold a version line (wildcard allowed as the last version part)
winget list --upgrade-available --source winget
```
Use `--id` with `--exact` in scripts; names are ambiguous. Other options in the upgrade reference: `--all` (also `-r`), `--include-unknown`, `--allow-reboot`, `--accept-package-agreements`, `--accept-source-agreements`, `--disable-interactivity`.

## Running unattended
- winget is delivered through App Installer (an MSIX package registered per user). Microsoft's troubleshooting page states the WinGet CLI is not supported in the SYSTEM (LocalSystem) context, and that the Microsoft.WinGet.Client PowerShell module can be used in system context for applications installed machine-wide. For Intune remediation, scheduled tasks or RMM, use that module or run in a user context. Servers may need App Installer installed first; check support for your server version in the documentation.
- Check each command's exit code and log output for evidence (see the winget logs section of the troubleshooting page).
- Restrict to an allow-list of package IDs for servers instead of `--all`.

## Private source
Host a winget REST source (Microsoft's reference implementation on Azure) or use the
Intune/WinGet integration to approve packages internally; add with
`winget source add --name corp --arg https://<rest-source> --type Microsoft.Rest`.
Check the winget documentation for policy options to restrict sources.

## Limits
- Community manifests: vet publishers; prefer packages with verified installers and hashes
  (winget checks the installer hash in the manifest; `--ignore-security-hash` exists and is not recommended).
- Some apps self-update or install per-user, and winget cannot always upgrade them in
  system context.
- No built-in rings or reporting; commercial catalogues add approvals and reporting.

## Verify
After the run `winget upgrade` lists nothing (or only pinned items); inventory shows the
new versions; scanner findings for those apps close at the next scan.

## Checked
Date: 2026-10-27. Documentation: Microsoft Learn winget upgrade, pinning, source, list and troubleshooting pages (options listed above, gating pins with a trailing wildcard, `source add --name --arg --type Microsoft.Rest`, `list --upgrade-available`, the statement that the WinGet CLI is not supported in system context). Corrected the system-context advice; removed unconfirmed package IDs, exit code claims, the ADMX claim and product names.
Method: documentation only; no commands were run.
