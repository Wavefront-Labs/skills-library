---
id: computing-software.digital-privacy-hygiene.privacy-configuration.california-delete-act-drop-requests
name: california-delete-act-drop-requests
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, california-delete-act, data-brokers, drop, cppa, data-broker-registry]
level: intro
status: docs-checked
description: "Use California's DROP platform to send one deletion request to registered data brokers, and know to keep using manual opt-outs for everything else."
sources:
  - "https://cppa.ca.gov/data_broker_registry/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# California Delete Act DROP requests

**Goal:** California residents can make one request that reaches registered data brokers, instead of many
separate opt-outs.

## Background
- The California Privacy Protection Agency (CPPA) runs the **Delete Request and Opt-out Platform (DROP)**.
- The CPPA's registry page states that since 1 January 2026 California residents may use DROP to submit one
  request to all active data brokers.
- Brokers register annually (the registry page gives 1-31 January) and the CPPA publishes the **Data Broker
  Registry**.

## Submit
1. Reach DROP through the links on the CPPA site and follow its residency verification.
2. Read the CPPA's DROP pages for exactly which identifiers it asks for and how matching works; give what it
   requests.
3. Keep the confirmation and check the CPPA pages for how broker responses are reported.

## Limits
- DROP covers registered data brokers only. Companies you deal with directly are first parties; use their own
  deletion tools.
- Check the CPPA pages for what categories of data are excluded and how often brokers must process requests.
- For sites that are not registered, keep using each site's own opt-out.

## Non-Californians
Use each broker's opt-out, any privacy-law requests your own state allows, or a removal service.

## Verify
- [ ] DROP request submitted and confirmation saved.
- [ ] People-search sites spot-checked again after a few weeks.

## Checked
2026-11-01. Confirmed against the CPPA Data Broker Registry page: DROP exists, residents can submit one request to
all active data brokers from 1 January 2026, brokers register annually in January. Removed as unconfirmed: the
SB 362 citation details, the August 2026 processing start, the 45-day re-check, hashing of identifiers, specific
exemptions and state lists, the 60-90 day recheck, and the other source URLs (not read).
Method: documentation only; no commands were run.
