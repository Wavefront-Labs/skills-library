---
id: computing-software.systems-network-administration.patch-management.chocolatey-package-updates
name: chocolatey-package-updates
category: computing-software
field: systems-network-administration
product: patch-management
tags: [chocolatey, choco-upgrade, third-party-patching, internal-repository, package-internalizer, windows]
level: practitioner
status: docs-checked
description: "Patch third-party Windows apps with Chocolatey: internal repository, choco outdated and upgrade, pinning, scheduled upgrades, reboot exit codes and reporting."
sources:
  - https://docs.chocolatey.org/en-us/choco/commands/upgrade/
  - https://docs.chocolatey.org/en-us/guides/organizations/organizational-deployment-guide/
  - https://docs.chocolatey.org/en-us/choco/commands/pin/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Chocolatey package updates

**Goal:** keep browsers, runtimes and tools on Windows servers and desktops current from a controlled source.

## Use an internal repository
The public community repository applies rate limiting (HTTP 429), and many community packages depend on downloads from the internet. Chocolatey recommends a self-hosted Chocolatey server for reliability, and internalising packages (embedding the downloads in the package), which is different from only caching nupkg files in Nexus, ProGet or Cloudsmith. Chocolatey for Business has a "Package Internalizer" feature; otherwise do it manually.
```powershell
choco source add -n=internal -s='https://nexus.example/repository/choco/' --priority=1
choco source disable -n=chocolatey
```

## Check and upgrade
```powershell
choco outdated
choco upgrade all -y --no-progress --limit-output
choco upgrade googlechrome 7zip -y
```

## Pin what must not move
```powershell
choco pin add -n=python3 --version=3.11.9
choco pin list
```

## Schedule
Run `choco upgrade all -y` from a scheduled task or a ConfigMgr/Intune script; stagger by ring by pointing rings at repository feeds that receive packages at different times (test feed, prod feed).

## Exit codes
0 success; 1641 success with a reboot initiated; 3010 success with a reboot required. Packages may return their own exit codes when the `usePackageExitCodes` feature is on (the default). Other non-zero = failure. Treat 3010 as "schedule reboot", not failure.

## Gotchas
- Apps that self-update (browsers) can drift from the package version; whether to disable the vendor updater is a policy decision.
- Packages installed outside Chocolatey are not managed; inventory them separately.

## Verify
`choco outdated` returns nothing on a sample of hosts after the run, and the Chocolatey log on those hosts shows success.

## Checked
2026-10-28. Confirmed against the Chocolatey docs for `choco upgrade` (`--no-progress`, `--limit-output`, exit codes 1641 and 3010, `usePackageExitCodes` default), `choco pin` (`add --name --version`, `list`), `choco source` (`--priority`, `disable`), `choco outdated`, Package Internalizer (C4B) and the community repository page (rate limiting, internalising versus caching). Removed: Artifactory and Simple Server as named hosts, Central Management, the `Chocolatey.log` path and the claim about upgrading self-updating apps. The `python3` pin and `nexus.example` URL are placeholders.
Method: documentation only; no commands were run.
