---
id: computing-software.systems-network-administration.windows-server.ca-certificate-renewal-and-backup
name: ca-certificate-renewal-and-backup
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, ad-cs, certificate-services, ca-renewal, backup-ca, backup-carolesservice, certutil-backup, ca-restore, key-archival]
level: advanced
status: docs-checked
description: "Back up an AD CS CA (database, key, registry, CAPolicy) and renew the CA certificate with or without a new key, including publishing and restore steps."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/renew-root-ca-certificate
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/migrate-certification-authority
  - https://learn.microsoft.com/en-us/powershell/module/adcsadministration/backup-caroleservice
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/certutil
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Renew a CA certificate and back up the CA

## Backup (schedule it)
```powershell
Backup-CARoleService -Path '<vol>:\CABackup' -Password (Read-Host -AsSecureString)   # DB + private key (PFX)
Backup-CARoleService -Path '<vol>:\CABackup' -DatabaseOnly                             # nightly
reg export HKLM\SYSTEM\CurrentControlSet\Services\CertSvc\Configuration '<vol>:\CABackup\certsvc.reg' /y
Copy-Item "$env:windir\CAPolicy.inf" '<vol>:\CABackup' -EA 0
certutil -catemplates > '<vol>:\CABackup\templates.txt'
```
- Store the PFX and password separately and offline. Without the key you cannot restore
  the CA identity.
- `-Password` applies to the key backup parameter sets; `-DatabaseOnly`, `-Incremental` and `-KeepLog` apply to database backups.
- If the key is in an HSM, use the HSM vendor's backup procedure.

## Restore / move to a new server
Install the role on the new server with the **existing** key (`Install-AdcsCertificationAuthority -CertFile ca.p12 -CertFilePassword ...`, same CA name), stop certsvc, `Restore-CARoleService -Path ... -Force`, import the registry file, start certsvc, re-publish templates.

## Renew the CA certificate
Renewing with the existing key pair is the simplest approach. Renew with a new key pair if the signing key is compromised,
an application requires a new signing key, or the CRL has grown too large. In the console, Renew CA Certificate asks to stop
the service and whether to generate a new key pair.
```powershell
certutil -renewCert ReuseKeys      # same key: the CA keeps the same CRL
certutil -renewCert                # new key: a new CRL with a CRL name suffix, e.g. RootCA(1).crl
```
- Subordinate CA: generates a request; submit to the parent CA, then
  `certutil -installcert new.crt`.
- Root CA: an enterprise root is distributed automatically in the domain (`gpupdate /force` speeds it up); for a standalone
  root export the certificate and distribute it by Group Policy, and manually to non-domain devices. Publishing to AD:
  `certutil -dspublish -f root2.crt RootCA`.
- The renewed certificate is a new file with the certificate index in parentheses (for example `RootCA(1).crt`); publish it
  to the AIA HTTP path and run `certutil -crl`.

## Gotchas
- A new-key renewal creates a new CRL for certificates signed with the new key; the old CRL must stay available for certificates signed with the old key.
- Do not remove the previous CA certificate from clients: it can still be needed for validating older signatures.

## Verify
- [ ] `certutil -cainfo` shows the new CA certificate; Enterprise PKI (PKIView) is healthy for each CA certificate.
- [ ] A test restore to an isolated VM succeeded in the last year.

## Checked

Checked 2026-10-26 against learn.microsoft.com / MicrosoftDocs/windowsserverdocs main branch, last commit 2026-10-23. Confirmed: Backup-CARoleService and Restore-CARoleService parameter sets (-Path, -Password, -DatabaseOnly, -Incremental, -KeepLog, -Force), certutil -renewCert [ReuseKeys], -installCert, -dspublish ... RootCA, the renewal behaviour for existing versus new key pairs (same CRL versus a new CRL with a name suffix, certificate file with an index in parentheses), enterprise versus standalone root distribution, and HSM backup per vendor. Removed as unconfirmed: renew at half of lifetime, the claim that the root self-signs immediately, system state backup coverage, the CA ValidityPeriodUnits check, and the two-active-CRLs wording.

Method: documentation only; no commands were run.
