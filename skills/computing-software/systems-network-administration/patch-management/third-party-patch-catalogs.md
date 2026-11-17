---
id: computing-software.systems-network-administration.patch-management.third-party-patch-catalogs
name: third-party-patch-catalogs
category: computing-software
field: systems-network-administration
product: patch-management
tags: [third-party-catalog, configmgr, intune, enterprise-app-catalog, wsus-publishing, third-party-patching]
level: practitioner
status: docs-checked
description: "Patch third-party Windows apps from catalogs: ConfigMgr third-party update catalogs (subscribe, publish, deploy) and Intune Enterprise App Catalog auto-update limits."
sources:
  - https://learn.microsoft.com/en-us/mem/configmgr/sum/deploy-use/third-party-software-updates
  - https://learn.microsoft.com/en-us/mem/intune/apps/apps-enterprise-app-management
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Third-party patch catalogs

A catalog publishes third-party app updates into your existing patch tool so they follow the same deployment process as Microsoft updates. This skill covers the two Microsoft-documented routes.

## Options
| Option | Delivery |
|---|---|
| ConfigMgr third-party software update catalogs | Subscribe to a partner or custom catalog; metadata syncs into WSUS, you publish content for the updates you want, then deploy like any software update |
| Intune Enterprise App Catalog (Enterprise App Management) | Microsoft-hosted Win32 apps (exe and msi) installed by the Intune management extension; needs a subscription in addition to Intune Plan 1 or Plan 2 |

## ConfigMgr setup (once per hierarchy)
1. Administration > Site Configuration > Sites, top-level site > Configure Site Components > Software Update Point > Third-Party Updates tab > Enable third-party software updates.
2. Choose the WSUS signing certificate mode on that tab: "Configuration Manager manages the certificate" (self-signed, no PKI needed) or "Manually manage the certificate" (for a PKI certificate, using System Center Updates Publisher or another tool). Managed certificate handling runs during the sync cycle and logs to wsyncmgr.log.
3. Client settings (custom client setting, Software Updates tab): Enable third-party software updates = Yes. This sets the Windows Update agent policy "Allow signed updates for an intranet Microsoft update service location" and installs the signing certificate in the client Trusted Publisher store. Client-side logging is in updatesdeployment.log.
4. Software Library > Software Updates > Third-Party Software Update Catalogs: select a catalog > Subscribe to Catalog, approve the catalog certificate, pick a schedule (the default simple schedule syncs every 7 days). Custom catalogs must use https and the updates must be digitally signed.
5. Run a software updates synchronization manually so the product metadata reaches the Configuration Manager database, enable the product in the SUP, then synchronize again. The updates appear in All Software Updates as metadata-only (blue arrow icon).
6. Select the updates you need > Publish Third-Party Software Update Content. This downloads the binaries from the vendor into the WSUSContent directory on the top-level SUP; run a sync again to turn them into deployable updates. Progress is in SMS_ISVUPDATES_SYNCAGENT.log.
7. Deploy through the normal Deploy Software Updates process. On the Download Locations page keep "Download software updates from the internet" (the content is already published to the SUP).

For v3 catalogs you can limit sync to chosen categories and optionally stage content for chosen categories automatically. The page recommends "Do not stage content, synchronize for scanning only", and staging only what you are likely to deploy, because of bandwidth and storage.

## Intune Enterprise App Catalog
- Intune prefills install and uninstall commands, detection rules (file size, file version, registry) and requirements (architecture, minimum OS); Microsoft recommends keeping the prefilled values.
- Auto-update: for catalog apps with a Required assignment on Windows 10 or 11, Intune applies new catalog versions without a new app or supersedence relationship. Apps assigned as Available keep the existing workflow. To review updates first, use Guided update supersedence (Apps > Enterprise App Catalog apps with updates).
- Self-updating catalog apps: Intune only ensures a minimum version; the app then updates by the vendor's process, which may need tenant network rules to allow the vendor.
- Content is hosted on *.manage.microsoft.com. Catalog apps are installed by the Intune management extension, not winget.
- ConfigMgr does not directly support Enterprise App Management apps; co-managed clients can get them when targeted from Intune.

## Gotchas
- ConfigMgr: "Publish third-party software update content" fails on metadata-only updates that another tool such as SCUP added to WSUS (message 11524); use that tool to publish the content.
- ConfigMgr: if the catalog provider changes its signing certificate, sync fails until you approve the new one in Security > Certificates (message 11508). Unsigned content cannot be published (11516). Old-format catalogs lack content certificates (11523): unblock the certificate in the Certificates node and publish again.
- ConfigMgr: the WSUS signing certificate must be trusted on the console machine, or the signature check fails when downloading. A proxy-dependent top-level SUP needs WinHTTP proxy settings on the site system.
- ConfigMgr: with a CMG for content storage, third-party update content will not download to clients if "Download delta content when available" is enabled.
- Intune auto-update has no rollback or automatic uninstall remediation, no rollout rings (all targeted devices get the new version at once), and the catalog is cached for up to one hour. If Microsoft revokes a malicious version you must find and remediate affected devices yourself.
- Intune auto-update conflicts with other app types (for example a line-of-business app) targeting the same product; manage each app through one deployment type.

## Verify
ConfigMgr: update shows as deployable (not metadata-only) in All Software Updates and clients report compliance after a Software Updates Scan Cycle. Intune: the Managed Apps report shows the app version and install status per device.

## Checked
Date: 2026-11-07. Read in full: Configuration Manager "Enable third-party updates" (setup, certificate modes, client setting, subscribe, publish, v3 options, known issues, status messages 11508/11516/11523/11524) and Intune "Enterprise Application Management" (prerequisites, self-updating apps, auto-update scope and limitations, FAQ). Removed as unconfirmed: all Patch My PC claims (its docs root was not read), Ivanti, ManageEngine, Action1 and winget-tool rows, Graph app-registration steps, "update only" vs "app + updates" modes, Intune requirement-rule and supersedence behaviour for non-Microsoft catalogs, per-user install handling, the generic scanner-finding verification, and the GPO-off failure statement (page only says the client setting sets that policy). The `docs.patchmypc.com` source was dropped.
Method: documentation only; no commands were run.
