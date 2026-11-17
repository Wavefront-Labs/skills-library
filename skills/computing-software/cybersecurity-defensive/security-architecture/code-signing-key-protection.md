---
id: computing-software.cybersecurity-defensive.security-architecture.code-signing-key-protection
name: code-signing-key-protection
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [cryptography, code-signing, authenticode, signtool, hsm, timestamping, ev-code-signing, signing-service]
level: advanced
status: draft
description: "Run code signing safely: HSM-backed keys (now required for public certs), a central signing service, Authenticode with signtool and RFC 3161 timestamps, and compromise response."
sources: ["https://cabforum.org/working-groups/code-signing/documents/", "https://learn.microsoft.com/en-us/windows/win32/seccrypto/signtool", "https://learn.microsoft.com/en-us/azure/trusted-signing/overview"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Code signing key protection

A stolen code signing key lets attackers ship malware that your customers' and your own allowlists
trust (e.g. stolen certificates used in supply-chain attacks). Protect the key like a root CA.

## Key storage requirements
CA/Browser Forum Code Signing Baseline Requirements: since June 2023 private keys for publicly trusted
code signing certificates (OV and EV) must be generated and stored in FIPS 140-2 Level 2 / Common
Criteria EAL4+ hardware (HSM, hardware token, or cloud HSM-backed signing service).
Options: cloud KMS/HSM (Azure Key Vault Premium/Managed HSM, AWS CloudHSM, Google Cloud HSM),
Microsoft Trusted Signing (managed service), DigiCert KeyLocker/SSL.com eSigner.

## Central signing service
- Build pipelines submit hashes/artefacts to a signing service; developers never hold keys.
- Signing only from protected branches and release pipelines; approvals for release signing.
- Log every signature (who, what artefact hash, pipeline run) and alert on signing outside release windows.
- Separate test-signing certificates (internal CA) from release certificates.

## Authenticode with signtool
```
signtool sign /fd sha256 /tr http://timestamp.digicert.com /td sha256 /f <cert>.pfx /p <pw> app.exe   # dev/test only
signtool sign /fd sha256 /tr <tsa-url> /td sha256 /dlib Azure.CodeSigning.Dlib.dll /dmdf metadata.json app.exe   # cloud HSM
signtool verify /pa /v app.exe
```
- **Always timestamp** (RFC 3161 `/tr`): signatures then remain valid after the certificate expires.
  Without a timestamp, everything becomes untrusted at expiry.
- SHA-256 file digest and timestamp digest.
Other ecosystems: `codesign` + notarisation (Apple), `jarsigner`, GPG for packages, Sigstore/cosign
for containers.

## If a key is compromised
1. Revoke the certificate with the CA, choosing the revocation date to just before the earliest
   suspected misuse (signatures timestamped after that date become invalid; earlier ones stay valid).
2. Issue a new certificate (new key), re-sign and re-release current versions.
3. Find malicious binaries signed with your cert (VirusTotal retrohunt by signer, CA cooperation);
   notify customers; add hashes to EDR blocklists.

## Gotchas
- PFX files in build agents or repos are the classic leak; scan for them.
- Revoking without a careful date breaks every legitimately signed old release.
- Signing proves origin, not safety; signing malicious code from a compromised build pipeline is a
  supply-chain failure, which SLSA provenance and build isolation address.

## Verify
`signtool verify /pa /v` on a release shows a valid chain and timestamp; the signing service audit log
contains exactly the expected release signatures for the period.
