---
id: computing-software.systems-network-administration.pki-tls-administration.code-signing-key-protection
name: code-signing-key-protection
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [code-signing-key-protection, pki-codesign, code-signing, authenticode, hsm-key-storage, timestamp, pki-tls-administration]
level: practitioner
status: draft
description: "Operate code signing: key in HSM or cloud signing, timestamping, CI integration and certificate renewal."
sources:
  - https://cabforum.org/working-groups/code-signing/documents/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Code signing certificates and key protection
Goal: signed builds without exposing the signing key.
- Public code signing keys must be on FIPS 140-2 Level 2 / EAL 4+ hardware or a cloud HSM service (CA/B Code Signing BRs since 2023; confirm).
- Options: vendor HSM token, Azure Trusted Signing / Key Vault, AWS Signer, Google Cloud KMS, or DigiCert KeyLocker.
- Sign with timestamp so signatures stay valid after cert expiry:
```
signtool sign /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 /sha1 <thumb> app.exe
osslsigncode sign -certs c.pem -key k.pem -h sha256 -ts http://timestamp.digicert.com -in app.exe -out app-signed.exe
```
- CI: use OIDC-based short-lived access to the signing service; restrict to protected branches and require approval.
- Separate keys for test and release; Authenticode, Java (jarsigner), macOS notarisation and Linux GPG/cosign each have their own flows.
Gotcha: no timestamp means every signature dies with the certificate, forcing a rebuild and re-release.
Verify:
- [ ] `signtool verify /pa /v app.exe` shows a valid timestamp.
- [ ] Signing key export attempt fails.
