---
id: computing-software.cybersecurity-defensive.nessus.offline-plugin-updates
name: offline-plugin-updates
category: computing-software
field: cybersecurity-defensive
product: nessus
tags: [nessus, nessus-deployment, offline-plugin-update, air-gapped, challenge-code, all-2-0-tar-gz, plugin-feed, tenable-sc]
level: practitioner
status: docs-checked
description: "Keep an air-gapped Nessus scanner current: offline registration with challenge code, downloading and installing plugin archives, and verifying the feed date."
sources: ["https://docs.tenable.com/nessus/Content/InstallNessusOffline.htm", "https://docs.tenable.com/nessus/Content/UpdatePluginsOffline.htm", "https://docs.tenable.com/nessus/Content/NessusCLI.htm", "https://docs.tenable.com/security-center/Content/OfflineNessusPluginUpdate.htm"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Offline plugin updates for air-gapped scanners

**Goal:** an isolated scanner whose plugins are updated through a controlled transfer process.

## One-time offline registration (Nessus 10.12 guide)
1. On the scanner's Welcome to Nessus page choose **Register Offline**, pick the product type and note the **Challenge Code** (also available on the CLI with `nessuscli fetch --challenge`).
2. On an internet-connected computer open the Nessus offline registration page (`https://plugins.nessus.org/v2/offline.php`), enter the challenge code and your activation code, and submit.
3. The next page shows a **Custom URL** (downloads the plugins file; specific to your licence, save it, you reuse it for every update), the **licence text** (from `-----BEGIN Tenable, Inc. LICENSE-----` to `-----END Tenable, Inc. LICENSE-----`) and a `nessus.license` file.
4. Download the plugins TAR file from the Custom URL and also the **signature file**; Nessus needs the signature to verify the TAR. Copy both to the offline system.
5. Paste the licence text on the Product Registration screen and continue. (On an already-installed host, `nessuscli fetch --register-offline nessus.license` registers from the licence file and sets offline mode.)

Offline mode disables features that need the Nessus feed, including `nessuscli update` from the feed. Tenable recommends this process only for offline instances; online instances receive plugin updates automatically.

## Routine update
1. On the internet-connected computer open the saved Custom URL to download the plugins TAR file, and download its signature file.
2. Transfer both files by your approved process.
3. Install, either:
   - UI: Settings > Software Update > **Manual Software Update** > **Upload your own plugin archive and signature file**; or
   - CLI, from the Nessus `sbin` directory (`/opt/nessus/sbin/` on Linux, the Tenable Nessus folder under Program Files on Windows, `/Library/Nessus/run/sbin/` on macOS): `nessuscli update <tar.gz file name> <tar.gz.sig file name>`.

## Tenable Security Center (offline plugin update)
Security Center uses a different file. Per the Security Center 6.9 guide: run `nessuscli fetch --challenge` on a Nessus scanner installed on the Security Center host (not started or configured; uninstall it afterwards), submit the challenge string and activation code at `https://plugins.nessus.org/offline.php` (not the `/v2/` page), copy the `https://plugins.nessus.org/get.php...` link and change `all-2.0.tar.gz` to `sc-plugins-diff.tar.gz`, download it, verify it with the MD5 checksum from Tenable's knowledge base article, then upload it in Security Center under System > Configuration > Plugins/Feed > Schedules > Active Plugins. Do not click the `nessus-fetch.rc` link. The guide also notes offline feed files can be downloaded from connect.tenable.com (Account Management > Products > Security Center > Manage Product > View Feed Credentials).

## Verify
- [ ] After the update the plugin set date shown in Nessus (Settings > About) matches the archive you installed.
- [ ] A transfer log with file hashes is kept for audit.

## Checked
2026-11-02. Confirmed from Tenable Nessus 10.12 pages "Install Tenable Nessus Offline", "Update Plugins Offline", the Nessus CLI page (fetch commands), and Security Center 6.9 "Perform an Offline Nessus Plugin Update". Removed (not stated there): the `all-2.0.tar.gz` name as the Nessus download file, SHA-256 recording, "plugins published daily / zero-day within hours" cadence and SLA advice, pausing of scanning during compilation, behaviour after re-running `fetch --challenge`, version-mismatch failure, clock-skew claim, "separate feeds for passive and compliance".

Method: documentation only; no commands were run.
