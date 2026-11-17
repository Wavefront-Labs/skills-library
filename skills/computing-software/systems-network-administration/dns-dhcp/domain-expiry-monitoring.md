---
id: computing-software.systems-network-administration.dns-dhcp.domain-expiry-monitoring
name: domain-expiry-monitoring
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, domain-expiry, rdap, whois, auto-renew, domain-portfolio]
level: practitioner
status: docs-checked
description: "Prevent domain expiry outages: RDAP expiry checks, ICANN expired-registration rules, renewal pitfalls, portfolio inventory and alerting."
sources:
  - https://www.icann.org/resources/pages/errp-2013-02-28-en
  - https://about.rdap.org/
  - https://www.rfc-editor.org/rfc/rfc9083
  - https://www.icann.org/resources/pages/epp-status-codes-2014-06-16-en
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Domain expiry monitoring

An expired domain can stop resolving: under ICANN's Expired Registration Recovery Policy the registrar must interrupt the registrant's existing DNS resolution path after expiry (to the extent the registry permits), which breaks web, email and API traffic together.

## Check expiry with RDAP
```
curl -Ls https://rdap.org/domain/example.com | jq -r '.events[] | select(.eventAction=="expiration") | .eventDate'
```
- RDAP replaces WHOIS with machine-readable, structured responses; rdap.org is a bootstrap endpoint that redirects to the authoritative RDAP service (404 if it knows none, for example some ccTLDs).
- RFC 9083 defines the `events` array; `expiration` is one of the defined `eventAction` values.
- rdap.org limits clients to 10 requests in 10 seconds (429 beyond that); for bulk checks use an RDAP client that reads the IANA bootstrap files.

## Alerting (practitioner advice)
- Keep an inventory of every domain, including defensive and ccTLD registrations, with registrar, owner and renewal mode.
- Run a scheduled check and alert well ahead of expiry; do not rely on registrar emails alone.
- Also watch registrar lock status, name server changes and the validity of contact email.

## ICANN gTLD expiry rules
- Registrars must send expiration reminders about one month and one week before expiry, and at least one more notice within five days after expiry if the registration is not renewed or deleted.
- Registrars may delete after expiry; the registrant must be allowed to renew from expiry onward, and the DNS path is interrupted for at least the last eight days the registration is renewable. Renewal restores the path.
- Non-sponsored gTLD registries offer a 30-day Redemption Grace Period after deletion, in which the registrar can restore it for the registrant (EPP status redemptionPeriod, then pendingDelete before the domain is purged and becomes available).
- Fees, grace and redemption terms vary by registrar and registry; read your registrar's terms.

## Auto-renew pitfalls (practitioner experience)
- Expired payment card, or the billing owner left the company.
- Registrar account in a personal name, with renewal mail going to a departed employee.
- Auto-renew switched off after a registrar transfer.

## Verify
- [ ] Every domain in the inventory has a monitored expiry date and a named owner, and a test alert fires.

## Checked
Method: 2026-11-09 documentation only; no commands were run. Read the ICANN Expired Registration Recovery Policy and EPP Status Codes pages, the about.rdap.org page and RFC 9083 (events/expiration). Removed as unsupported: the whois grep, Nagios/Prometheus exporter names, the 60/30/14/7 day thresholds, the 0-45 day auto-renew grace, 5-day pendingDelete as a fixed figure and the 10-year registration maximum. Alert and pitfall sections are practitioner advice.
