---
id: computing-software.cybersecurity-defensive.threat-intelligence.threat-intel-feed-curation
name: threat-intel-feed-curation
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [threat-intelligence, ti-feeds, ioc-aging, misp, stix-taxii, confidence-scoring, feed-overlap, intel-requirements, false-positive-feeds, open-source-intelligence, commercial-feeds]
level: advanced
status: draft
description: "Curate threat intel feeds so they improve detection instead of flooding it: intel requirements, feed confidence/aging, de-duplication, and measuring whether a feed is actually earning its keep."
sources: ["MITRE - Structured Threat Information Expression (STIX) / TAXII public documentation", "SANS FOR578 - Cyber Threat Intelligence (public course outline)", "FIRST CTI SIG - intelligence requirements guidance"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Threat intel feed curation — more IOCs is not more security

**Goal:** run threat intelligence feeds so they sharpen detection with
high-confidence, relevant indicators — not flood the SIEM with stale or
irrelevant IOCs that either get ignored or drive the next alert-fatigue problem.

## 1. Start from intelligence requirements, not from "subscribe to everything"
Write down what you actually need intel *for*: which threat actors/malware
families target your industry and region, which of your technologies
(specific VPN, specific CMS, specific cloud provider) have had recent targeted
campaigns, and what decisions the intel feeds (block a domain? brief
leadership? patch urgently?). A feed chosen against stated requirements gets
used; a feed subscribed to because it was free or came bundled gets ignored or,
worse, auto-ingested and silently degrades your blocklist's signal quality.

## 2. Confidence and aging — not all IOCs deserve the same treatment
Tag every ingested indicator with source confidence (an analyst-verified IOC
from your own incident vs. a bulk open-source feed scrape) and a **decay/expiry**
policy — a malicious IP from a feed six months ago is very likely reassigned to
an innocent party by now (especially cloud/hosting IPs that churn constantly),
while a malware file hash remains valid indefinitely (hashes don't get
reassigned). Apply different expiry rules per indicator type: IPs and domains
decay fast (days to weeks for IPs tied to dynamic/cloud infrastructure), hashes
and YARA rules don't decay structurally but can go stale in relevance. An
auto-blocking feed with no expiry accumulates stale entries that eventually
block legitimate, reassigned infrastructure.

## 3. De-duplicate and reconcile overlapping feeds
Multiple feeds (open-source, commercial, ISAC/sector-specific) report heavily
overlapping indicators for the same campaigns, often with inconsistent
confidence labelling. Normalise into one platform (MISP or equivalent, speaking
STIX/TAXII where feeds support it) so the SIEM/firewall integration consumes one
reconciled list, not N separate raw feeds each with their own false-positive
rate and format quirks — duplicated ingestion wastes lookup/storage and
complicates attribution of which feed a hit came from.

## 4. Measure whether a feed is earning its keep
Track, per feed: how many of its indicators actually matched something in your
environment over a period, how many of those matches were true positives on
investigation, and how many false positives it caused (blocked something
legitimate). A feed with a high volume of indicators and near-zero true-positive
matches in your specific environment is a cost (ingestion, storage, lookup
latency) without a benefit — cut it or demote it to informational-only rather
than auto-blocking. This is the main lever against "we have 40 feeds" vendor
sprawl with no evidence any of them help.

## 5. Context over raw IOCs
A raw indicator with no context (what campaign, what TTPs, what's the
confidence) is far less useful than the same indicator linked to an ATT&CK
technique and a short analyst note — build or buy a platform that preserves
context alongside the indicator, and push context into the SIEM alert itself
(so an analyst triaging a hit sees "this IP is linked to campaign X using
technique T1059" not just "IP matched blocklist").

## Gotchas
- Auto-blocking on a feed with no confidence/expiry policy is how a legitimate,
  recently-reassigned IP gets silently blocked for your whole user base —
  always have a documented appeal/unblock path and don't auto-block the lowest
  confidence tiers.
- Attribution claims in commercial feeds vary widely in rigor — treat actor
  attribution as lower-confidence than the technical indicator itself unless the
  feed documents its methodology.
- A feed format mismatch (expects STIX 2.1, your platform parses 2.0) can fail
  silently, ingesting zero new indicators while the integration reports "healthy."
- Sharing intel back to an ISAC/community without first checking for sensitive
  internal context embedded in the indicator (internal hostnames, employee
  details in a phishing sample) is a data-leakage risk — sanitise before sharing.

## Verify
- [ ] Feeds are chosen against written intelligence requirements, not
      availability/cost alone.
- [ ] Every ingested indicator carries a confidence tag and an expiry policy
      appropriate to its type.
- [ ] Feeds are reconciled/de-duplicated into one platform before downstream use.
- [ ] Each feed's true-positive/false-positive rate in your environment is
      tracked and reviewed periodically.
- [ ] Auto-block actions have a documented, fast appeal/unblock path.

Related: computing-software.cybersecurity-defensive.threat-intelligence.attack-mapping-and-ioc-handling,
computing-software.cybersecurity-defensive.security-operations.threat-hunting-methodology,
computing-software.cybersecurity-defensive.network-defence.dns-security-and-sinkholing
