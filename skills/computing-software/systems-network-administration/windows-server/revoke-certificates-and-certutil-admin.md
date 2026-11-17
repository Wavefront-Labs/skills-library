---
id: computing-software.systems-network-administration.windows-server.revoke-certificates-and-certutil-admin
name: revoke-certificates-and-certutil-admin
category: computing-software
field: systems-network-administration
product: windows-server
tags: [ad-cs, certificate-revocation, certutil, crl, certificate-services]
level: practitioner
status: docs-checked
description: "Revoke issued certificates with the right reason codes, publish CRLs immediately, and use certutil for CA database queries, backup checks and URL tests."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/certutil
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Revoking certificates and certutil admin tasks

## Find the certificate
```cmd
certutil -view -restrict "CommonName=web01.corp.example.com" -out "RequestID,SerialNumber,NotAfter"
```
`-restrict` takes comma-separated column/operator/constant restrictions and `-out` selects the columns; add a Disposition
restriction to filter by request state.

## Revoke
```cmd
certutil -revoke <SerialNumber> 1
```
Reason codes: 0 unspecified (default), 1 key compromise, 2 CA compromise, 3 affiliation changed, 4 superseded, 5 cessation of
operation, **6 certificate hold**, 8 remove from CRL, 9 privilege withdrawn, 10 AA compromise; `unrevoke` reverses a revocation
(for a certificate on hold).
Use 1 for leaked keys; 4 when replaced; 5 for decommissioned servers.

## Publish now
Revocation is not visible until a new CRL is published and clients' cached CRLs expire:
```cmd
certutil -crl
```
Copy the new CRL to the HTTP CDP location if publication to it is not automatic. Clients cache CRLs; `certutil -URLcache *
delete` clears the current user's cached URLs (add `-f` to force a refetch) on a system you are testing from.

## Other everyday certutil
| Task | Command |
|---|---|
| CA config and health | `certutil -ping`, `certutil -cainfo` |
| Test chain and URLs as a client | `certutil -verify -urlfetch cert.cer` |
| Dump CA settings | `certutil -getreg CA` |
| Back up CA database and key | `certutil -backup <BACKUP_DIR> [Incremental] [KeepLog]` |
| Issue/deny a pending request | `certutil -resubmit <RequestId>` / `certutil -deny <RequestId>` |
| Delete expired and revoked certificate rows (shrink DB) | `certutil -deleterow <date> Cert` |

## Verify
- [ ] `certutil -verify -urlfetch` on the revoked cert reports it revoked after the new CRL is published.

## Checked

Checked 2026-10-26 against learn.microsoft.com / MicrosoftDocs/windowsserverdocs main branch, last commit 2026-10-23. Confirmed in the certutil reference: -revoke SerialNumber [Reason] with reason values 0-6, 8, 9, 10 and Unrevoke, -view with -restrict and -out, -crl, -ping, -CAInfo, -getreg, -verify -urlfetch, -backup BackupDirectory [Incremental] [KeepLog], -resubmit and -deny RequestId, -deleterow RowId | Date [Request | Cert | Ext | Attrib | CRL] (Cert deletes expired and revoked certificates) and -URLcache [URL | CRL | * [delete]]. Removed as unconfirmed: the numeric Disposition values, the claim that hold is the only reversible reason, reliance on OCSP for urgent cases, and the key password note for -backup.

Method: documentation only; no commands were run.
