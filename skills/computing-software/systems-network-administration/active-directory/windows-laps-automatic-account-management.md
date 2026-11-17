---
id: computing-software.systems-network-administration.active-directory.windows-laps-automatic-account-management
name: windows-laps-automatic-account-management
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, windows-laps, laps-automatic-account-management, passphrases, server-2025, local-admin]
level: advanced
status: docs-checked
description: "Use Windows LAPS automatic account management (Windows Server 2025 / 24H2): LAPS creates, names, randomizes and disables the managed local account, with passphrase options."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-concepts-account-management-modes
  - https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-management-policy-settings
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows LAPS automatic account management

Manual mode (the default) manages an account you maintain yourself. Automatic account management, supported only on
Windows 11 24H2, Windows Server 2025 and later, lets Windows LAPS create and manage the account.

## Policy settings (GPO or CSP: LAPS > Configure automatic account management)
- **AutomaticAccountManagementEnabled**: 1 = on; defaults to 0.
- **AutomaticAccountManagementTarget**: 0 = manage the built-in Administrator account, 1 = manage a new custom account;
  defaults to 1.
- **AutomaticAccountManagementNameOrPrefix**: name, or prefix when randomization is on; defaults to `WLapsAdmin`.
- **AutomaticAccountManagementRandomizeName**: 1 = suffix the name with a random six-digit number every time the
  password rotates; defaults to 0. Local account names max out at 20 characters, so the name part is truncated to 14.
- **AutomaticAccountManagementEnableAccount**: 1 = enable, 0 = disable; defaults to 0.
These settings are ignored unless `AutomaticAccountManagementEnabled` is on. The managed account is added to the local
Administrators group, has password-not-required and password-never-expires cleared, and its description marks it as
LAPS-controlled.

## Password complexity options (2025)
`PasswordComplexity`: 1-4 are letter/number/special-character tiers (default 4), 5 = improved readability, 6 = passphrase
(long words), 7 = passphrase (short words), 8 = passphrase (short words with unique prefixes). `PassphraseLength` is the
number of words, 3 to 10, default 6, and is ignored unless complexity is a passphrase option; it is supported only on
Windows 11 24H2, Windows Server 2025 and later.

## Gotchas
- Mixed fleets: the automatic-management settings are only supported on the OS versions above, so older machines need
  a different configuration.
- Keeping the account disabled prevents password spray against it, but it must be enabled by policy before use; a
  per-device randomized name means staff must not rely on a common account name (both points are from Microsoft's
  security discussion).
- Restricted Groups and Local Users and Groups policies ignore attempts to remove the managed account from the local
  Administrators group.

## Verify
- [ ] The managed account exists with the intended name behaviour on a new device, and the LAPS password can be retrieved.

## Checked

Documentation: Microsoft Learn "Windows LAPS account management modes" and "Windows LAPS policy settings", from
MicrosoftDocs/windowsserverdocs and MicrosoftDocs/windows-powershell-docs, main branch (latest commits 2026-10-23).
Confirmed: setting names, values, defaults (Enabled 0, Target 1, NameOrPrefix WLapsAdmin, RandomizeName 0, EnableAccount 0),
six-digit random suffix and 14-character limit, PasswordComplexity values 1-8, PassphraseLength 3-10 default 6, OS support
(Windows 11 24H2, Windows Server 2025 and later), configured-account properties, local group policy behaviour. Removed
unconfirmed: the "RID 500" wording, `Get-LapsADPassword -AsPlainText ... Account` output, `Get-LocalUser` check and the
"Rename administrator account" warning.

Method: documentation only; no commands were run.
