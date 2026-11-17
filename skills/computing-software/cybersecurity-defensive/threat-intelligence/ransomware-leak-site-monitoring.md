---
id: computing-software.cybersecurity-defensive.threat-intelligence.ransomware-leak-site-monitoring
name: ransomware-leak-site-monitoring
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [leak-site-monitoring, digital-risk-protection, ransomware, data-leak-sites, third-party-risk, threat-intelligence]
level: practitioner
status: draft
description: "Monitor ransomware data leak sites for your organisation, suppliers and peers: safe access, automation via trackers, verification of claims and response triggers."
sources: ["https://www.ransomware.live/", "https://www.cisa.gov/stopransomware", "https://www.ncsc.gov.uk/collection/ransomware"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Ransomware leak site monitoring

Ransomware groups publish victim names (and later data) on Tor-hosted leak sites to pressure payment.

## What to monitor
- Your organisation and subsidiaries/brands.
- Critical suppliers and customers (third-party breach early warning).
- Sector peers (trend and targeting intelligence).

## Methods
- Aggregators/trackers (ransomware.live, RansomLook, DRP and CTI vendors) that scrape leak sites and
  provide APIs/alerts; preferable to direct access.
- Direct access only from isolated infrastructure (Tor in disposable VMs), under policy; never download
  leaked data onto corporate systems without legal approval and controlled handling.
- Keyword alerts on organisation names, domains, and variants.

## Verifying claims
- Groups sometimes post false or exaggerated claims, re-post old breaches, or confuse similarly named
  companies. Check: data samples (file trees, screenshots) against your systems, timing vs known
  incidents, the group's credibility.
- Supplier listed: contact the supplier through known contacts, request confirmation and impact on
  your data (see supplier breach response).

## Response triggers
- Your organisation listed: activate incident response immediately (may be the first sign), engage
  counsel/insurer, preserve evidence, assess data exposure.
- Supplier listed: third-party breach process, credential rotation for integrations, data exposure
  assessment.
- Peer listed: check for shared vulnerabilities/vendors; hunt for the group's TTPs.

## Gotchas
- Countdown timers create pressure; decisions on contact/negotiation go through IR and legal, never
  ad hoc.
- Searching or sharing leaked personal data has legal implications.

## Verify
Alert pipeline test (synthetic match), documented triage outcomes for each hit, and supplier list
synced from vendor management.
