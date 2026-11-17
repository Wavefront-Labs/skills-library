---
id: computing-software.cloud-infrastructure-engineering.docker.docker-desktop-settings-management-admin-settings
name: docker-desktop-settings-management-admin-settings
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-desktop, admin-settings-json, settings-management, enforce-sign-in, enhanced-container-isolation, docker-business, mdm, fleet-configuration]
level: advanced
status: docs-checked
description: "Lock Docker Desktop settings across a fleet with admin-settings.json or Admin Console Settings Management: file locations, locked/value keys, sign-in enforcement, verification."
sources: ["https://docs.docker.com/desktop/enterprise/hardened-desktop/settings-management/", "https://docs.docker.com/desktop/enterprise/hardened-desktop/settings-management/configure-json-file/", "https://docs.docker.com/desktop/enterprise/hardened-desktop/settings-management/settings-reference/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Docker Desktop Settings Management (admin-settings.json)

**Goal:** an IT/platform team pins security-relevant Docker Desktop settings (proxy, ECI,
TCP socket exposure, extensions, updates) on every developer machine so users cannot
change them.

## Prerequisites
- Docker Business subscription and **enforced sign-in** to your organisation. Settings
  apply only once the user signs in with an account in that org; an unsigned-in Desktop
  ignores the policy. The presence of `admin-settings.json` itself forces sign-in.
- Delivery methods: the local JSON file (created with the `--admin-settings` installer flag or by hand; Docker suggests MDM tools such as Jamf to distribute it) or cloud policies created in Docker Home. Policy precedence: user-specific policies, then the organization default policy, then the local `admin-settings.json` (lowest priority, overridden by Docker Home policies). Policies need a verified organisation domain to take effect.

## File location (create as UTF-8 without BOM)
| OS | Path |
|---|---|
| macOS | `/Library/Application Support/com.docker.docker/admin-settings.json` |
| Windows | `%ProgramData%\DockerDesktop\admin-settings.json` (the ProgramData folder, normally on the system drive) |
| Linux | `/usr/share/docker-desktop/admin-settings.json` |

Place the file in a protected directory to prevent unauthorised changes. The macOS and Windows installers accept `--admin-settings` to generate it, for example `--allowed-org=<org name> --admin-settings="{'configurationFileVersion': 2, 'enhancedContainerIsolation': {'value': true, 'locked': false}}"`.

## Structure
```json
{
  "configurationFileVersion": 2,
  "exposeDockerAPIOnTCP2375": { "locked": true,  "value": false },
  "enhancedContainerIsolation": {
    "locked": true, "value": true,
    "dockerSocketMount": { "imageList": { "images": ["docker.io/testcontainers/ryuk:*"] } }
  },
  "proxy": { "locked": true, "mode": "manual",
             "http": "http://proxy.corp:3128", "https": "http://proxy.corp:3128",
             "exclude": ["localhost", "127.0.0.1", ".corp"] },
  "extensionsEnabled":        { "locked": true,  "value": true },
  "onlyMarketplaceExtensions": { "locked": true, "value": true },
  "disableUpdate":            { "locked": false, "value": false },
  "analyticsEnabled":         { "locked": true,  "value": false },
  "blockDockerLoad":          { "locked": true,  "value": true },
  "filesharingAllowedDirectories": [ { "path": "$HOME", "sharedByDefault": true } ],
  "linuxVM": { "dockerDaemonOptions": { "locked": true, "value": "{\"debug\": false}" } },
  "kubernetes": { "locked": false, "enabled": false }
}
```
- `locked: true`: users cannot change the value in Docker Desktop, the CLI or config files. `locked: false` is a default the user may change, and is ignored on existing installs where the user already customised that value.
- Some settings are grouped under one toggle (ECI, Kubernetes, Docker Scout); locking the main toggle locks the whole group.
- Docker's settings reference lists each key with its platform and minimum Desktop version; check it before relying on a key. The proxy `exclude` value is an array of strings, and `proxy.mode` is `system` or `manual`.
- ECI `dockerSocketMount.imageList.images` allows the listed images (for example Testcontainers' Ryuk) to mount the Docker socket.

## Rollout
1. Pilot group: deploy the file and enforce sign-in as described on Docker's enforce sign-in page.
2. Settings take effect after Docker Desktop restarts and the user signs in. For existing installs, fully quit and reopen Desktop; restarting from the menu is not sufficient, and Desktop does not prompt users to do so.
3. Watch for proxy lockouts: a wrong locked proxy breaks pulls for everyone; keep
   `exclude` covering internal registries. Note that `containersProxy` governs image pulls and `proxy` governs Desktop host-level traffic.

## Verify
- Enforced settings appear grayed out in Docker Desktop and cannot be changed through the Dashboard, CLI or configuration files; try toggling one.
- Docker's compliance reporting page describes per-user compliance checks for cloud policies.

## Checked

Checked against docker/docs `desktop/enterprise/hardened-desktop/settings-management/` (`_index.md`, `configure-json-file.md`, `settings-reference.md`) and the Windows and macOS install pages (docker/docs latest commit 2026-10-23).

- Prerequisites (Business subscription, enforced sign-in, file forces sign-in), file locations for macOS, Windows and Linux, `locked` semantics, grouped settings, `--admin-settings` installer flag, policy precedence order, apply-after-full-restart behaviour, `proxy` and `containersProxy` roles, `exclude` as an array, `filesharingAllowedDirectories` entries with `path` and `sharedByDefault`, and key names `analyticsEnabled`, `extensionsEnabled`, `onlyMarketplaceExtensions`, `disableUpdate`, `blockDockerLoad`.
- Removed as unconfirmed: registry key and `registry.json` rollout details, the `Admin Console` navigation path, the `docker info` and `uid_map` verification steps, the silent-ignore statement for unknown keys and the installer command spelling for Windows.

Method: documentation only; no commands were run.
