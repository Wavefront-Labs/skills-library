---
id: computing-software.digital-privacy-hygiene.privacy-configuration.manual-data-broker-opt-outs
name: manual-data-broker-opt-outs
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, manual-broker-opt-out, data-brokers, people-search-opt-out, whitepages, spokeo, beenverified, opt-out-alias]
level: practitioner
status: draft
description: "Remove your listings from the major people-search sites by hand: find every profile, submit opt-outs with an alias email, track confirmations, and recheck for relisting."
sources:
  - "https://www.privacyguides.org/en/data-redaction/"
  - "https://github.com/yaelwrites/Big-Ass-Data-Broker-Opt-Out-List"
  - "https://cppa.ca.gov/data_broker_registry/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Manual data broker opt-outs

**Goal:** people-search sites sell your address, phone, relatives and age to anyone for a
few dollars. Opting out is free but tedious; do it in priority order.

## Prepare
- A dedicated **alias email** for opt-outs (brokers will email confirmation links; some
  resell submitted data, so don't use your main address).
- A tracking sheet: site, profile URL, date submitted, confirmation, recheck date.
- Never give more information than the form requires; avoid uploading ID unless the law
  requires the broker to accept less (often they don't need it).

## Order (US; start with sites that feed others)
1. Major people-search: Whitepages, Spokeo, BeenVerified (covers PeopleLooker etc.),
   Intelius family (Intelius, PeopleConnect, TruthFinder, Instant Checkmate), MyLife,
   Radaris, FastPeopleSearch, TruePeopleSearch, PeopleFinders, USPhoneBook.
2. Marketing/data aggregators: Acxiom, Epsilon, LexisNexis (consumer opt-out options vary).
3. Use the community-maintained opt-out list linked in sources for current URLs and steps.

## Per site
Search for yourself (name + state) > copy each matching profile URL > opt-out page > paste
URL / select records > alias email > click confirmation link > screenshot confirmation.
Repeat for each address/name variant (maiden names, old cities).

## Recheck
Listings reappear when brokers refresh data. Recheck every 3-6 months, or use a removal
service (see
`computing-software.digital-privacy-hygiene.privacy-configuration.evaluating-data-removal-services`).
California residents: the state DROP platform lets one request reach all registered brokers.

## Verify
- [ ] Top 10 sites show no listing when searched in a private window.
- [ ] Recheck reminders scheduled.
