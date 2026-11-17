---
id: computing-software.software-engineering.mobile-development.certificate-pinning-and-network-security-config
name: certificate-pinning-and-network-security-config
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, mobile-security, certificate-pinning, network-security-config, public-key-pinning, okhttp-certificatepinner, nspinneddomains, app-transport-security, tls, android, ios]
level: advanced
status: docs-checked
description: "Decide whether to pin, then pin TLS public keys safely on Android (network security config) and iOS (NSPinnedDomains), with backup pins and expiry to avoid bricking."
sources: ["https://developer.android.com/privacy-and-security/security-config", "https://developer.apple.com/news/?id=g9ejcf8y", "https://mas.owasp.org/MASTG/knowledge/android/MASVS-NETWORK/MASTG-KNOW-0015/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Certificate pinning and network security config

**Goal:** stop man-in-the-middle interception by rogue CAs where the threat model justifies it, without locking every
user out on the next certificate rotation.

## Should you pin?
Apple: pinning is not required and in most cases should be avoided; the system already evaluates server trust, and
pinning can only tighten trust, never loosen it. If the server's public keys change, the app refuses to connect until
you ship an updated pinning configuration. Typical valid reason: regulatory requirements naming which CAs may be
trusted. OWASP calls pinning a hardening practice that is not foolproof (an attacker can modify validation logic,
replace pinned certificates in `res/raw` or `assets`, or alter the pins, then repackage and re-sign the APK).

## Pin public keys, with a backup
Pins are the base64 SHA-256 digest of the X.509 SubjectPublicKeyInfo (SPKI). Apple's example for a PEM certificate:
```bash
cat ca.pem | openssl x509 -inform pem -noout -outform pem -pubkey | openssl pkey -pubin -inform pem -outform der | openssl dgst -sha256 -binary | openssl enc -base64
```
- Always include a backup key so a forced key or CA change does not break connectivity (otherwise you must push an
  app update).
- Pinning a CA's public key (intermediate or root) instead of the server's lets you deploy new server keys signed by
  the same CA without a config update. Pinning several keys covers revoked or rotated certificates.
- Plan a fallback experience and a recovery path, and test with extra certificates and varied server setups.

## Android: network security configuration
Point the manifest at the file: `<application android:networkSecurityConfig="@xml/network_security_config">`.
```xml
<network-security-config>
  <domain-config>
    <domain includeSubdomains="true">example.com</domain>
    <pin-set expiration="2030-01-01">
      <pin digest="SHA-256">7HIpactkIAq2Y49orFOOQKurWxmmSFZhBCoQYcRhJ3Y=</pin>
      <!-- backup pin -->
      <pin digest="SHA-256">fwza0LRMXouZHRC8Ei+4PyuldPDcf3UKgO/04cDM1oE=</pin>
    </pin-set>
  </domain-config>
</network-security-config>
```
- A chain is valid if it contains at least one pinned key. Only `SHA-256` digests are supported.
- `expiration` (`yyyy-MM-dd`) turns pinning off after that date, which helps apps that never update, but Android notes
  it may let attackers bypass your pins.
- `includeSubdomains="true"` matches the domain and all subdomains; with several matching `domain-config` elements the
  most specific (longest) domain rule wins.
- `<debug-overrides>` applies only when `android:debuggable` is true; its trust anchors are added to all other configs
  and pinning is not performed for chains using them. Stores do not accept debuggable apps.
- `cleartextTrafficPermitted` defaults to false for apps targeting Android 9 (API level 28) and higher.
- By default apps trust the system CAs; apps targeting API level 23 and lower also trust user-added CAs.
- The NSC applies to traffic handled by the Android framework (`HttpsURLConnection`, WebView) but not native code.
  OkHttp's `CertificatePinner` is a code-level alternative built on a custom TrustManager. Do not write a trust-all
  TrustManager, and verify hostnames manually with a safe `HostnameVerifier` if you build your own.
- Cross-platform frameworks (Flutter, Cordova and others) may not use the platform stack, so pinning needs separate
  handling.

## iOS: NSPinnedDomains
In Info.plist, `NSAppTransportSecurity` > `NSPinnedDomains` > the domain, with `NSPinnedCAIdentities` (CA keys; must
appear in an intermediate or root of the chain) or `NSPinnedLeafIdentities` (server keys), each an array of
dictionaries with `SPKI-SHA256-BASE64`. `NSIncludesSubdomains` true covers direct subdomains such as
`math.example.org`, but not deeper ones such as `advanced.math.example.org`.

## Verify
- [ ] With an interception proxy's CA installed, release builds refuse connections.
- [ ] A backup pin is present and a rotation runbook is documented.

## Checked
2026-11-08. Confirmed against the Android Developers Network security configuration page, Apple's news article Identity Pinning and OWASP MASTG-KNOW-0015: pinning advice, backup pins, expiration semantics, debug-overrides, defaults, NSPinnedDomains keys and subdomain rule, openssl pipeline, NSC scope. Removed: OkHttp CertificatePinner API page (404) and its code details, iOS 14 version gate, URLSessionDelegate and TrustKit advice, Frida and kill-switch remarks, the MASVS L2 claim, the live-server openssl pipeline, and the example pin dates.
Method: documentation only; no commands were run.
