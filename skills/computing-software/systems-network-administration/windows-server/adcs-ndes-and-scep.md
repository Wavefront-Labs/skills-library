---
id: computing-software.systems-network-administration.windows-server.adcs-ndes-and-scep
name: adcs-ndes-and-scep
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, ad-cs, ndes, scep, intune-certificate-connector, mobile-devices]
level: advanced
status: docs-checked
description: "Deploy AD CS Network Device Enrollment Service (NDES) for SCEP enrollment of network and Intune-managed devices: service account, templates, registry mapping and hardening."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/network-device-enrollment-service-overview
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/create-domain-user-account-ndes-service-account
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/install-policy-module-network-device-enrollment-service
  - https://learn.microsoft.com/en-us/powershell/module/adcsdeployment/install-adcsnetworkdeviceenrollmentservice
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NDES and SCEP

NDES implements SCEP so devices that cannot join AD (routers, MDM-managed phones) get certificates from an
enterprise CA.

## Install
- Dedicated member server (not the CA), IIS installed with the role.
- Service account: domain user (a managed service account or gMSA is also supported) in local IIS_IUSRS, with **Request** permission on the CA and
  Read + Enroll on the template.
```powershell
Install-WindowsFeature ADCS-Device-Enrollment -IncludeManagementTools
Install-AdcsNetworkDeviceEnrollmentService -ServiceAccountName AD\svc-ndes -ServiceAccountPassword (Read-Host -AsSecureString) `
  -CAConfig 'CA01.ad.example.com\Example Issuing CA' -RAName 'Example NDES RA' -RACountry AU
```
This sets up the NDES registration authority (RA) information; NDES signs enrolment requests with an Enrollment Agent
certificate when it forwards them to the CA.

## Templates
Duplicate a template (e.g. from "User" or "Computer"), Subject Name = **Supply in the request**, set key size and
EKU; grant svc-ndes Read/Enroll. Point NDES at the template through values under the registry key
`HKLM\SOFTWARE\Microsoft\Cryptography\MSCEP` (value names per the NDES configuration steps for your Windows
Server release), then restart IIS (`IISReset`).

## Use it
- Device communication location: `https://<hostname>/certsrv/mscep`.
- Administrator challenge-password retrieval: `https://<hostname>/certsrv/mscep_admin`.
- MDM software requests a challenge password from `mscep_admin`; an optional NDES policy module can validate the
  request (registry value `Policy` under `MSCEP\Modules`, then `IISReset`).

## Hardening
- Never expose `mscep_admin` externally; only the device-facing `/certsrv/mscep` endpoint needs to be reachable.
- Template subject is supplied by the requester: restrict who can reach NDES and validate requests (policy module).

## Verify
- [ ] `https://<hostname>/certsrv/mscep` responds; a test device enrolls and the CA shows the issued cert.

## Checked

Checked 2026-10-26 against learn.microsoft.com / MicrosoftDocs/windowsserverdocs main branch, last commit 2026-10-23. Confirmed: Install-AdcsNetworkDeviceEnrollmentService parameters (-ServiceAccountName, -ServiceAccountPassword, -CAConfig, -RAName, -RACountry); the mscep and mscep_admin endpoints; NDES signing with an Enrollment Agent certificate; IIS_IUSRS membership and managed service account note; the MSCEP registry key, the Modules and Policy value, and IISReset for the policy module. Removed as unconfirmed: the three MSCEP template value names, the CEP Encryption certificate name, the MaxFieldLength and MaxRequestBytes tuning, mscep.dll as the URL tail, the gMSA 2022 gate, and Intune connector and application proxy specifics (the Intune documentation is not in a public repository).

Method: documentation only; no commands were run.
