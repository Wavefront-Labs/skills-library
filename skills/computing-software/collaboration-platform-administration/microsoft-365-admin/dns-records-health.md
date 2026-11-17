---
id: computing-software.collaboration-platform-administration.microsoft-365-admin.dns-records-health
name: dns-records-health
category: computing-software
field: collaboration-platform-administration
product: microsoft-365-admin
tags: [dns-records-health]
level: practitioner
status: draft
description: Know the DNS records Microsoft 365 needs and diagnose a domain reporting DNS errors.
sources: ['https://learn.microsoft.com/en-us/microsoft-365/admin/', 'https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ms-102']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Required DNS records for Microsoft 365 services
**Goal:** Know the DNS records Microsoft 365 needs and diagnose a domain reporting DNS errors.

- MX points to <domain>.mail.protection.outlook.com (priority 0); SPF TXT includes spf.protection.outlook.com.
- Autodiscover CNAME to autodiscover.outlook.com.
- Teams/Skype legacy: lyncdiscover and sip CNAMEs plus SRV records (_sip._tls, _sipfederationtls._tcp); legacy records may be unnecessary for Teams-only tenants (confirm in the current docs).
- Use Domains > select domain > Check health to see missing or conflicting records.
- Enterprise registration and enrollment CNAMEs are for device management (enterpriseregistration, enterpriseenrollment).

## Gotchas
- A pre-existing SPF TXT must be merged, never duplicated; two SPF records break evaluation.
- Cloudflare proxying (orange cloud) must be off for these CNAMEs.

## Self-check
The admin center shows no DNS warnings and a test mail round trip succeeds.
