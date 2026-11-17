---
id: computing-software.it-support-helpdesk.intune-mdm.device-restrictions-and-delivery-optimization-profiles
name: device-restrictions-and-delivery-optimization-profiles
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, device-restrictions-profile, delivery-optimization, configuration-profiles, settings-catalog, bandwidth]
level: practitioner
status: docs-checked
description: "Build Intune device restriction profiles per platform, plus Delivery Optimization settings (download mode, bandwidth, group ID, VPN, Connected Cache)."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/configuration/device-restrictions-configure"
  - "https://learn.microsoft.com/en-us/mem/intune/configuration/delivery-optimization-windows"
  - "https://learn.microsoft.com/en-us/windows/deployment/do/waas-delivery-optimization-reference"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# device-restrictions-and-delivery-optimization-profiles

## Device restrictions
- Create: Intune admin center > Devices > Manage devices > Configuration > Create > New policy. Choose the platform (Android device administrator, Android (AOSP), Android Enterprise, iOS/iPadOS, macOS, Windows 10 and later) and profile type Device restrictions (or Templates > Device restrictions). Then Basics, Configuration settings, Scope tags, Assignments, Review + create.
- Name policies so they are identifiable (the docs' example: `iOS/iPadOS: Block camera on devices`) and add a description.
- Typical controls: camera, app stores, built-in apps or allowed/prohibited app lists, cloud and storage backup, minimum password length and simple passwords.
- Android device administrator management is deprecated and unavailable for devices with Google Mobile Services; prefer another Android management option.
- The per-platform setting lists are linked from the Learn page. Which settings need supervision, and whether the settings catalog is a better fit, are not covered there: check the platform's settings list before relying on a setting.
- Design: a baseline profile for everyone plus targeted exceptions; avoid the same setting with different values in several profiles.

## Delivery Optimization (DO)
- Intune: Devices > Manage devices > Configuration > Create > New Policy > Windows 10 and later > Templates > Delivery Optimization. Since April 2025 the template uses the settings catalog format; existing old-format profiles remain but no new ones can be created. The policy applies at the device's next check-in.
- MDM settings live under `./Vendor/MSFT/Policy/Config/DeliveryOptimization/`.

| Setting (MDM name) | Documented behaviour |
|---|---|
| DODownloadMode | 0 HTTP only (no peering); 1 LAN (default, peers behind the same public IP); 2 Group (peering across subnets by group; recommended for most orgs); 3 Internet; 99 Simple (no DO cloud service, HTTP only); 100 Bypass (deprecated from Windows 11, can cause downloads to fail, uses BITS) |
| DOGroupID / DOGroupIDSource | GUID per device for custom groups; source 1 AD site, 2 domain SID, 3 DHCP option 234, 4 DNS suffix, 5 Entra tenant ID. Default when unset: AD site, then domain SID, then Entra tenant ID. Source applies only to mode 2 |
| DOMaxCacheAge / DOMaxCacheSize | Defaults 259,200 s (three days) and 20% |
| DOMinFileSizeToCache | Default 50 MB |
| DOMinRAMAllowedToPeer / DOMinDiskSizeAllowedToPeer | Defaults 4 GB RAM and 32 GB disk |
| DOPercentageMaxForegroundBandwidth / DOPercentageMaxBackgroundBandwidth | Default 0 (dynamic); docs recommend the absolute KB/s settings (DOMaxForegroundDownloadBandwidth, DOMaxBackgroundDownloadBandwidth) in low-bandwidth environments |
| DOMonthlyUploadDataCap | Default 20 GB; 0 means unlimited |
| DOAllowVPNPeerCaching, DOVpnKeywords | By default no peering when a VPN is detected; default keywords include VPN, Secure, Virtual Private Network |
| DOCacheHost, DOCacheHostSource | Connected Cache servers by FQDN or IP, comma-separated; DHCP option 235 discovery; DOCacheHost wins unless DOCacheHostSource = 2 (Force) |
| DOMinBatteryPercentageAllowedToUpload | By default no uploads on battery; docs suggest 40 if allowed |

- Do not set 100 (Bypass). To turn peering off use 0; with no internet access use 99.
- Group ID membership must not be used as proof of device identity.

## Verify
Per-setting status shows Succeeded on pilot devices (Monitor the profile status), and the Windows Delivery Optimization activity shows content coming from peers or cache at a multi-device site. (Client cmdlets and the Settings activity monitor are not covered by the cited pages.)

## Checked
Method: documentation only; no commands were run. Checked 2026-11-08 against the Intune Learn pages device-restrictions-configure and delivery-optimization-windows and the Windows Delivery Optimization reference (all read in full). Corrected: modes 99 and 100 were swapped (99 is Simple, 100 is Bypass and deprecated). Removed as unconfirmed by the cited pages: per-platform lists of common restrictions, supervised-only claims, settings catalog preference, client cmdlets and the Settings activity monitor path.
