---
id: computing-software.digital-forensics-incident-response.log-analysis.siem-lookups-and-watchlists-for-enrichment
name: siem-lookups-and-watchlists-for-enrichment
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [siem-lookups, watchlists, enrichment, splunk-lookups, sentinel-watchlists, dfir]
level: practitioner
status: draft
description: "Use SIEM lookups and watchlists to enrich investigations: IOC lists, asset and identity context, VIP and crown-jewel tagging in Splunk lookups, Sentinel watchlists and Elastic enrich."
sources: ["https://docs.splunk.com/Documentation/Splunk/latest/Knowledge/Aboutlookupsandfieldactions", "https://learn.microsoft.com/en-us/azure/sentinel/watchlists", "https://www.elastic.co/guide/en/elasticsearch/reference/current/ingest-enriching-data.html", "https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/Inputlookup"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SIEM lookups and watchlists for enrichment

Raw events say "user jdoe logged on to host FIN-SRV-02 from 198.51.100.7". Lookups add: jdoe is a domain admin, FIN-SRV-02 is a crown jewel, the IP is a known VPN exit for the attacker. Enrichment turns hours of manual pivoting into one query.

## What to load
| List | Columns | Use |
|---|---|---|
| Incident IOCs | indicator, type, first_seen, case_id, confidence | Sweeps and detections during the incident |
| Assets | hostname, IP, owner, criticality, role, location | Severity scoring, scoping |
| Identities | user, department, manager, privileged flag, leaver date | Insider and privileged-use context |
| Known-good | service accounts, scanner IPs, admin jump hosts | False-positive suppression |
| Compromised accounts / hosts | entity, compromise time, remediated time | Watch post-remediation activity |

## Splunk
```spl
| inputlookup case_iocs.csv                                     ``` inspect the list
index=proxy [| inputlookup case_iocs.csv where type="domain" | rename indicator AS dest_host | fields dest_host]
index=wineventlog EventCode=4624 | lookup assets.csv hostname AS ComputerName OUTPUT criticality owner
```
Lookup definitions with `time_field` support temporal lookups (e.g. DHCP IP-to-host at a point in time). KV-store lookups suit frequently updated lists.

## Microsoft Sentinel watchlists
Upload CSV (or create via API); query with `_GetWatchlist('alias')`:
```kql
let iocs = _GetWatchlist('case_iocs') | where Type == "ip" | project IP = SearchKey;
CommonSecurityLog | where DestinationIP in (iocs)
```
`SearchKey` is the indexed column for joins. Watchlists have size limits for direct upload; use Azure Storage for large lists.

## Elastic
Enrich policies (`match`, `geo_match`, `range`) execute into enrich indices, used by the `enrich` ingest processor at index time or `ENRICH` in ES|QL at query time.

## Practice
- Keep lists in version control or a managed source, with an owner and update time; stale asset lists mislead.
- Expire IOCs (IPs especially) with a review date.
- Use enrichment in detections to raise severity on crown jewels and privileged users.

## Gotchas
- Case-sensitivity and formatting mismatches (FQDN vs short hostname, UPN vs sAMAccountName) cause silent non-matches; normalise.
- Index-time enrichment freezes the value at ingest; query-time reflects current values; know which you need for historical questions.

## Verify
A known indicator from the list returns its test event in the sweep query, and asset/identity enrichment fields populate for a sample of events.
