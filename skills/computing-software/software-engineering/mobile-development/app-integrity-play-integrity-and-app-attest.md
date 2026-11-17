---
id: computing-software.software-engineering.mobile-development.app-integrity-play-integrity-and-app-attest
name: app-integrity-play-integrity-and-app-attest
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, mobile-security, play-integrity, app-attest, devicecheck, anti-tampering, api-abuse]
level: practitioner
status: gated
description: "Verify requests come from your genuine app on a genuine device with Play Integrity API and Apple App Attest, server-side verification, nonces, and sensible enforcement."
sources:
  - https://developer.android.com/google/play/integrity/overview
  - https://developer.android.com/google/play/integrity/verdicts
  - https://developer.apple.com/documentation/devicecheck/establishing-your-app-s-integrity
  - https://developer.apple.com/documentation/devicecheck/validating-apps-that-connect-to-your-server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# App integrity: Play Integrity and App Attest

**Goal:** make it expensive to abuse your backend with modified apps, emulators, scripts or bots, by verifying platform-signed attestations on the server.

## 1. What they prove (and do not)
- **Play Integrity**: the request comes from your app binary (recognised by Play), installed from Play, on a device passing integrity checks, optionally with a licensed user. Verdicts are signed by Google.
- **App Attest**: a key generated on the device is bound to your app's identity on a genuine Apple device; each request can carry an assertion signed by that key. (gated: unconfirmed, source is paywalled or blocked)
- Neither proves the **user** is honest or that the device is not automated by a real phone farm. They are risk signals, not authentication.

## 2. Play Integrity flow
1. Server issues a one-time nonce (or for standard requests, the app binds a hash of the request: `requestHash`).
2. App requests a token:
```kotlin
val manager = IntegrityManagerFactory.createStandard(context)
val provider = manager.prepareIntegrityToken(PrepareIntegrityTokenRequest.builder().setCloudProjectNumber(PROJECT).build()).await()
val token = provider.request(StandardIntegrityTokenRequest.builder().setRequestHash(sha256(body)).build()).await().token()
```
3. Server decodes it via Google's `decodeIntegrityToken` API (never on the device), and checks: `requestDetails.requestHash` matches, `appIntegrity.appRecognitionVerdict == PLAY_RECOGNIZED`, package name and certificate digest, `deviceIntegrity.deviceRecognitionVerdict` contains `MEETS_DEVICE_INTEGRITY` (or `MEETS_STRONG_INTEGRITY` for high-risk actions), `accountDetails.appLicensingVerdict`, and timestamp freshness.
Quotas apply (default 10,000 requests/day per app, increasable); use standard requests (prepared provider) for frequent calls.

## 3. App Attest flow
```swift
let service = DCAppAttestService.shared
guard service.isSupported else { /* fallback: DeviceCheck or risk-based */ return }
let keyId = try await service.generateKey()
let clientDataHash = Data(SHA256.hash(data: serverChallenge))
let attestation = try await service.attestKey(keyId, clientDataHash: clientDataHash)
// send keyId + attestation to server once; server validates the certificate chain to Apple's App Attest root,
// checks the app ID (TeamID.bundleID) and counter, stores the public key
let assertion = try await service.generateAssertion(keyId, clientDataHash: Data(SHA256.hash(data: requestBody)))
// per request: server verifies the signature with the stored key and that the counter increased
```
Use the `development` vs `production` environment entitlement correctly; App Attest is unavailable on simulators and some older devices.

## 4. Enforcement strategy
- Start in **monitor mode**: log verdicts, measure false negatives (rooted power users, custom ROMs, old devices).
- Gate sensitive actions (account creation, payouts, promo redemption, high-value API endpoints) rather than every request.
- Combine with rate limiting, device/account reputation and server-side anomaly detection.
- Fail with a user-friendly path (update the app, use the website), not silent breakage.

## Gotchas
- Client-side checks (root detection libraries, jailbreak checks) are bypassable; only server-verified attestations carry weight.
- Do not cache a single token for reuse; bind tokens to requests (nonce/request hash) to prevent replay.
- Sideloaded builds (enterprise, internal testing outside Play) fail app recognition; configure test tracks and allowlists.
- Key loss on iOS (app reinstall, device restore) requires re-attestation; handle unknown key IDs gracefully.

## Checked
2026-10-31. Confirmed on the Play Integrity overview and verdicts pages: default 10,000 requests per day across all installs (increase on request), `decodeIntegrityToken`, `PLAY_RECOGNIZED`, `LICENSED`, `MEETS_DEVICE_INTEGRITY` and `MEETS_STRONG_INTEGRITY`. Removed the iOS 14+ and Secure Enclave specifics. The Apple App Attest documentation pages are JavaScript-only and unreadable, so the App Attest flow and code are gated.
Method: documentation only; no commands were run.

## Verify
- Server logs show verdict distributions in monitor mode; a re-signed APK and an emulator are flagged; replaying a captured token or assertion is rejected.
