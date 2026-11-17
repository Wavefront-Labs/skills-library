---
id: computing-software.systems-network-administration.active-directory.defender-for-identity-sensors
name: defender-for-identity-sensors
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, privileged-access, defender-for-identity, mdi-sensor, mdi, identity-threat-detection, dsa-account, event-collection, security-posture]
level: practitioner
status: docs-checked
description: "Deploy Defender for Identity sensors on DCs, AD CS, AD FS and Entra Connect servers: v3.x vs v2.x, DSA gMSA for v2.x, event auditing, health and posture."
sources:
  - https://learn.microsoft.com/en-us/defender-for-identity/deploy/deploy-defender-identity
  - https://learn.microsoft.com/en-us/defender-for-identity/deploy/configure-windows-event-collection
  - https://learn.microsoft.com/en-us/defender-for-identity/directory-service-accounts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Microsoft Defender for Identity (MDI) sensors

**What:** sensors on identity servers collect signals (network traffic and Windows events) to detect threats such as
privilege escalation and high-risk lateral movement, and to report identity security issues such as unconstrained Kerberos
delegation, feeding Microsoft Defender XDR.

## Choose the sensor version
Install sensors on all domain controllers (including RODCs) and on AD FS, AD CS and Microsoft Entra Connect servers that are
not DCs (on Connect, both the active and staging servers).
- **Sensor v3.x**: Windows Server 2019 or later with the September 2026 or later cumulative update. Activate it from the
  Sensor management tab if the server is onboarded to Microsoft Defender for Endpoint, otherwise use the v3.x onboarding
  package. v3.x always uses the local system account (no Directory Service Account or gMSA); it does not support VPN
  integration or syslog notifications and has limitations with Azure ExpressRoute.
- **Sensor v2.x**: Windows Server 2016 or earlier, or where VPN or syslog features are needed. v2.x reads AD with a
  Directory Service Account (DSA); a gMSA is the recommended type.
- Both versions can coexist in one workspace. If any sensor is v3.x, choose "Automatically use the sensor's local system
  account for all sensors" in the DSA settings.

## Prerequisites
- Licence: EMS E5/A5, Microsoft 365 E5/A5/G5, Microsoft 365 E5/A5/G5/F5 Security, or standalone Defender for Identity.
- A Microsoft Entra tenant and a user with the Security administrator role to create the workspace.
- v2.x sensors need two cores, 6 GB RAM and 6 GB disk (10 GB recommended) beyond the server's own use.
- **v2.x DSA**: read access to all AD objects, including the **Deleted Objects** container so user deletions are detected.
  For a gMSA, create a security group, add the gMSA, and grant the rights to the group. Check it with `Test-MDIDSA`.
```powershell
New-ADServiceAccount -Name gmsaMDI -DNSHostName gmsaMDI.ad.example.com `
  -PrincipalsAllowedToRetrieveManagedPassword 'GG-MDI-Sensors'
```
- Outbound connectivity from sensors to the MDI cloud service.

## Windows event auditing
Auditing must be configured or the sensor raises health alerts. For v3.x, turn on **Automatic Windows auditing
configuration** in the Defender portal: it sets the advanced audit policies, domain object SACL entries, NTLM auditing,
Configuration container auditing, AD FS container auditing and the AD CS audit filter (the CA must already have an audit
filter). For v2.x and manual setups, follow the current event-collection page (it covers events such as 4776 and 8004
for NTLM). The `DefenderForIdentity` PowerShell module can check and set it:
`New-MDIConfigurationReport`, `Get-MDIConfiguration -Mode Domain -Configuration All` and `Set-MDIConfiguration`.

## Operate
- Review sensor health issues in the Defender portal (sensor stopped, DSA problems, auditing gaps) and the Sensor
  management tab action cards.
- Review the identity security posture recommendations and fix the highlighted weaknesses.

## Verify
- [ ] All DCs show sensors onboarded with no open health issues.
- [ ] `Test-MDIDSA -Identity <account> -Detailed` passes for v2.x DSAs.

## Checked
Checked 2026-10-27 against Microsoft Learn (Defender for Identity deployment overview, prerequisites, directory service
accounts and Windows event collection pages, read as rendered pages). Confirmed the v3.x and v2.x split and its OS
cut-offs, v3.x local-system account, licence list, DSA permissions including Deleted Objects, `Test-MDIDSA`, the MDI
module cmdlets and the automatic auditing options. Corrected: v3.x does not use a DSA or gMSA, and the old single "install a sensor with an
access key" flow now depends on sensor version. Removed the named attack-technique list, the `-KerberosEncryptionType`
option, the sizing-tool and zone-transfer test statements.
Method: documentation only; no commands were run.
