---
id: computing-software.software-engineering.mobile-development.testing-against-owasp-masvs-and-mastg
name: testing-against-owasp-masvs-and-mastg
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, masvs, mastg, owasp, mobile-security-testing, mobsf, frida, security-assessment]
level: advanced
status: draft
description: "Assess a mobile app against OWASP MASVS using MASTG test cases: control groups, MAS profiles, static and dynamic tooling (MobSF, jadx, Frida, objection), and reporting."
sources: ["https://mas.owasp.org/MASVS/", "https://mas.owasp.org/MASTG/", "https://mas.owasp.org/checklists/", "https://github.com/MobSF/Mobile-Security-Framework-MobSF"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Testing against OWASP MASVS / MASTG

**Goal:** a structured, repeatable security assessment of an Android/iOS app with findings mapped
to an industry standard that developers, auditors and app-store programs recognise.

## The documents
- **MASVS** (Mobile Application Security Verification Standard) - *what* to verify. Version 2 control
  groups: `MASVS-STORAGE`, `MASVS-CRYPTO`, `MASVS-AUTH`, `MASVS-NETWORK`, `MASVS-PLATFORM`,
  `MASVS-CODE`, `MASVS-RESILIENCE`, `MASVS-PRIVACY`.
- **MASTG** (Mobile Application Security Testing Guide) - *how*: platform-specific tests,
  techniques and tools for each control.
- **MAS profiles**: L1 (baseline for all apps), L2 (defence in depth: banking, health), R
  (resilience against reverse engineering and tampering: apps protecting IP or high-value logic).
  Choose the profile from a threat model before testing.
- MASVS is also the basis for **ADA MASA** (App Defense Alliance) and Google Play's independent
  security review badge.

## Scope and setup
- Get the release build (IPA/APK/AAB) plus a debug build if allowed; test accounts; backend scope.
- Devices: a rooted Android (Magisk) and a jailbroken iOS device or Corellium; proxy (Burp Suite,
  mitmproxy) with its CA installed (user CA on Android needs a debug network-security-config or
  system install on rooted devices).

## Static analysis
- **MobSF**: automated first pass (manifest/Info.plist issues, hard-coded secrets, insecure APIs,
  exported components, ATS exceptions, binary protections).
- Decompile: `jadx-gui app.apk` (Java/Kotlin), `apktool d` (resources, smali); iOS: class-dump,
  Ghidra/Hopper on the decrypted binary.
- Check: secrets and API keys in code/resources, debug flags (`android:debuggable`), backup settings
  (`allowBackup`, data extraction rules), exported components without permissions, WebView settings,
  weak crypto (ECB, static IVs, MD5), logging of sensitive data, third-party SDK inventory.

## Dynamic analysis
- Traffic: all endpoints HTTPS, certificate validation (cannot MITM without your CA), pinning if
  claimed, no sensitive data in URLs, auth tokens expire/revoke server-side.
- Storage: inspect `/data/data/<pkg>/` (shared_prefs, databases, files) and the iOS app container /
  Keychain after use - no plaintext tokens, PII or cached sensitive responses; screenshots in the app
  switcher masked for sensitive screens.
- Runtime: **Frida** / **objection** to hook methods, bypass root/jailbreak detection and pinning
  (testing resilience controls), dump keychain, explore the heap.
- IPC: drive exported activities/receivers/providers with `adb shell am start -n`, `content query`;
  test deep links with malicious parameters.
- Auth: biometric bypass via hooking (is the crypto bound to the biometric prompt via
  `CryptoObject`/Keychain access control, or just a boolean?), session handling, OAuth redirect handling.

## Reporting
For each finding: MASVS control, MASTG test id, severity (CVSS or risk rating), evidence, affected
build, reproduction steps, remediation. Track the MAS checklist (spreadsheet from mas.owasp.org) with
pass/fail/NA per test for the chosen profile.

## Building it into development
- Automate the cheap parts: MobSF or similar SAST in CI, dependency scanning, secret scanning, lint
  rules (Android Lint security checks).
- Re-test high-risk areas on every major release; full assessment annually or on architecture change.

## Verify
- [ ] Profile (L1/L2/R) chosen from a threat model and documented.
- [ ] Every applicable MASVS control has a result with evidence.
- [ ] Findings retested after fixes; CI covers automatable checks.
