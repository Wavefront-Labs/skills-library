---
id: computing-software.cybersecurity-defensive.identity-access-management.adcs-hardening
name: adcs-hardening
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [active-directory-security, adcs-hardening, ad-cs, certificate-templates, esc1, esc8, certify, locksmith, pkinit, enrollment-agents]
level: advanced
status: draft
description: "Harden Active Directory Certificate Services against ESC-class escalation: template flags, enrolment rights, web enrolment relay, CA settings and audit."
sources: ["SpecterOps - Certified Pre-Owned whitepaper (ESC1-ESC8)", "Microsoft Learn - AD CS security guidance and KB5014754 strong certificate mapping", "Locksmith (TrimarcJake) documentation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AD CS hardening

**Goal:** the enterprise CA cannot be used by ordinary users to obtain certificates that
authenticate as someone else, especially as domain admins.

## Find issues
- **Locksmith** (`Invoke-Locksmith -Mode 0` for report, mode 4 offers fixes) detects common ESC
  misconfigurations; **PSPKIAudit** and BloodHound ADCS edges also help.
- `certutil -v -dstemplate` and the Certificate Templates console for template settings.

## Fix the common classes
| Class | Misconfiguration | Fix |
|---|---|---|
| ESC1 | Template allows requester to supply subject (`ENROLLEE_SUPPLIES_SUBJECT`) + client auth EKU + low-privileged enrol rights | Remove the flag or require manager approval; restrict enrol rights |
| ESC2/ESC3 | Any Purpose or no EKU; enrolment agent templates broadly enrollable | Specific EKUs; restrict enrolment agent templates and set enrolment agent restrictions on the CA |
| ESC4 | Low-privileged users have write rights on templates | Fix template ACLs (only PKI admins write) |
| ESC6 | CA flag `EDITF_ATTRIBUTESUBJECTALTNAME2` lets any request specify SAN | `certutil -setreg policy\EditFlags -EDITF_ATTRIBUTESUBJECTALTNAME2` then restart CertSvc |
| ESC7 | Low-privileged CA managers/officers | Restrict CA permissions |
| ESC8 | NTLM relay to HTTP web enrolment (certsrv) | Remove web enrolment if unused; otherwise HTTPS with EPA, disable NTLM on IIS |
| ESC9/10 | Weak certificate mapping | Enforce strong mapping (KB5014754, Full Enforcement mode) |

## Operate
- Treat CA servers as Tier 0; only Tier 0 admins log on.
- Audit: enable CA auditing (`certutil -setreg CA\AuditFilter 127`) and object access auditing; collect events 4886 (request), 4887 (issued), 4899/4900 (template changes).
- Alert on certificates issued with a SAN different from the requester, and on template modifications.
- Remove unused templates from publication on CAs.

## Gotchas
- Default templates like "User" are safe; custom copies made years ago are where ESC1 lives.
- Fixing a template does not revoke certificates already issued from it; review issued certs and revoke suspicious ones.
- Strong mapping enforcement can break legacy certificate-based logons; check events 39/40/41 on DCs in compatibility mode first.

## Verify
- [ ] Locksmith reports no ESC1-ESC8 findings.
- [ ] Test request with a SAN for another user from a standard account is denied.
