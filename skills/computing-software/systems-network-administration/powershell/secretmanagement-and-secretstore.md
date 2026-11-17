---
id: computing-software.systems-network-administration.powershell.secretmanagement-and-secretstore
name: secretmanagement-and-secretstore
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-security, secretmanagement, secretstore, get-secret, register-secretvault, azure-key-vault, credential-handling, unattended-automation]
level: practitioner
status: docs-checked
description: "Keep credentials out of scripts with SecretManagement: register a SecretStore vault, unlock it in unattended jobs, and know the limits of each choice."
sources:
  - https://learn.microsoft.com/en-us/powershell/utility-modules/secretmanagement/overview
  - https://learn.microsoft.com/en-us/powershell/utility-modules/secretmanagement/how-to/using-secrets-in-automation
  - https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.secretstore/set-secretstoreconfiguration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SecretManagement and SecretStore

`Microsoft.PowerShell.SecretManagement` is a common set of cmdlets (`Get-Secret`, `Set-Secret`)
over pluggable vaults, so scripts do not depend on one vault's details. It becomes useful once
extension vaults are registered. `Microsoft.PowerShell.SecretStore` is a cross-platform extension
vault (any platform that supports PowerShell 7) that keeps secrets in a local file for the
current user and encrypts it with .NET Core cryptographic APIs. Other extension vaults listed by
Microsoft: Azure KeyVault (Microsoft owned), KeePass, LastPass, Hashicorp Vault, KeyChain and
CredMan; search the PowerShell Gallery for the SecretManagement tag. Assess how far you trust any
vault extension Microsoft did not write.

**Status:** Microsoft has declared the secret modules feature complete. They get security and
critical fixes only, and the repository is archived. Latest published: SecretManagement v1.1.2,
SecretStore v1.0.6. Microsoft points to passwordless methods (passkeys, SSO, Microsoft Entra ID
federation, hardware keys) as the future.

## Install and register a local SecretStore
```powershell
Install-Module -Name Microsoft.PowerShell.SecretManagement -Repository PSGallery
Install-Module -Name Microsoft.PowerShell.SecretStore -Repository PSGallery
Register-SecretVault -Name SecretStore -ModuleName Microsoft.PowerShell.SecretStore -DefaultVault
Get-Secret -Name <SECRET_NAME>
```
Add secrets with `Set-Secret`. The store is per user: run the install and configuration in the
user context of the account that will run the automation.

Defaults restored by `Set-SecretStoreConfiguration -Default`: scope CurrentUser, authentication
Password, PasswordTimeout 900 seconds, interaction Prompt.

## Unattended automation (Windows)
The store normally prompts for its password. For an automation account, give it a password held
as a SecureString and set interaction to None so it never prompts:
```powershell
# run once as the automation account
$credential = Get-Credential -UserName 'SecureStore'      # the user name is unimportant
$securePasswordPath = '<PATH_TO>\passwd.xml'
$credential.Password | Export-Clixml -Path $securePasswordPath

$password = Import-Clixml -Path $securePasswordPath
$storeConfiguration = @{
    Authentication  = 'Password'
    PasswordTimeout = 3600      # seconds the store stays unlocked
    Interaction     = 'None'
    Password        = $password
    Confirm         = $false
}
Set-SecretStoreConfiguration @storeConfiguration

# in the job
$password = Import-Clixml -Path $securePasswordPath
Unlock-SecretStore -Password $password
$automationPassword = Get-Secret -Name <SECRET_NAME>
```
- `Export-Clixml` of a SecureString is encrypted with Windows DPAPI. Microsoft calls this a
  Windows-only solution and suggests a CI system's secure variable (for example GitHub Actions
  secrets) as the other way to supply the password.
- After `PasswordTimeout` the store must be unlocked again before secrets can be read.
- With `Interaction None`, a command that needs a password and has none throws
  `Microsoft.PowerShell.SecretStore.PasswordRequiredException`.
- `-Authentication None` allows access without a password. Microsoft says it is less secure, may
  suit testing, and should not be used for important secrets.
- `-Scope` accepts CurrentUser or AllUsers, but only CurrentUser is currently supported.
- `-Password` on `Set-SecretStoreConfiguration` cannot change an existing password; use
  `Set-SecretStorePassword`.

## Rules
- Never put passwords in scripts or scheduled task arguments.
- Never write secrets to a transcript or log.

## Verify
- [ ] The scheduled job reads its secret without prompting, running as its own account.
- [ ] `Select-String -Path *.ps1 -Pattern 'AsPlainText -Force'` finds no hard-coded secrets.

## Checked
2026-11-09. Confirmed against the three cited Microsoft Learn pages (SecretManagement overview,
Use the SecretStore in automation, Set-SecretStoreConfiguration): module roles, vault list,
archived/feature-complete notice and versions, install and register commands, the DPAPI
Export-Clixml flow, Set-SecretStoreConfiguration parameters and defaults, Unlock-SecretStore and
timeout behaviour. Removed as unconfirmed: Install-PSResource, `Set-Secret -Secret` and
`Get-Secret -AsPlainText` forms, PSCredential round trip, 1Password vault, Az.KeyVault
registration, managed identity and Key Vault RBAC details, gMSA advice, backup advice, and
claims about where the store file lives.

Method: documentation only; no commands were run.
