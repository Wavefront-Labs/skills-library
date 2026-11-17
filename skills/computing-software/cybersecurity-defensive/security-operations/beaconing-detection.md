---
id: computing-software.cybersecurity-defensive.security-operations.beaconing-detection
name: beaconing-detection
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [threat-hunting, beaconing-detection, c2-detection, network-analysis, jitter, proxy-logs, zeek, rita]
level: advanced
status: draft
description: "Hunt for command-and-control beaconing in proxy, firewall or Zeek data: interval regularity, jitter, data size consistency, and filtering legitimate polling software."
sources: ["https://github.com/activecm/rita", "https://www.activecountermeasures.com/threat-hunting-a-practical-guide/", "https://attack.mitre.org/techniques/T1071/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Beaconing detection

**Goal:** find implants checking in to C2 on a schedule, even with jitter and encrypted
traffic, using connection metadata.

## Signals
- **Regular intervals** between connections from one source to one destination (e.g. every
  60 s +/- 10%).
- **Consistent sizes** (request/response bytes similar each time).
- **Long duration**: pattern persists for hours or days, including outside working hours.
- **Rare destination**: few internal hosts talk to it; young domain; odd ASN.

## Splunk approach (proxy or firewall)
```
index=proxy earliest=-24h
| sort 0 src_ip dest_host _time
| streamstats current=f last(_time) as prev by src_ip dest_host
| eval delta=_time-prev | where isnotnull(delta)
| stats count avg(delta) as avg stdev(delta) as sd avg(bytes_out) as avg_out stdev(bytes_out) as sd_out dc(eval(strftime(_time,"%H"))) as hours by src_ip dest_host
| eval jitter=sd/avg, size_cv=sd_out/avg_out
| where count>50 AND jitter<0.2 AND hours>=12
| sort jitter
```
Then join destination prevalence: `| lookup` or a second stats `dc(src_ip) by dest_host`
and keep destinations with very few sources.

## Zeek + RITA
RITA (Real Intelligence Threat Analytics) imports Zeek conn/dns/http/ssl logs and scores
beacons on interval and size skew, dispersion and connection count:
```
rita import --logs /opt/zeek/logs/2026-10-15 --database day1015
rita view day1015          # beacons tab sorted by score
```
Scores near 1.0 deserve investigation; check DNS beacons (regular queries to subdomains)
and long connections too.

## Triage a candidate
Resolve process on the host (EDR network events by remote IP), check signer and path,
domain age and reputation, TLS certificate details/JA3/JA4, and whether other hosts beacon
to the same infrastructure.

## Gotchas
- Legitimate beacons are everywhere: AV/EDR updates, telemetry, NTP, chat apps, monitoring
  agents, Windows Update, SaaS sync clients. Maintain a filter list by destination domain
  and by process.
- Proxies that pool connections or CDNs fronting C2 blur destination; use SNI/Host header.
- Long-sleep implants (hours) need multi-day windows; heavy jitter (50%+) defeats simple
  stdev checks, so also look at regular daily counts.

## Verify
Run a controlled beacon in a lab (curl in a loop with sleep and random jitter) and confirm
the search or RITA ranks it near the top.
