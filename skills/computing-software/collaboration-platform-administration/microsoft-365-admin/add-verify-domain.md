---
id: computing-software.collaboration-platform-administration.microsoft-365-admin.add-verify-domain
name: add-verify-domain
category: computing-software
field: collaboration-platform-administration
product: microsoft-365-admin
tags: [add-verify-domain, m365-tenant-domains]
level: practitioner
status: draft
description: Add a custom domain to a Microsoft 365 tenant and verify ownership with a DNS record.
sources: ['https://learn.microsoft.com/en-us/microsoft-365/admin/', 'https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ms-102']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Add and verify a custom domain
**Goal:** Add a custom domain to a Microsoft 365 tenant and verify ownership with a DNS record.

- Admin center > Settings > Domains > Add domain; enter the domain name.
- Verify with the TXT record shown (MS=msXXXXXXXX) at the DNS host, or the MX record option.
- Choose services; accept the suggested records only after reviewing the existing ones.
- Set the default domain only when ready, since it changes new users' UPN suffix.
- Remove the TXT record later only if you are sure it is not needed (it is harmless to keep).

## Gotchas
- A domain can be verified in only one tenant at a time unless it is a subdomain; it must be removed from the old tenant first.
- DNS propagation can take up to 72 hours; recheck before assuming failure.

## Self-check
Domain status shows Healthy and `nslookup -type=TXT <domain>` returns the MS= value.
