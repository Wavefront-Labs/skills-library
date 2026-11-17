---
id: computing-software.it-support-helpdesk.apple-device-management.vpn-per-app
name: vpn-per-app
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, wifi-vpn, vpn-per-app, vpn-payload, per-app-vpn]
level: practitioner
status: docs-checked
description: "Deploy the VPN payload and map a per-app VPN to an app with the Settings command ApplicationAttributes so only that app's traffic uses the tunnel."
sources:
  - "https://support.apple.com/guide/deployment/vpn-device-management-settings-overview-dep2d2adb35d/web"
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/profiles/com.apple.vpn.managed.yaml"
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/commands/settings.yaml"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vpn-per-app

Goal: tunnel only chosen app traffic.
- VPN payload `com.apple.vpn.managed` (macOS 10.7 or later, iOS 4 or later; more than one allowed). `VPNType` is one of VPN, L2TP, IPSec, IKEv2, AlwaysOn or TransparentProxy. For `VPNType` VPN, `VPNSubType` is required, and `VendorConfig` is only read when `VPNSubType` is set.
- `ProviderType`: `packet-tunnel` (default) or `app-proxy`, which tunnels traffic at the app level. `OnDemandEnabled` and `OnDemandRules` control on-demand connection. The `AlwaysOn` dictionary is iOS only.
- Mapping to an app: the Settings command `ApplicationAttributes` item has `Attributes.VPNUUID`, "a per-app VPN unique identifier for this app"; the same item has `ContentFilterUUID`, `DNSProxyUUID` and `RelayUUID`. It fails for apps managed by declarative device management.
- User Enrolment supports App-Layer VPN and App-to-App Layer VPN mapping only.
Practice: record which apps map to which VPN configuration, because replacing an app means the mapping must be applied again.
Gotcha: if the mapping command fails, check whether declarative device management manages that app.

## Checked

Date: 2026-11-07
Method: documentation only; no commands were run.
- Read in full: Apple Platform Deployment "VPN device management settings overview"; the apple/device-management YAML for `com.apple.vpn.managed`; the `ApplicationAttributes` section of the Settings command YAML (a search then read of that section, not the whole file).
- Removed as unconfirmed: "Always-On VPN needs supervision" (the payload definition shows no supervision requirement), "the app must be a managed app", "VPNUUID in the app's install settings" (the key is set through the Settings command), the DNS and proxy in the same profile advice, and the Verify steps.
- The original sources were developer.apple.com pages that render with JavaScript and could not be read, so they were replaced.
