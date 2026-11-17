---
id: computing-software.cybersecurity-defensive.threat-modelling.mobile-app-threat-modelling
name: mobile-app-threat-modelling
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [threat-modelling, mobile-threat-modelling, owasp-masvs, mobile-security, android, ios, api-backend]
level: practitioner
status: docs-checked
description: "Threat model mobile apps by walking the eight OWASP MASVS groups: storage, crypto, auth, network, platform, code, resilience and privacy."
sources: ["https://raw.githubusercontent.com/OWASP/owasp-masvs/master/OWASP_MASVS.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mobile app threat modelling

**Goal:** design mobile apps assuming an attacker can have physical access to the device and run a modified copy of the app, with the remote endpoint as the place authentication and authorisation are enforced.

## Model elements
App process, local storage (internal and public locations, backups, logs), IPC mechanisms, WebViews, the user interface (screenshots, notifications), third-party SDKs and libraries, and the remote endpoint. Draw trust boundaries between device and backend, app and other installed apps, and app and SDKs.

## Threats by MASVS group
- **MASVS-STORAGE (1, 2):** sensitive data stored insecurely, or leaked unintentionally through APIs, backups or logs, including into public folders other apps can read.
- **MASVS-CRYPTO (1, 2):** outdated cryptography, poor key management across generation, storage and protection. MASVS points to NIST SP 800-175B and SP 800-57.
- **MASVS-AUTH (1, 2, 3):** weak protocol use; enforcement must be on the remote endpoint. Local authentication (biometrics, PIN) implemented incorrectly; sensitive operations without additional authentication.
- **MASVS-NETWORK (1, 2):** platform TLS defaults disabled or bypassed through low-level APIs or third-party libraries; no pinning of endpoints under the developer's control.
- **MASVS-PLATFORM (1, 2, 3):** IPC exposed insecurely; WebViews leaking data or exposing native functionality via JavaScript bridges; sensitive data shown in auto-generated screenshots, notifications or by shoulder surfing.
- **MASVS-CODE (1 to 4):** old platform versions supported, no way to force app updates, components with known vulnerabilities, untrusted input from the UI, IPC, network or file system not validated.
- **MASVS-RESILIENCE (1 to 4):** tampered platform, modified or repackaged app, static analysis, dynamic analysis and instrumentation. MASVS says missing resilience measures are not by themselves vulnerabilities; they add threat-specific protection.
- **MASVS-PRIVACY (1 to 4):** collecting more data than needed, SDKs collecting before consent, user identification and fingerprint-like signals reused across purposes, undisclosed collection, no user control over their data.

## Gotchas
- Server-side behaviour is out of scope for MASVS; verify the backend separately (MASVS points to OWASP ASVS).
- MASVS-PRIVACY is a baseline, not a substitute for a DPIA or legal assessment.

## Output
Register of threats per MASVS group with the affected component, the control id, and a decision to mitigate or accept (resilience controls are chosen by the app's own threat model).

## Checked
Method: 2026-11-09 read OWASP_MASVS.yaml (raw GitHub, OWASP/owasp-masvs) in full and kept only its group and control content. Removed as unconfirmed here: keystore and keychain hardware backing, OAuth PKCE, `android:exported`, App Links and Universal Links, Network Security Config and ATS, Play Integrity and App Attest, Frida, MobSF, rotation of pinned certificates, root and jailbreak detection claims, and the MASTG and Mobile Top 10 sources (not read).
