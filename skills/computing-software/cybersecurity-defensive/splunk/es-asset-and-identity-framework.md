---
id: computing-software.cybersecurity-defensive.splunk.es-asset-and-identity-framework
name: es-asset-and-identity-framework
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, splunk-enterprise-security, asset-and-identity, asset-lookup, identity-lookup, priority, enrichment, risk-based-alerting]
level: advanced
status: draft
description: "Populate the Splunk Enterprise Security asset and identity framework: lookup sources, field formats, merge settings and how priority drives urgency."
sources: ["https://docs.splunk.com/Documentation/ES/latest/Admin/Addassetandidentitydata", "https://docs.splunk.com/Documentation/ES/latest/Admin/Formatassetoridentitylist", "https://docs.splunk.com/Documentation/ES/latest/User/Howurgencyisassigned"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ES asset and identity framework

**Goal:** every notable and risk event in Splunk Enterprise Security shows who owns the
host, who the user is, and how much it matters, so urgency is calculated rather than guessed.

## 1. Build the source lists
Assets (CSV or a scheduled search writing a lookup), header fields ES expects:
`ip, mac, nt_host, dns, owner, priority, lat, long, city, country, bunit, category, pci_domain, is_expected, should_timesync, should_update, requires_av`
Identities:
`identity, prefix, nick, first, last, suffix, email, phone, managedBy, priority, bunit, category, watchlist, startDate, endDate, work_city, work_country`
- `identity` may be pipe-delimited aliases: `asmith|alice.smith|alice.smith@example.com`.
- `priority`: `unknown, low, medium, high, critical`. Reserve critical for tier-0 (DCs,
  PKI, identity providers) and executives/admins.
- `category` is pipe-delimited free text (`pci|web|dmz`) usable in correlation searches.
Feed them from authoritative systems on a schedule: CMDB/EDR inventory for assets, AD or
the HR system for identities (`| ldapsearch` from SA-ldapsearch, or an HR export).

## 2. Register in ES
Configure > Data Enrichment > Asset and Identity Management: add each lookup as a source,
set the source type (asset or identity) and order/precedence. Merge settings decide whether
records with the same key from different sources combine (enable for asset `ip`/`dns` and
identity email conversion).
Identity matching options: enable email and "convert to short form" if logs show
`DOMAIN\user` in some sources and `user@domain` in others.

## 3. How it is used
- Automatic lookups add `src_priority`, `dest_owner`, `user_bunit` etc. to events.
- Notable urgency = event severity x asset/identity priority (matrix in
  Configure > Incident Management). An informational event on a critical asset is "medium".
- Risk-based alerting multiplies risk scores by priority via the risk modifier.

## Gotchas
- Huge asset lists with CIDR ranges and overlapping entries slow every search; keep CIDR
  entries for network zones only and individual hosts for known assets.
- Stale identities (leavers) still match; use `endDate` and remove after retention.
- DHCP churn makes IP-keyed assets wrong; key workstations by `nt_host`/`dns`.
- After changes, the merge search runs on schedule; check
  `| inputlookup asset_lookup_by_str | head` rather than assuming.

## Verify
```
| from datamodel:"Identity_Management.All_Assets" | stats count by priority
index=notable | stats count by urgency, dest_priority
```
Test with a known DC IP: a notable on it should carry `dest_priority=critical` and the
right owner.
