---
id: computing-software.systems-network-administration.powershell.dsc-credentials-encryption
name: dsc-credentials-encryption
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, dsc, desired-state-configuration, dsc-credentials, mof-encryption, document-encryption-certificate, psdscallowplaintextpassword, psdscallowdomainuser, psdscrunascredential]
level: advanced
status: docs-checked
description: "Use credentials in DSC configurations safely: document-encryption certificates, ConfigurationData CertificateFile/Thumbprint, LCM CertificateID, PsDscRunAsCredential."
sources:
  - https://learn.microsoft.com/en-us/powershell/dsc/pull-server/securemof
  - https://learn.microsoft.com/en-us/powershell/dsc/configurations/configdatacredentials
  - https://learn.microsoft.com/en-us/powershell/dsc/configurations/runasuser
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Credentials in DSC configurations

Compiling a configuration that contains a credential fails with *"Converting and storing encrypted passwords as plain
text is not recommended"* unless you encrypt with a certificate (correct) or set `PSDscAllowPlainTextPassword = $true`
(not recommended: the MOF then holds the password in clear text; take precautions when storing such MOFs).

## 1. Encryption certificate on each target node
Requirements from the Learn article:
- Key Usage must contain KeyEncipherment and DataEncipherment, and should not contain Digital Signature.
- Enhanced Key Usage must contain Document Encryption (1.3.6.1.4.1.311.80.1) and should not contain Client
  Authentication or Server Authentication.
- The private key is available on the target node, in `Cert:\LocalMachine\My`.
- The provider must be "Microsoft RSA SChannel Cryptographic Provider".
Using a certificate with Digital Signature or authentication EKUs works but makes the key easier to misuse; use a
certificate created only for this purpose.

Recommended: create the certificate on the target node and export only the public key to the authoring machine, so the
private key never leaves the node. Learn's example (run as Administrator):
```powershell
$cert = New-SelfSignedCertificate -Type DocumentEncryptionCertLegacyCsp -DnsName 'DscEncryptionCert' -HashAlgorithm SHA256
$cert | Export-Certificate -FilePath "$env:temp\DscPublicKey.cer" -Force
```

## 2. Reference the public key in ConfigurationData
- `CertificateFile`: the public-key-only certificate file (DER or Base-64 encoded X.509) used to encrypt for that node.
- `Thumbprint`: the certificate that decrypts on the target node; it must exist in the node's Local Machine store.
- `PSDscAllowPlainTextPassword`: allow unencrypted credentials (not recommended).
- `PSDscAllowDomainUser = $true` suppresses the warning about using a domain account as a credential; a local account
  avoids exposing domain credentials that could be used on other servers.
```powershell
$cd = @{ AllNodes = @( @{ NodeName = 'web01'; CertificateFile = '<CERT_DIR>\web01.cer'; Thumbprint = '<THUMBPRINT>'; PSDscAllowDomainUser = $true } ) }
```
Use a `[PSCredential]` configuration parameter so credentials are held for the shortest time; compiling prompts for the
credential and encrypts the MOF with the node's `CertificateFile`.

## 3. Tell the LCM which certificate decrypts
Before `Start-DscConfiguration` can work, set `CertificateId` in the LCM `Settings` block to the thumbprint so the
Local Configuration Manager can decrypt, then apply the metaconfiguration with `Set-DscLocalConfigurationManager`.

## Running a resource as another user
Every resource has an automatic `PsDscRunAsCredential` property (WMF 5.0+) that runs it as the given account. It
can be hard-coded or set to `Get-Credential`. In PowerShell 5.0 it was not supported in configurations calling composite
resources; 5.1 supports it. It is not available in PowerShell 4.0. The same encryption rules apply.

## Verify
- [ ] The compiled MOF shows encrypted values rather than the clear-text password.
- [ ] `Start-DscConfiguration -Wait -Verbose` applies without decryption errors.

## Checked
2026-11-09. Read in full the Learn securemof, configdatacredentials and runasuser articles. Confirmed: certificate
requirements, public-key-only export, ConfigurationData keys, CertificateId, domain-user warning, plain-text warning,
PsDscRunAsCredential versions. Removed as unconfirmed: exportable-key remark, CNG explanation, gMSA advice, DSC v3 and
Machine Configuration section, certificate-rotation and expiry pitfalls, the Select-String check.
Method: documentation only; no commands were run.
