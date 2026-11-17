---
id: computing-software.systems-network-administration.powershell.powershell-enums-and-flags
name: powershell-enums-and-flags
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-classes, powershell-enum, flags-attribute, bitwise-operators, useraccountcontrol, enum-parsing]
level: practitioner
status: verified
description: "Define and use enums and [Flags()] enums in PowerShell: parsing, validation, bitwise -band/-bor tests, decoding values like userAccountControl, and .NET enum helpers."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_enum
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/useraccountcontrol-manipulate-account-properties
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_arithmetic_operators
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enums and flags

## Simple enum
```powershell
enum Environment { Dev = 1; Test = 2; Prod = 3 }
function Deploy-App { param([Parameter(Mandatory)][Environment]$Target) "Deploying to $Target ($([int]$Target))" }
Deploy-App -Target prod             # case-insensitive string conversion; tab-completes
[Environment]'Test'                 # cast from string
[Environment]::Prod -gt [Environment]::Test   # compares underlying values
[enum]::GetNames([Environment])
[Environment].GetEnumValues()
```
An enum-typed parameter validates like `ValidateSet` and gives tab completion for free.
Specify an underlying type with `enum Port : uint16 { Http = 80 }` (PS 6.2+ per about_Enum; checked: `value__` is `UInt16`).

## Flags enum for bit fields
```powershell
[Flags()] enum UAC {
  SCRIPT = 0x0001; ACCOUNTDISABLE = 0x0002; LOCKOUT = 0x0010; PASSWD_NOTREQD = 0x0020
  NORMAL_ACCOUNT = 0x0200; DONT_EXPIRE_PASSWORD = 0x10000; SMARTCARD_REQUIRED = 0x40000
  TRUSTED_FOR_DELEGATION = 0x80000; NOT_DELEGATED = 0x100000; DONT_REQ_PREAUTH = 0x400000
  PASSWORD_EXPIRED = 0x800000; TRUSTED_TO_AUTH_FOR_DELEGATION = 0x1000000
}
[UAC]66048        # userAccountControl value 0x10200 -> NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
```
Values must be powers of two (or deliberate combinations). Combine with `-bor`, test with
`-band` or `.HasFlag()`:
```powershell
$f = [UAC]::NORMAL_ACCOUNT -bor [UAC]::DONT_EXPIRE_PASSWORD
($f -band [UAC]::ACCOUNTDISABLE) -ne 0     # False
$f.HasFlag([UAC]::DONT_EXPIRE_PASSWORD)    # True
[UAC]'NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD' # parse a comma list
```
The flag values above match Microsoft's "Use the UserAccountControl flags" article. For LDAP filters on bits, use the matching rule OIDs instead of client-side tests:
`(userAccountControl:1.2.840.113556.1.4.803:=65536)` in an LDAP filter (bitwise AND).
Note `LOCKOUT` and `PASSWORD_EXPIRED` are computed bits (UF_LOCKOUT 0x10, UF_PASSWORD_EXPIRED 0x800000) that are not persisted in userAccountControl; read `msDS-User-Account-Control-Computed` for those (Win32 AD schema reference). The OID 1.2.840.113556.1.4.803 is LDAP_MATCHING_RULE_BIT_AND in Microsoft's search-filter syntax page.

## Existing .NET enums
```powershell
[System.IO.FileAttributes]'ReadOnly, Hidden'
(Get-Item .\file.txt).Attributes -band [IO.FileAttributes]::Hidden
[enum]::GetValues([System.Security.AccessControl.FileSystemRights]) | ForEach-Object { '{0,-30} {1:X8}' -f $_, [int]$_ }
[System.Enum]::TryParse([Environment], 'qa', $true, [ref]$null)   # PS 7: False, no exception
```

## Gotchas
- An invalid string cast throws a terminating error listing valid names; use `TryParse` for
  untrusted input.
- Enums defined in a module are not exported by `Import-Module`; use `using module`
  (same as classes).
- Comparing an enum to a string compares by name after conversion: `$svc.Status -eq 'Running'` works.

Checked on 7.6: `-bor`/`-band`/`HasFlag`, comma-list parse, `TryParse` returning `False` for `'qa'`, and a module-defined enum is not visible after `Import-Module` ("Unable to find type").

## Verify
- [ ] Decoded flag lists match the AD Attribute Editor's userAccountControl display.
- [ ] Invalid parameter values are rejected with a helpful message.
