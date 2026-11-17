---
id: computing-software.cybersecurity-defensive.security-architecture.device-trust-signals
name: device-trust-signals
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [zero-trust, device-trust, device-posture, conditional-access, mdm-compliance, certificate-based-device-identity, ztna]
level: advanced
status: draft
description: "Use device trust in zero-trust access decisions: device identity via certificates or MDM, posture signals (EDR, patch, encryption), conditional access enforcement and gaps."
sources: ["https://csrc.nist.gov/pubs/sp/800/207/final", "https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-conditional-access-grant", "https://www.cisa.gov/zero-trust-maturity-model"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Device trust signals

**Goal:** access decisions consider not just who the user is but whether the device is
known, managed and healthy (NIST SP 800-207 tenet: asset state informs access; CISA ZTMM
Devices pillar).

## 1. Device identity
- **Managed device registration:** Entra hybrid join / Entra join, Intune or Jamf enrolment,
  Google endpoint management. Gives a device ID the IdP can check.
- **Device certificates:** issued via MDM (SCEP/PKCS) with private key in TPM/Secure Enclave;
  used for 802.1X, VPN/ZTNA client auth, and mTLS to proxies. Hard to copy to another device.
- Avoid relying on IP address or user agent as device identity.

## 2. Posture signals
- MDM compliance: OS version minimum, disk encryption (BitLocker/FileVault), screen lock,
  jailbreak/root detection, firewall on.
- EDR health and risk: agent running, up to date, machine risk score (Defender for
  Endpoint risk level feeds Intune compliance; CrowdStrike ZTA score to Okta/Zscaler).
- Patch level: within N days of current.
- Signals must be fresh: compliance evaluated recently (check-in within hours/days).

## 3. Enforce
- **Conditional access** (Entra): grant control "Require device to be marked as compliant"
  or "Require Microsoft Entra hybrid joined device" for sensitive apps; Okta Device Assurance
  policies; Google context-aware access levels.
- **ZTNA/SSE:** device posture checks before granting app access (Zscaler, Cloudflare
  Access, Netskope).
- Tiered: unmanaged devices get browser-only, no download (app-enforced restrictions /
  session controls via CASB); managed compliant get full access.

## Gaps to plan for
- BYOD: app protection policies (MAM) instead of device compliance.
- Linux workstations and developer machines: limited MDM posture; use device certificates
  plus EDR signals.
- Servers and workloads: workload identity, not user-device CA.
- Break-glass accounts excluded from device requirements (with monitoring).

## Gotchas
- Report-only mode first: compliance policies misconfigured block whole departments.
- Compliance grace periods let a non-compliant device keep access for days; set deliberately.
- Device compliance tokens can be stolen with the session (token theft); pair with token
  protection/binding where available.

## Verify
Sign in to a protected app from an unmanaged device and from a compliant device; the first is
blocked or limited, the second allowed. Sign-in logs show the device compliance evaluation.
