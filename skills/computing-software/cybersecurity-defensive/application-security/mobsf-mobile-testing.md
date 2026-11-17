---
id: computing-software.cybersecurity-defensive.application-security.mobsf-mobile-testing
name: mobsf-mobile-testing
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [mobsf, mobile-app-security, android, ios, masvs, static-analysis, mobile-security-testing]
level: practitioner
status: draft
description: "Test your own Android and iOS builds with MobSF: static analysis of APK/IPA, reading the report against MASVS, dynamic analysis setup, REST API and CI integration."
sources: ["https://mobsf.github.io/docs/", "https://github.com/MobSF/Mobile-Security-Framework-MobSF", "https://mas.owasp.org/MASVS/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mobile app testing with MobSF

Mobile Security Framework (MobSF) is an open-source automated analyser for Android (APK, AAB, source zip) and
iOS (IPA, source zip) apps. Use it on your own builds to catch insecure configuration and code patterns before
release and to give pentesters a head start.

## Run it
```bash
docker run -it --rm -p 8000:8000 opensecurity/mobile-security-framework-mobsf:latest
```
Open http://localhost:8000 and upload the build (default web credentials are documented; change them if the
instance is shared). Static analysis takes a few minutes.

## Reading the static report
- **Security score** and findings mapped to OWASP MASVS and CWE.
- **Manifest analysis (Android)**: `android:debuggable="true"`, `allowBackup="true"`, cleartext traffic
  permitted (`usesCleartextTraffic`, network security config), exported activities/services/receivers/
  providers without permission, low `minSdkVersion`.
- **iOS Info.plist / ATS**: `NSAllowsArbitraryLoads`, missing binary protections (PIE, stack canaries, ARC).
- **Code analysis**: hard-coded secrets and API keys, insecure random, weak crypto (ECB, MD5), WebView
  `setJavaScriptEnabled` with `addJavascriptInterface`, logging of sensitive data, SQL string building,
  disabled certificate validation.
- **Permissions**: dangerous permissions not needed by features.
- **Libraries and trackers**: third-party SDKs and known trackers (privacy review input).
- **Certificate**: debug-signed builds, signature scheme versions.

Triage like SAST: many hits are in third-party libraries; focus on your package namespace first.

## Dynamic analysis
Requires a rooted Android emulator (Genymotion or Android Studio AVD supported per docs) or a jailbroken/
Corellium iOS device. MobSF installs the app, instruments with Frida, captures traffic, logs, and lets you run
Frida scripts (SSL pinning bypass for testing your own app, API monitoring). Useful to confirm data stored on
device and what the app transmits.

## CI integration
REST API (API key shown in the UI / `MOBSF_API_KEY`): `POST /api/v1/upload`, `POST /api/v1/scan`,
`POST /api/v1/report_json`, and `POST /api/v1/scorecard`. Fail the build on new high findings; mobsfscan
(separate CLI, SARIF output) runs on source in PRs.

## Gotchas
- Automated findings are not a pentest; business logic and backend API flaws need separate testing.
- Obfuscated release builds reduce code findings; scan the release build anyway for manifest and binary
  checks, and the debug build for code.

## Verify
Release build report has no high findings in your own code, manifest shows debuggable false and no cleartext,
and the CI job archives the JSON report per build.
