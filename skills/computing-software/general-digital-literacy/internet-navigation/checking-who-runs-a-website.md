---
id: computing-software.general-digital-literacy.internet-navigation.checking-who-runs-a-website
name: checking-who-runs-a-website
category: computing-software
field: general-digital-literacy
product: internet-navigation
tags: [internet-navigation, evaluating-sources, website-ownership, whois, domain-age, about-page, company-registration]
level: intro
status: draft
description: "Work out who is behind a website using its About and contact pages, domain WHOIS and registration date, company registers, and archive history before trusting or buying."
sources:
  - https://lookup.icann.org/
  - https://web.archive.org/
  - https://find-and-update.company-information.service.gov.uk/
  - https://consumer.ftc.gov/articles/how-recognize-and-avoid-phishing-scams
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Check who runs a website

**Goal:** know whether a site is the real organisation, a reputable publisher, or a fake shop or propaganda outfit.

## On the site
- **About** page: named people, organisation, funding. Vague "we are passionate experts" with stock photos is a warning sign.
- **Contact:** a physical address, phone, company number (UK sites selling goods must show company details). Look the address up on a map.
- Legal pages: Terms, Privacy policy naming the company.

## Domain checks
- Read the domain carefully: `paypal.com.secure-login.xyz` belongs to `secure-login.xyz`.
- **WHOIS/RDAP:** lookup.icann.org › enter the domain › registration date and registrar. A shop registered three weeks ago selling discounted designer goods is a classic scam. Owner details are often privacy-protected (normal), but the **creation date** still shows.
- Official sites use predictable domains: `gov.uk`, `.gov`, `nhs.uk`, `ac.uk`, `.edu`.

## Off the site (lateral reading)
- Search the name plus "scam", "reviews", "Wikipedia". See what independent sources say.
- **Company registers:** Companies House (UK), state business registries/SEC EDGAR (US), OpenCorporates.
- **Wayback Machine** (web.archive.org): how long the site has existed and how it has changed.
- Trustpilot and similar: read the 1-star reviews and check for sudden bursts of 5-star ones.
- Online shop checkers: Get Safe Online's Check a Website; Scamadviser.

## Gotchas
- A padlock (HTTPS) only means the connection is encrypted; scam sites have padlocks too.
- Contact pages copied from real companies exist; call the number from an independent source.

## Verify
- [ ] Owner identified, domain age reasonable, independent sources confirm the organisation is real.
