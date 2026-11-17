---
id: computing-software.digital-privacy-hygiene.privacy-configuration.self-search-audit-of-your-public-footprint
name: self-search-audit-of-your-public-footprint
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, self-doxxing-audit, digital-footprint, osint, reverse-image-search, google-dorks, username-search, name-monitoring, google-alerts]
level: practitioner
status: docs-checked
description: "Search for yourself the way a stalker or doxxer would: name, usernames, phone, address and face, record findings, prioritise removals, and set up ongoing alerts."
sources:
  - "https://ssd.eff.org/module/how-to-manage-your-digital-footprint"
  - "https://support.google.com/websearch/answer/4815696"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Self-search audit (self-doxxing)

**Goal:** know what's discoverable about you before someone hostile does. Method from EFF Surveillance Self-Defense,
"How to: Manage Your Digital Footprint" (last reviewed May 16, 2025).

## Baseline first
EFF: if a stalker or ex-partner can get into an important account they may reach the same private information, so
first use unique passwords (a password manager helps) and two-factor authentication. EFF also suggests Privacy
Badger and removing your phone's advertising ID.

## Search systematically (private browsing window or separate browser)
EFF recommends a private window or different browser so you are not logged into accounts (such as Google) that skew
results.
1. Your **name, nickname, handle and avatar** in a search engine.
2. Your **address, phone number and email addresses** directly.
3. **Usernames**: whatsmyname.app checks known usernames across social sites and also helps spot impersonation.
4. **Search operators** for deeper results: EFF points to Reporters Without Borders' guide for the list.
5. Deeper tools: OSINT Framework (EFF suggests its username, email address and social networks sections).
6. **People-search sites** that list address, phone and email, usually assembled by data brokers.
7. Optionally "doxx each other" with trusted friends or family, who may find data you forgot or consider harmless.

Do not be overwhelmed: EFF says finding more than expected is normal. Note which items are high priority and keep
track of what the information is and where you found it.

## Record and prioritise
Spreadsheet: URL, what it reveals (address, phone, family, workplace, photo), how to remove. Priority order is this
skill's suggestion: home address and phone first, then family members, workplace, photos, old posts.

## Act (EFF's steps)
- Data brokers: opt out (see
  `computing-software.digital-privacy-hygiene.privacy-configuration.manual-data-broker-opt-outs`). Yael Grauer's
  opt-out list is EFF's reference. Most sites require email confirmation and information repopulates, so repeat over
  the years. Paid services such as EasyOptOuts and Optery claim to help but cannot promise full coverage and may need
  ongoing subscriptions.
- Some US states offer address confidentiality programs ("Safe at Home") that act as a proxy address.
- Social accounts: list every account (a password manager helps), review each privacy setting, and make profiles
  private if not used for public communication.
- Google: use the "Results about you" page for notifications and to request removal of results with a phone number or
  address. If Google approves, the hosting site is not changed and the data can still be found on other search
  engines.

## Ongoing monitoring
Google Alerts emails you when new Search results match a topic (for example mentions of your name). In Google Alerts,
enter the topic, click Show options to set frequency, sources, region and which account receives it, then Create
Alert. Repeat the audit on a schedule you choose; EFF gives no interval.

## Verify
- [ ] Spreadsheet of findings with removal status.
- [ ] Alerts created for name, phone and address.

## Checked
Checked 2026-11-08 against the full text of the EFF guide and the Google Alerts help page. Removed unsupported
specifics: PimEyes and named reverse-image engines, the sample search strings, the 6-month interval and alias
delivery. Priority ranking is labelled as this skill's own. Google UI steps are as the help page words them.
Method: documentation only; no commands were run.
