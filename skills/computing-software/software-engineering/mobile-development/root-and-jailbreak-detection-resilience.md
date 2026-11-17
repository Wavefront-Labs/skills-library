---
id: computing-software.software-engineering.mobile-development.root-and-jailbreak-detection-resilience
name: root-and-jailbreak-detection-resilience
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, mobile-security, jailbreak-detection, root-detection, masvs-resilience, obfuscation, anti-tampering, risk-based]
level: advanced
status: draft
description: "Apply MASVS-RESILIENCE sensibly: what root and jailbreak checks can and cannot do, layered signals, server-side decisions, obfuscation and when not to bother."
sources: ["https://mas.owasp.org/MASVS/12-MASVS-RESILIENCE/", "https://mas.owasp.org/MASTG/", "https://developer.android.com/google/play/integrity"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Root and jailbreak detection (MASVS-RESILIENCE)

MASVS places resilience as an optional, risk-based layer for apps handling high-value assets (banking, DRM, games with real-money economies). It raises the cost of reverse engineering; it never replaces server-side controls.

## What clients can check
- Android: `su` binaries and Magisk artefacts, `ro.debuggable`/test-keys build tags, writable system partitions, installed root-manager packages, debugger attached (`Debug.isDebuggerConnected()`), emulator signs, hooking frameworks (Frida ports and libraries in `/proc/self/maps`).
- iOS: files such as `/Applications/Cydia.app` or `/bin/bash`, ability to write outside the sandbox, suspicious dylibs via `_dyld_image_count()`, `fork()` success, `ptrace` debugger flag.
- Integrity attestation is stronger: Play Integrity (device/app integrity verdicts) and Apple App Attest, verified on your server (see app-integrity skill).

## Design
1. Decide the threat model first: is a rooted user an attacker, or just a power user? Blocking all rooted devices harms legitimate people.
2. Combine several signals, score them, and act server-side (step-up auth, lower limits, deny high-risk actions) rather than only crashing locally.
3. Obfuscate and shrink release builds (R8 with a tuned `proguard-rules.pro`; Swift symbols stripped; commercial protectors if the risk justifies it).
4. Protect secrets by not shipping them; put keys in server-side flows or hardware-backed stores.
5. Test your own checks with Magisk (with DenyList), Frida and objection, as the MASTG describes.

## Gotchas
- Every client-side check can be hooked; a single boolean `isRooted()` is trivial to bypass.
- False positives from custom ROMs and OEM builds create support load; log and tune.
- Detection libraries add size and update burden.

Verify: on a rooted test device, confirm the app reports the expected signals to the server and the server enforces the chosen policy; then attempt a Frida hook of the check and record whether other signals still catch it.
