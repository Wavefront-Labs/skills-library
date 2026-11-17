---
id: computing-software.systems-network-administration.pki-tls-administration.gpo-mdm-trust-distribution
name: gpo-mdm-trust-distribution
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [gpo-mdm-trust-distribution, pki-trust-distribution, trust-distribution, gpo, intune, jamf, pki-tls-administration]
level: practitioner
status: draft
description: "Push a private root CA to managed endpoints using Group Policy, Intune and Jamf, and check devices that miss it."
sources:
  - https://learn.microsoft.com/en-us/mem/intune/protect/certificates-trusted-root
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Trust distribution via GPO and MDM
Goal: every managed device trusts the root without user action.
- GPO: Computer Configuration > Policies > Windows Settings > Security Settings > Public Key Policies > Trusted Root Certification Authorities > Import. For intermediates use Intermediate Certification Authorities.
- AD publishing: `certutil -dspublish -f root.crt RootCA` and autoenrolment puts the root in every domain member.
- Intune: Devices > Configuration > Create profile > Trusted certificate (upload .cer); assign to device groups; pair with SCEP/PKCS profiles that reference it.
- Jamf: Configuration profile with a Certificate payload set to trusted.
- Firefox uses its own store: policy `ImportEnterpriseRoots: true` on Windows/macOS.
- Android user-store CAs are ignored by many apps (since API 24); use MDM-managed certs for Chrome only.
- Distribute the CA before issuing leaves, and keep both old and new roots during rollover.
Gotcha: Browser and OS stores differ; mobile devices on BYOD without MDM will not trust the CA, so use a public CA for external users.
Verify:
- [ ] `certmgr.msc` or `security find-certificate` on a sample device shows the root.
- [ ] A report lists devices missing the profile.
