---
id: computing-software.systems-network-administration.pki-tls-administration.adcs-ndes-scep
name: adcs-ndes-scep
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [adcs-ndes-scep, pki-adcs-enrol, adcs, ndes, scep, intune-connector, pki-tls-administration]
level: practitioner
status: draft
description: "Install NDES, configure its service account, templates and challenge password policy, and secure it behind a reverse proxy."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/network-device-enrollment-service-guidance
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NDES for SCEP enrolment
Goal: SCEP certificate enrolment for routers, MDM and non-domain devices.
1. Dedicated service account (gMSA or user) in IIS_IUSRS, with SPN and local logon-as-service rights.
2. `Install-AdcsNetworkDeviceEnrollmentService -ServiceAccountName DOMAIN\ndes-svc -RAName "NDES-RA" -CAConfig "ca.example.com\Issuing CA"`.
3. Registry `HKLM\SOFTWARE\Microsoft\Cryptography\MSCEP`: set EncryptionTemplate, GeneralPurposeTemplate and SignatureTemplate to a template name (default IPSECIntermediateOffline).
4. Template security: NDES account has Enroll; subject "Supply in the request"; remove Enroll from users.
5. Challenge: `http://ndes/certsrv/mscep_admin` (one-time, 60 minutes). Disable the password requirement only in a lab.
6. Publish via reverse proxy with TLS; restrict `/mscep/` and `/mscep_admin/`.
Intune: use the Microsoft Intune Certificate Connector and Azure AD App Proxy rather than exposing NDES.
Gotcha: SCEP encrypts only the CSR; treat the challenge as a secret and keep short validity.
Verify:
- [ ] `https://ndes/certsrv/mscep/mscep.dll` shows the NDES page.
- [ ] A test device enrols and the template appears in the issued cert.
