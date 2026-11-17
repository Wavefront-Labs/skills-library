---
id: computing-software.systems-network-administration.netbird.device-certificate-check
name: device-certificate-check
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, device-certificates, certificate-posture-check, tpm, pkcs11]
level: advanced
status: docs-checked
description: "Require device certificates from your CA with a NetBird Certificate posture check: prerequisites, setup, per-OS certificate locations, verification and failure messages."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/access-control/posture-checks/device-certificates.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Certificate check admits a peer only if it holds a certificate chaining to your CA and proves key possession by signing a management-server challenge, repeated every 4 hours.

Prerequisites: management and client 0.81.0+; CA PEM (root or intermediate); P-256/P-384 ECDSA or RSA 2048+ keys (Ed25519 also on Linux), usable without a prompt. Use a CA dedicated to device identities: the check does not bind to a user or hostname.

Setup: Access Control > Posture Checks > Create > enable Certificate; paste the CA PEM (add extra anchors for rotation); save; add the check to a policy's Posture Checks tab. Peers without a certificate fail, including all iOS and Android devices.

Locations:
- Windows: Local Computer Personal store, or profile owner's Personal store; TPM-backed keys work.
- macOS: System keychain needs key access for NetBird (MDM `AllowAllAppsAccess` true, or `security import -T <netbird binary>`).
- Linux: `.pem`/`.crt`/`.cer` in `/etc/netbird/certs` (or `NB_CERT_STORE_DIR`); root-owned, no symlinks, keys `chmod 600`. TPM via TSS2 key file or tpm2-pkcs11 (`NB_CERT_PKCS11_URI`, `NB_TPM_PIN`); never pass the PIN via `--service-env`.

Verify: `netbird debug log level debug` and read the client log. Failures: "matched none of the candidates" (missing intermediate), "store holds no candidates", `CFError -25308` (macOS key access), "rejected the PIN". Failing devices retry every 5 minutes.

## Checked

2026-11-04. Confirmed against the NetBird device certificates page: 4-hour challenge, 0.81.0 requirement, key types, CA dedicated warning, setup steps, mobile failure, per-OS locations, macOS AllowAllAppsAccess and `security import -T`, Linux certs directory and permissions, TPM options, PIN warning, log messages, 5-minute retry. Nothing removed.
Method: documentation only; no commands were run.
