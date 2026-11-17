---
id: computing-software.systems-network-administration.active-directory.admt-password-export-server
name: admt-password-export-server
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-migration, admt, password-export-server, pes, password-migration, encryption-key]
level: advanced
status: draft
description: "Install and use the ADMT Password Export Server to migrate passwords: create the key in the target, install PES on a source DC, service account and troubleshooting."
sources:
  - https://www.microsoft.com/en-us/download/details.aspx?id=56570
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ADMT Password Export Server (PES)

PES runs on a DC in the **source** domain and hands password hashes securely to ADMT so
users keep their passwords after migration.

## Create the encryption key (target, ADMT server)
```
admt key /option:create /sourcedomain:old.example.com /keyfile:'<vol>:\pes\key.pes' /keypassword:*
```
Transfer the key file securely to the source DC.

## Install PES (source DC, ideally the PDC emulator)
- Run the PES installer (pwdmig.msi; x64 version for 64-bit DCs), point it at the key
  file and enter the key password.
- The installer asks which account runs the PES service (LocalSystem or a source-domain
  account). The ADMT migration account must be in the source domain's Administrators
  group.
- Registry: `HKLM\System\CurrentControlSet\Control\Lsa\AllowPasswordExport = 1` to
  enable export (set it only during migration windows), then start the service
  `Password Export Server Service`.

## Use
In the user migration wizard choose **Migrate passwords**, specify the PES DC, or on the
command line `/po:copy /ps:oldpdc.old.example.com`.

## Troubleshooting
- "Unable to establish a session with the password export server": PES service not
  running, AllowPasswordExport = 0, RPC blocked, or the migration account lacks admin on
  the source DC.
- Password complexity in target stricter than source: migration still copies the hash;
  users are not forced to comply until next change.
- After migration set AllowPasswordExport back to 0 and uninstall PES.

## Verify
- [ ] Test user logs on to the target domain with the old password.
