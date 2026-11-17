---
id: computing-software.cybersecurity-defensive.network-defence.enterprise-browser-security-policy
name: enterprise-browser-security-policy
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [web-filtering, browser-security-policy, chrome-enterprise-policies, edge-policies, extension-allowlist, smartscreen, safe-browsing, browser-updates, cis-browser-benchmarks]
level: practitioner
status: draft
description: "Harden managed Chrome and Edge with policy: extension allowlisting, Safe Browsing/SmartScreen enforcement, update control, password and download settings."
sources: ["CIS Control 9.1, 9.4 (supported browsers, restrict unnecessary extensions)", "CIS Google Chrome and Microsoft Edge Benchmarks", "Chrome Enterprise policy list and Microsoft Edge policy reference"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Enterprise browser security policy

**Goal:** the browser, where most work and most attacks happen, runs current, with only
approved extensions and with built-in protections that users cannot switch off.

## Key policies (Chrome name / Edge name where different)
| Area | Setting |
|---|---|
| Extensions | `ExtensionInstallBlocklist = *` then `ExtensionInstallAllowlist` with approved IDs; or `ExtensionSettings` JSON to also block by permission (e.g. block extensions requesting `<all_urls>` unless allowed) |
| Safe Browsing | `SafeBrowsingProtectionLevel = 1` (standard) or 2 (enhanced); Edge `SmartScreenEnabled = 1`, `PreventSmartScreenPromptOverride = 1`, `SmartScreenPuaEnabled = 1` |
| Downloads | `DownloadRestrictions = 1` (block dangerous) or 4 (malicious) |
| Updates | Do not disable auto-update; Edge/Chrome update policies to allow; monitor version compliance |
| Passwords | `PasswordManagerEnabled = false` if an enterprise password manager is used |
| Sign-in and sync | Restrict sync to corporate accounts (`RestrictSigninToPattern`, Edge `RestrictSigninToPattern`), block profile mixing if needed |
| Developer tools | `DeveloperToolsAvailability = 2` for non-developers (limits some malicious extension and session theft techniques) |
| Insecure content | Block mixed content; `HttpsOnlyMode = force_enabled` where feasible |
| Remote debugging | `RemoteDebuggingAllowed = false` (blocks cookie theft via debug port) |

Deploy via Intune settings catalog, GPO ADMX templates, or Chrome Enterprise Core (cloud).
Verify on a client at `chrome://policy` / `edge://policy`.

## Extension governance
- Inventory installed extensions (Chrome Enterprise reporting, Edge management service, EDR).
- Review requests: publisher, permissions, update history, ownership changes (extensions are sold to malicious buyers).
- Remove extensions whose ownership or permissions change unexpectedly.

## Gotchas
- Users with local admin can run other browsers; control which browsers are allowed (application control) or manage all.
- Blocking all extensions without an allow process drives users to unmanaged browsers.
- Session cookies stolen by infostealers bypass MFA; combine with token protection and short session lifetimes.

## Verify
- [ ] `chrome://policy` on sample machines shows policies applied with status OK.
- [ ] Extension inventory shows only allowlisted IDs.
