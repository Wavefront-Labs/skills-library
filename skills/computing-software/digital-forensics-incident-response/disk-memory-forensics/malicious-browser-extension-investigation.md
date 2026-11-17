---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.malicious-browser-extension-investigation
name: malicious-browser-extension-investigation
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [browser-extensions, browser-forensics, chrome-forensics, persistence, dfir]
level: advanced
status: draft
description: "Investigate malicious or hijacked browser extensions: inventory from profiles and policy, manifest permissions, install source, code review and data theft scope."
sources: ["https://developer.chrome.com/docs/extensions/reference/manifest", "https://support.google.com/chrome/a/answer/7532015", "https://attack.mitre.org/techniques/T1176/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Malicious browser extension investigation

**Goal:** extensions can read every page, steal cookies and session tokens, inject scripts and
persist through reboots (ATT&CK T1176). Supply-chain hijacks of popular extensions affect whole fleets.

## Inventory
- Chromium: `<Profile>\Extensions\<extension-id>\<version>\manifest.json`; `Preferences` and
  `Secure Preferences` (`extensions.settings`) record install time (`install_time`, WebKit epoch),
  `from_webstore`, `location` (1 = Web Store, 4 = unpacked/command line, 5 = policy) and granted permissions.
- Firefox: `<profile>\extensions.json`, `extensions\*.xpi`, `addonStartup.json.lz4`.
- Enterprise: policy force-installs `ExtensionInstallForcelist` (registry `HKLM\SOFTWARE\Policies\Google\Chrome`);
  malware abuses this to install extensions that users cannot remove.
- Fleet: Velociraptor `Windows.Applications.Chrome.Extensions` / osquery `chrome_extensions` table.

## Triage an extension
- Permissions in manifest: `<all_urls>`, `cookies`, `webRequest`, `scripting`, `nativeMessaging`, `debugger` = high risk.
- `location` 4 (sideloaded via `--load-extension` in a modified shortcut) is a strong malicious indicator; check LNK target arguments.
- Review JS: obfuscated code, `chrome.cookies.getAll`, remote config fetches, exfil endpoints.
- Compare version history: hijacked updates appear as a new version on a date; check Web Store / CRX hash.

## Scope impact
- Which users/hosts had it, which versions, during what window.
- Data at risk: session cookies (rotate sessions for SaaS), credentials typed, page content.
- Proxy/DNS logs for exfil domains from the extension code.

## Remediate
Block by ID (`ExtensionInstallBlocklist`), remove forcelist entries, revoke sessions for affected users.

## Gotchas
- Extension folders remain after uninstall sometimes; confirm active state in Preferences.
- Chromium `Secure Preferences` MAC protects settings; malware edits are detectable by MAC mismatch reset messages.

## Verify
Every host with the extension ID is identified, and sessions for affected SaaS accounts were revoked.
