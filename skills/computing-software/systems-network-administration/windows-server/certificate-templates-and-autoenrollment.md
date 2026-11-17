---
id: computing-software.systems-network-administration.windows-server.certificate-templates-and-autoenrollment
name: certificate-templates-and-autoenrollment
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, ad-cs, certificate-services, certificate-templates, autoenrollment, certtmpl, enroll-permissions, certutil-pulse]
level: practitioner
status: docs-checked
description: "Create AD CS certificate templates and roll them out with autoenrollment: duplicate a template, key and subject settings, permissions, publish, GPO and verify."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/manage-certificate-templates
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-cs/certificate-template-concepts
  - https://learn.microsoft.com/en-us/powershell/module/adcsadministration/add-catemplate
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/certutil
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Certificate templates and autoenrollment

## Create a template
`certtmpl.msc` > duplicate a built-in (e.g. Computer, Web Server, Workstation
Authentication); never edit built-ins.
- Compatibility: select the oldest CA and recipient operating systems that must use the template (the newest listed values
  are Windows Server 2016 for the CA and Windows 10 / Windows Server 2016 for the recipient).
- General: a unique display name (note the short template name, which differs), validity and renewal periods.
- Cryptography: pick a provider that the CA and requesters support.
- Subject Name: prefer identity information from AD DS. If you enable **Supply in the request**, restrict enrollment and
  validate every permitted identity value; also confirm the CA-wide `EDITF_ATTRIBUTESUBJECTALTNAME2` flag is disabled.
- Extensions: application policies only what is needed (for example Server Authentication, Client Authentication).
- Security: grant Read, Enroll and, only when intended, Autoenroll to narrowly scoped groups. If you remove Authenticated
  Users, give every issuing CA computer account Read.

## Publish on the CA
```powershell
Add-CATemplate -Name 'CorpWebServer' -Force
certutil -catemplates
```

## Autoenrollment GPO
Computer (and/or User) Configuration > Policies > Windows Settings > Security Settings >
Public Key Policies > **Certificate Services Client - Auto-Enrollment**: Enabled, with the renewal and update options
your policy needs.
Trigger now: `gpupdate /force; certutil -pulse`.

## Supersede and re-issue
Add the predecessor on the replacement template's **Superseded Templates** tab only as part of an approved transition.
Supersedence can trigger enrollment for the replacement but does not remove older certificates from a user's store.

## Troubleshoot
- "Template not found": not published on any CA, or replication to the site's DCs pending.
- Access denied: the requester is not in a group with Read and Enroll, or the issuing CA computer account lacks Read.

## Verify
- [ ] `certutil -store my` on a target shows the template certificate (Template= field).

## Checked

Checked 2026-10-26 against learn.microsoft.com / MicrosoftDocs/windowsserverdocs main branch, last commit 2026-10-23. Confirmed: template Compatibility values, General, Subject Name, Security and Superseded Templates guidance, the Add-CATemplate -Name and -Force parameters, the Public Key Policies path for Certificate Services Client - Auto-Enrollment, certutil -catemplates and certutil -pulse. Removed as unconfirmed: one-year validity and six-week renewal, the RSA and ECDSA key sizes and SHA256 advice, the ESC1 wording, the Reenroll All Certificate Holders action, the autoenrollment event log name and event IDs, and the klist purge step.

Method: documentation only; no commands were run.
