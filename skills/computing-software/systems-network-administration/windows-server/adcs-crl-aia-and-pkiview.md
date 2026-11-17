---
id: computing-software.systems-network-administration.windows-server.adcs-crl-aia-and-pkiview
name: adcs-crl-aia-and-pkiview
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, ad-cs, certificate-services, crl, aia, cdp, pkiview, delta-crl, certutil-urlfetch, revocation]
level: advanced
status: docs-checked
description: "Publish AD CS CRLs and AIA correctly: CDP and AIA URL variables, CRL and delta schedules, offline root CRL renewal, pkiview and certutil -url checks."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/operate-certificate-revocation-crl-cdp
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/monitor-ad-cs-health-enterprise-pki
  - https://learn.microsoft.com/en-us/windows-server/networking/core-network-guide/cncg/server-certs/configure-the-cdp-and-aia-extensions-on-ca1
  - https://learn.microsoft.com/en-us/windows-server/networking/core-network-guide/cncg/server-certs/configure-web1-to-distribute-certificate-revocation-lists
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/certutil
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# CRL and AIA publication and pkiview checks

When clients cannot fetch a valid CRL, TLS, smart card logon, VPN and 802.1X fail
(revocation offline). An expired root CRL takes the whole PKI down.

## CDP entries
Each CDP entry separates publication (`PublishToServer`, `PublishDeltaToServer`) from retrieval settings embedded in
certificates (`AddToCertificateCdp`, `AddToFreshestCrl`). Use an HTTP location for client-facing retrieval; a local
folder or UNC path is a publication location, not a good client-facing URL.
```powershell
certutil -getreg CA\CRLPublicationURLs
Get-CACrlDistributionPoint; Get-CAAuthorityInformationAccess
Add-CACrlDistributionPoint -Uri 'http://pki.example.com/pki/<CAName><CRLNameSuffix><DeltaCRLAllowed>.crl' -AddToCertificateCdp -AddToFreshestCrl
```
Changes only apply to certificates issued afterwards; keep the previous endpoint available until no unexpired
certificate references it. The cmdlet prompts for confirmation (add `-Force` only when your change process allows an
unattended run) and does not create the web site or copy files; restart the CA service if the cmdlet says it is required.

## Schedules
A publishing interval and a CRL validity period are different settings: make sure a successor CRL is published and
distributed before clients need it. After a schedule change, restart the CA service and publish a new CRL:
```powershell
Restart-Service certsvc; certutil -crl
```
Copy CRLs to every HTTP retrieval location (the cmdlets do not copy files) and verify the files arrive.

## Offline root CRL
Use a scheduled, witnessed process before the CRL expires: start the root, `certutil -crl`, copy the CRL to every
retrieval endpoint and publish it with `certutil -dspublish -f <file>.crl`, then verify from the networks that depend
on it. Avoid delta CRLs on an offline root unless a requirement justifies them.

## IIS hosting gotcha
In IIS Manager, open Request Filtering for the pki virtual directory and select **Allow double escaping** so delta CRL
file names are served.

## Verify
```powershell
certutil -verify -urlfetch issued.cer       # every URL "Verified"
certutil -URL issued.cer                     # URL retrieval tool
```
- [ ] Enterprise PKI (PKIView) shows every CA certificate and CRL location healthy.

## Checked

Checked 2026-10-26 against learn.microsoft.com / MicrosoftDocs/windowsserverdocs main branch, last commit 2026-10-23. Confirmed: Get-CACrlDistributionPoint properties and Add-CACrlDistributionPoint flags (-AddToCertificateCdp, -AddToFreshestCrl) with the CAName, CRLNameSuffix and DeltaCRLAllowed placeholders; that CDP changes affect only certificates issued afterwards; the publishing interval versus validity distinction and the offline root guidance; certutil -dspublish, -getreg, -URL and -verify -urlfetch; restart of certsvc; the Allow double escaping request filtering setting; Enterprise PKI (PKIView). Removed as unconfirmed: the numeric CDP flag values and the % variable list, the CRLPeriod, CRLDeltaPeriod and CRLOverlap registry values and example numbers, the reason delta names need double escaping, the appcmd line and the robocopy suggestion.

Method: documentation only; no commands were run.
