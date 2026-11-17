---
id: computing-software.it-support-helpdesk.intune-mdm.scep-and-pkcs-certificate-profiles
name: scep-and-pkcs-certificate-profiles
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, scep-certificate-profile, pkcs-certificate, trusted-certificate, ndes, cloud-pki, configuration-profile, wifi-8021x]
level: advanced
status: docs-checked
description: "Deploy device and user certificates with Intune: trusted root, SCEP via NDES or Cloud PKI, PKCS with the certificate connector, subject/SAN variables, and failed-issuance fixes."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/protect/certificates-configure"
  - "https://learn.microsoft.com/en-us/mem/intune/protect/certificates-profile-scep"
  - "https://learn.microsoft.com/en-us/mem/intune/protect/microsoft-cloud-pki-overview"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# scep-and-pkcs-certificate-profiles

Certificates authenticate 802.1X Wi-Fi, VPN and other resources, and sign or encrypt S/MIME email. A failure shows up to the
user as "can't connect to corporate Wi-Fi".

## Pieces
1. **Trusted certificate profile**: deploys the root (or intermediate) CA certificate. Required before SCEP or PKCS profiles;
   deploy it to the same devices and users that get the certificate profile.
2. **SCEP**: each certificate is unique per request and tied to the requesting user or device; it works for user-less devices
   such as kiosks. With a Microsoft CA you need an NDES server and the Certificate Connector for Microsoft Intune. A
   third-party CA's SCEP does not need the connector (set up the partner integration plus an Entra app for challenge
   validation). **Microsoft Cloud PKI** replaces the on-premises CA, NDES and connector; it needs a subscription in addition
   to Intune Plan 1 or 2, and the private key is created on the device and never leaves it.
3. **PKCS**: needs the Certificate Connector. Each device gets a unique certificate. A user-type template always needs user
   affinity (a user-less device gets no certificate); a device-type template does not. With a third-party CA, PKCS is only
   supported with the DigiCert PKI Platform.
4. **PKCS imported**: one certificate exported from a source (such as an email server) deployed to many users or devices,
   for S/MIME signing and decryption. Needs the connector and the PFXImport PowerShell project.

Each certificate profile supports a single platform, so create one per platform.

## SCEP profile key fields (Windows focus)
- Deployment channel: user channel for user certificates, device channel for device certificates; it cannot be edited
  after the profile is deployed.
- Certificate type: User (user and device attributes in subject and SAN) or Device (device attributes only). Use Device for
  user-less devices and Windows machine certificates (placed in the Local Computer store).
- Subject name format: variables go in double curly brackets, for example `CN={{UserPrincipalName}}` (user) or
  `CN={{AAD_Device_ID}}` (device). Avoid `{{DeviceId}}` on Windows, where it can cause Intune sync to fail. Names over 64
  characters may need DN length enforcement disabled on the CA.
- SAN attributes: Email, UPN, DNS, URI. A client certificate used against Network Policy Server: set the SAN to the UPN.
- Validity: you can enter a value lower than the template validity, never higher; Intune supports up to 24 months; plan for
  five days or more.
- Key storage provider (Windows): TPM if present otherwise software; TPM or fail; Windows Hello for Business or fail;
  Software. 4096-bit keys are Software KSP only on Windows.
- Key usage: Digital signature and Key encipherment. Extended key usage: usually client authentication.
- Root certificate: the trusted certificate profile (for a multi-level PKI, the top-level root profile).
- Renewal threshold (%): for 20, renewal is attempted at 80% of lifetime elapsed.
- SCEP server URL: external NDES URL for internet devices, for example `https://ndes.contoso.com/certsrv/mscep/mscep.dll`;
  HTTPS is required for Android device administrator and Android Enterprise. If multiple URLs load-balance to different NDES
  servers across the three calls (capabilities, public key, signing request), the request fails.

## Strong mapping (KB5014754)
The KDC requires certificates for AD authentication to carry a SID mapping. For SCEP via Intune add the
`{{OnPremisesSecurityIdentifier}}` variable to the URI attribute of the SAN. Required for user certificates on all
platforms and, for device certificates, only for Entra hybrid-joined Windows devices. Users and devices must be synced from
AD to Entra ID.

## Troubleshooting
- Profile Error or Pending: Devices > All devices > the device > Device configuration, and the policy's Per setting status.
- Pending or no cert: confirm the trusted certificate profile reached the same users or devices as the SCEP profile.
- To get a cert quickly after enrolment, assign to a user group rather than a device group (device groups need full device
  registration first).
- A subject name with an escaped special character (`+ , ; =`) produces a CSR mismatch and challenge validation fails. Wrap
  the whole CN in quotes or remove the character; backslash escaping fails.
- A device must support every variable in the profile; `{{IMEI}}` on a device with no IMEI makes the profile fail.
- Android 12 and later personally owned work profiles cannot supply serial, IMEI or MEID variables.
- iOS/iPadOS and macOS: an expired certificate is not re-requested; exclude the device from the profile temporarily to
  remove it and request a new one.
- Editing a profile to add the S/MIME given-name and surname attributes triggers reissuance of all its certificates.

## Verify
The device store shows the certificate with the expected subject, SAN and EKU, chained to the trusted root, and the Wi-Fi or
VPN profile connects.

## Checked
Date: 2026-11-08. Read in full: Intune "Use certificates for authentication" (updated 2026-04-07), "Create and assign SCEP
certificate profiles" (2026-04-07) and the Cloud PKI overview (2026-09-08). Removed as unconfirmed: "Intune Suite add-on"
wording, Entra App Proxy for NDES, the EKU OID, TPM "preferred", PKCS delivering a PFX with an off-device key, Event Viewer
and NDES connector log paths, IIS and template permission steps, NPS and CRL troubleshooting, the claim that user vs device
group type is the top cause of Pending, and the "any profile change reissues certs" claim.
Method: documentation only; no commands were run.
