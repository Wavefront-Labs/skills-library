---
id: computing-software.systems-network-administration.windows-server.adcs-migration-to-new-server
name: adcs-migration-to-new-server
category: computing-software
field: systems-network-administration
product: windows-server
tags: [ad-cs, adcs-migration, ca-renewal, backup-ca, workload-migration]
level: advanced
status: docs-checked
description: "Migrate an AD CS certification authority to a new server keeping the same CA name and keys: backup, registry export, removal, install with existing key and restore."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/migrate-certification-authority
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/certutil
  - https://learn.microsoft.com/en-us/powershell/module/adcsdeployment/install-adcscertificationauthority
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating AD CS to a new server

Keep the CA name and key: certificates already issued stay valid, CRL/AIA chains unchanged.

## 1. Source CA: back up
```cmd
certutil -backup <BACKUP_DIR> keepLog
reg export HKLM\SYSTEM\CurrentControlSet\Services\CertSvc\Configuration <BACKUP_DIR>\ca-config.reg
certutil -catemplates > <BACKUP_DIR>\templates.txt
```
Record CAPolicy.inf, CDP/AIA extensions (`certutil -getreg CA\CRLPublicationURLs`, `CACertPublicationURLs`), and
custom settings. If the key is in an HSM, follow the HSM vendor's migration steps instead of exporting the PFX.

## 2. Source CA: remove
After the backups, stop the CA service (`net stop certsvc`) so no more certificates are issued, then remove the CA role
service with Remove Roles and Features in Server Manager before installing it on the destination. Back up CAPolicy.inf
(in the Windows directory) and record the template list. If the destination host name differs, review the imported
registry for the old host name and update the Enrollment Services object `dNSHostName` in ADSI Edit.

## 3. Target: install with the existing key
```powershell
Install-WindowsFeature ADCS-Cert-Authority -IncludeManagementTools
Install-AdcsCertificationAuthority -CAType EnterpriseRootCa -CertFile <BACKUP_DIR>\CA.p12 -CertFilePassword (Read-Host -AsSecureString) -Force
```
(EnterpriseSubordinateCa for issuing CAs.)

## 4. Restore database and config
```cmd
net stop certsvc
certutil -f -restoredb <BACKUP_DIR>
reg import <BACKUP_DIR>\ca-config.reg
net start certsvc
```
`<BACKUP_DIR>` for the restore is the parent of the Database folder. Edit the exported .reg file first if the host name
changed (for example `CAServerName`). Republish templates with `certutil -setcatemplates + <templatelist>` using the
list recorded earlier, and fix CDP/AIA if the host name appears in URLs.

## Verify
- [ ] `certutil -ping`; issue a test certificate; pkiview.msc clean; old certificates still validate.

## Checked

Checked 2026-10-26 against learn.microsoft.com / MicrosoftDocs/windowsserverdocs main branch, last commit 2026-10-23. Confirmed in the Migrate a certification authority page: certutil -backup syntax (KeepLog), reg export of the CertSvc Configuration key, certutil -catemplates and -setcatemplates, stopping certsvc after backup, removing the role with Remove Roles and Features, importing the .p12 CA certificate (Install-AdcsCertificationAuthority with -CertFile and -CertFilePassword), certutil -f -restoredb with the parent of the Database directory, reg import, the CAServerName registry value, HSM vendor procedures, and dNSHostName on the Enrollment Services object. Removed or fixed as unconfirmed: Uninstall-AdcsCertificationAuthority as the removal step, the nonexistent certutil -setcasites step, and the claim that the AD objects are simply reused.

Method: documentation only; no commands were run.
