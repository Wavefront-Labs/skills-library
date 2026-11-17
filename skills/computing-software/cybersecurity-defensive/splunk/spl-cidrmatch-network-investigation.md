---
id: computing-software.cybersecurity-defensive.splunk.spl-cidrmatch-network-investigation
name: spl-cidrmatch-network-investigation
category: computing-software
field: cybersecurity-defensive
product: splunk
tags: [splunk, spl, cidrmatch, cidr-lookup, network-investigation, subnet-classification, ip-address, iplocation]
level: practitioner
status: draft
description: "Investigate network activity in Splunk with cidrmatch, CIDR lookups (match_type CIDR) and subnet classification to separate internal, partner and internet traffic."
sources: ["https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/ConditionalFunctions", "https://docs.splunk.com/Documentation/Splunk/latest/Knowledge/Addfieldmatchingrulestoyourlookupconfiguration", "https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/Iplocation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Network investigation with cidrmatch

## Inline classification
```
index=firewall action=allowed
| eval src_zone=case(cidrmatch("10.0.0.0/8",src) OR cidrmatch("172.16.0.0/12",src) OR cidrmatch("192.168.0.0/16",src),"internal",
                     cidrmatch("100.64.0.0/10",src),"cgnat", true(),"external")
| stats sum(bytes_out) as out by src_zone dest
```
`cidrmatch(cidr, ip)` returns a boolean; it works in `eval` and `where`, not as a bare search term.
In the base search, `src=10.0.0.0/8` also works (search-time CIDR matching on IP fields) and is
cheaper because it filters early.

## Many subnets: CIDR lookup
Inline lists do not scale. Build `subnets.csv` (`cidr,zone,owner,site`) and in `transforms.conf`:
```
[subnets]
filename = subnets.csv
match_type = CIDR(cidr)
max_matches = 1
```
Then `| lookup subnets cidr as src OUTPUT zone owner site`. Order rows most-specific first; with
`max_matches = 1` the first matching row wins. In ES, put subnets in the asset lookup instead so
notables get `src_category` and priority automatically.

## Investigation recipes
- Internal host to internet on unusual ports:
  `| where zone="internal" AND NOT cidrmatch("10.0.0.0/8",dest) AND NOT dest_port IN (80,443,53)`
- Find which IPs in an IOC range talked to you: `index=proxy dest_ip=203.0.113.0/24 | stats values(src) by dest_ip`
- Geolocate external peers: `| iplocation dest | stats dc(dest) by Country` (MaxMind lite DB, coarse).
- IPv6: `cidrmatch("2001:db8::/32", src)` works; normalise addresses (compressed forms) first.

## Gotchas
- Fields with ports (`10.1.1.1:443`) never match; split with `rex` first.
- `cidrmatch` with a non-IP string returns false, not an error; a renamed field silently breaks logic.
- `tstats` cannot run eval functions in `where`; filter with `where All_Traffic.src=10.0.0.0/8` instead.

## Verify
Spot-check: `| makeresults | eval t=cidrmatch("10.0.0.0/8","10.2.3.4")` returns `true`; reconcile
lookup zone counts against the IPAM subnet export.
