---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-domains-registration
name: cloud-domains-registration
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-domains, domain-registration, cloud-dns, registrar, whois-privacy]
level: practitioner
status: docs-checked
description: "Register and manage domains with Cloud Domains: search, contact privacy, linking to Cloud DNS, auto-renew, transfer and the Squarespace transition for former Google Domains."
sources: ["https://cloud.google.com/domains/docs/overview", "https://cloud.google.com/domains/docs/register-domain", "https://cloud.google.com/sdk/gcloud/reference/domains/registrations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Domains registration

Cloud Domains registers and configures domains in Google Cloud, billed through your Cloud Billing account and managed
per project with IAM. On 7 September 2023 Squarespace acquired all domain registrations and related customer accounts
from Google Domains; registering requires accepting the Squarespace Terms of Service for the project.

## 1. Search and register
```bash
gcloud domains registrations search-domains SEARCH_TERM
gcloud domains registrations get-register-parameters DOMAIN_NAME
gcloud domains registrations register DOMAIN_NAME
```
- `search-domains` suggests names. `get-register-parameters` returns current availability, yearly price,
  supported privacy modes and notices.
- If you choose Cloud DNS as the DNS provider, first create a managed public zone with the same domain name:
  `gcloud dns managed-zones create CLOUD_DNS_ZONE_NAME --description="DESCRIPTION" --dns-name=DOMAIN_NAME`.
  Alternatively use custom name servers (at least two), and configure records at your third-party DNS provider.
- `register` prompts for the yearly price agreement, DNS settings, contact privacy and contacts. Billing must be enabled on the project.
- A verification email is sent to the registrant email you enter.
- Only TLDs on the Cloud Domains pricing page are supported.

## 2. Contacts and privacy
- The registrant is the rightful owner of the domain, so keep contact details accurate. Admin and technical contacts are
  required only for country-code TLDs; since August 2025 generic TLDs ignore them.
- Privacy options: private contact data (proxy details, not offered for every TLD), limited public information
  (only for .com and .net) and all contact info public. Domains using `PRIVATE_CONTACT_DATA` are changed to `REDACTED_CONTACT_DATA` when migrated to Squarespace.

## 3. Renewal, DNS and transfer
- Cloud Domains sets the registration to renew yearly automatically while Cloud Billing is active; auto-renew can be turned off.
  A domain that expired within the past 30 days can be renewed with the CLI (`renew-domain`) or API at the yearly price.
- Cloud DNS can provide name servers and managed DNSSEC when you create a public zone.
- The `gcloud domains registrations` reference lists the groups `authorization-code`, `configure` (management, DNS or contact
  settings), `operations` and the commands `describe`, `list`, `update`, `delete`, `initiate-push-transfer` and `renew-domain`. Use `--help` on the group
  for exact flags. The `google-domains-dns` group is for deprecated Google Domains DNS configuration.

## Gotchas
- The domain is a project resource; project deletion or billing problems put the registration at risk, so use a dedicated project (project protection is not covered by the cited pages).
- Google Domains as DNS provider is retired and some Cloud Domains DNS functionality is no longer supported.

## Verify
- [ ] `gcloud domains registrations describe DOMAIN_NAME` shows the registration as active (check the output fields on your version).
- [ ] Auto-renew state matches intent.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed on the Cloud Domains overview, the register-domain page and the gcloud registrations reference page.
Removed: `get-authorization-code` (the group is `authorization-code`), the flags `--contact-data-from-file`,
`--contact-privacy`, `--yearly-price`, `--cloud-dns-zone` and `configure ... --transfer-lock-state`, the 15-day suspension claim, the DNSSEC DS
auto-publish claim and the lien-protection advice, none of which the cited pages state.
