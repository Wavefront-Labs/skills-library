---
id: computing-software.it-support-helpdesk.desktop-support.browser-security-settings-and-extensions
name: browser-security-settings-and-extensions
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, workstation-security, browser-security, extension-allowlist, smartscreen, edge-policies]
level: practitioner
status: docs-checked
description: "Secure Microsoft Edge on managed devices: extension block and allow lists, force-install, ExtensionSettings permission and host blocks, and Defender SmartScreen behaviour."
sources:
  - "https://learn.microsoft.com/en-us/deployedge/microsoft-edge-manage-extensions-policies"
  - "https://learn.microsoft.com/en-us/deployedge/microsoft-edge-security-smartscreen"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# browser-security-settings-and-extensions

Goal: configure the browser centrally (Edge covered here) and clean up when a user's browser has been hijacked.

## Extension control (Edge group policy)
Group Policy path: Administrative Templates > Microsoft Edge > Extensions.
- **Block list**: "Control which extensions cannot be installed" (`ExtensionInstallBlocklist`). Enter app IDs, one
  per row; type `*` to block everything and pair it with "Allow specific extensions to be installed"
  (`ExtensionInstallAllowlist`) to build an allow-list. Blocking an already installed extension disables it and the
  user cannot re-enable it; it is not uninstalled. The app ID is at the end of the extension's Edge Add-ons URL.
- **Force install**: "Control which extensions are installed silently" (`ExtensionInstallForcelist`). Installed
  without interaction; the user cannot uninstall or disable it; it overrides any blocklist. Entries are
  `extension_id;update_url`.
- **ExtensionSettings** ("Configure extension management settings", a compressed JSON string):
  - `blocked_permissions` blocks extensions needing a permission (for example `"usb"`); an extension needing a
    blocked permission is disabled, not removed. `*` as the ID applies to all; a specific ID applies only to it.
  - `runtime_blocked_hosts` / `runtime_allowed_hosts` stop or allow extensions reading or changing named sites; this
    does not stop users installing extensions.
  - Block a whole store by setting `installation_mode` to `blocked` for its `update_url`; the force and allow lists
    still work for specific extensions.

## SmartScreen in Edge
- Microsoft Defender SmartScreen is on by default in Edge; users can turn it off at edge://settings/privacy
  unless Group Policy or MDM prevents it.
- It warns on malicious or unknown sites and downloads (reputation based on download traffic, history, past
  anti-virus results and URL reputation). Known-safe files download without a warning.
- By default users can bypass warnings; Microsoft recommends reviewing the recommended group policy settings that
  restrict this. See the SmartScreen settings page for the exact policy names.

## Cleaning a hijacked browser
Symptoms: search engine changed, redirects, notification spam, new toolbar.
1. Remove unknown extensions.
2. Reset browser settings to defaults.
3. Remove spammy site notification permissions.
4. On an unmanaged machine, unexpected organisation policies mean something wrote policies: remove and scan.
5. Scan the device (malware procedure).

## Gotchas
- Allow-list-only policies generate requests; publish a request process.
- Install software and extensions only from the official store or vendor site.

## Verify
A test unapproved extension is blocked and SmartScreen warns on the Microsoft demo site.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed on the Edge extensions policy and SmartScreen pages. The Chrome admin help landing page returned a stub,
so Chrome policy names were removed. Also removed as not on the cited pages: other Edge policy names
(`PreventSmartScreenPromptOverride`, `RestrictSigninToPattern` etc.), update-channel, download-blocking and
password-manager advice, and the certificate guidance.
