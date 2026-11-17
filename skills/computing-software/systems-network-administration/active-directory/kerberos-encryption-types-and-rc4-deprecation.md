---
id: computing-software.systems-network-administration.active-directory.kerberos-encryption-types-and-rc4-deprecation
name: kerberos-encryption-types-and-rc4-deprecation
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, authentication-policies, kerberos-encryption-types, rc4-deprecation, aes, msds-supportedencryptiontypes]
level: advanced
status: docs-checked
description: "Move a domain to AES Kerberos: audit RC4 use from 4768/4769 events, set msDS-SupportedEncryptionTypes, reset old passwords and plan for RC4 removal."
sources:
  - https://learn.microsoft.com/en-us/windows-server/security/kerberos/detect-remediate-rc4-kerberos
  - https://learn.microsoft.com/en-us/windows-server/get-started/whats-new-windows-server-2025
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/set-aduser
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/ktpass
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kerberos encryption types and RC4 deprecation

RC4 is considered insecure, is the Kerberoasting-friendly default for accounts that do not support AES, and is being
phased out. Get to AES before the platform does it for you.

## Where things stand
- Updates from 8 November 2022 (CVE-2022-37966, KB5021131) changed the default Kerberos encryption type to AES-SHA1
  for accounts where no type is set.
- Windows Server 2025 DCs no longer issue TGTs with RC4 encryption, and Kerberos no longer honours the legacy
  `SupportedEncryptionTypes` registry value (use Group Policy).
- The Microsoft page (dated 2026-02-06) said Microsoft planned to disable RC4 as the default assumed supported
  encryption type on DCs by the end of Q2 2026 (CVE-2026-20833, KB5073381). Confirm the current state in that KB before
  relying on the old default.

## Audit current use
On DCs, security events **4768** (TGT) and **4769** (service ticket) carry the encryption fields. Ticket Encryption Type
values: `0x11` AES128-CTS-HMAC-SHA1-96, `0x12` AES256-CTS-HMAC-SHA1-96, `0x17` RC4-HMAC, `0x18` RC4-HMAC-EXP. Also read
`MSDS-SupportedEncryptionTypes`, `Available Keys`, `Advertized Etypes` and `Session Encryption Type`. RC4 detail is
logged on KDCs for Windows Server 2019 and later (and Windows Server 2016 with the January 2025 cumulative update).
Microsoft publishes two open-source scripts for this in its Kerberos-Crypto repository on GitHub (review them before
use): `List-AccountKeys.ps1` for the keys available per account and `Get-KerbEncryptionUsage.ps1`, which takes
`-Encryption RC4` to filter. A SIEM works too.

## Why accounts lack AES keys
- An account created before AES-SHA1 support in Windows Kerberos whose password was never reset lacks AES-SHA1 keys;
  changing the password generates them.
- The processed `msDS-SupportedEncryptionTypes` value excludes AES (for example 4 = RC4 only). If the attribute is not
  set, the KDC uses `DefaultDomainSupportedEncTypes`.

## Configure
```powershell
Set-ADUser svc-legacy -KerberosEncryptionType AES128,AES256
```
`-KerberosEncryptionType` accepts None, DES, RC4, AES128 and AES256. Domain-wide default for accounts without the attribute: the DC registry value `DefaultDomainSupportedEncTypes`
under `HKLM\System\CurrentControlSet\services\KDC` (REG_DWORD): `0x18` allows only AES128 and AES256. Without the value
the default also assumes DES, RC4 and AES session keys. Changing it affects **all** accounts that have no attribute
value, so set explicit values on accounts where you can.

GPO "Network security: Configure encryption types allowed for Kerberos" (Computer Configuration > Windows Settings >
Security Settings > Local Policies > Security Options): tick AES128_HMAC_SHA1 and AES256_HMAC_SHA1 to allow AES only;
add RC4_HMAC_MD5 to allow both. Restart devices after the policy applies.

## Plan
1. Audit for a representative period. 2. Reset passwords on accounts without AES keys. 3. Set AES on service accounts.
4. Fix or isolate apps that only do RC4 (regenerate keytabs with a `ktpass /crypto AES256-SHA1` or `AES128-SHA1` type).
5. Remove RC4 from the allowed types or set `DefaultDomainSupportedEncTypes` to `0x18` on all DCs. After disabling,
failures show as `KDC_ERR_ETYPE_NOTSUPP` (event 4769 failure code `0xE`); `klist get HOST/<server>` reproduces it.

## Verify
- [ ] No RC4 (`0x17`) tickets in the 4768/4769 events over a representative period.

## Checked

Date: 2026-10-27. Documentation: "Detect and remediate RC4 usage in Kerberos" (2026-02-06), What's new in Windows Server
2025, Set-ADUser (Windows Server 2025 module page), ktpass reference (MicrosoftDocs/windowsserverdocs and
windows-powershell-docs, main branch).
Confirmed: event IDs and ticket type values, 2022 default change, RC4 TGT removal on 2025 DCs, the registry key, value
name and `0x18`, GPO name and option names, `-KerberosEncryptionType` values, `ktpass /crypto` values, failure code `0xE`.
Removed unconfirmed claims: the PowerShell event-parsing script (field index not documented), "events 201-209", the
"AES + RC4 session keys" meaning of `0x1C`, the DFL 2008 password-reset rule, the "Future" option and the krbtgt-reset
advice.

Method: documentation only; no commands were run.
