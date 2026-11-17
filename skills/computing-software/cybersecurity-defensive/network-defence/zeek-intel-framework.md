---
id: computing-software.cybersecurity-defensive.network-defence.zeek-intel-framework
name: zeek-intel-framework
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [ids, zeek-intel-framework, zeek, intel-log, ioc-matching, threat-intel-feeds, critical-stack, network-ioc]
level: practitioner
status: docs-checked
description: "Match threat intel in Zeek with the Intel Framework: intel file format and indicator types, loading and updating feeds, seen locations, intel.log fields, and tuning."
sources: ["https://docs.zeek.org/en/master/frameworks/intel.html", "https://docs.zeek.org/en/master/scripts/base/frameworks/intel/main.zeek.html", "https://docs.zeek.org/en/master/scripts/policy/frameworks/intel/seen/__load__.zeek.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zeek Intelligence Framework

Zeek checks observed network values (IPs, domains, URLs, file hashes, certificate hashes, email
addresses) against loaded indicators and writes matches to `intel.log`.

## Load it (local.zeek)
```zeek
@load frameworks/intel/seen          # observation scripts (DNS, HTTP, TLS SNI, x509, files, smtp...)
@load frameworks/intel/do_notice     # optional: raise notices for indicators with meta.do_notice=T
redef Intel::read_files += { "/opt/zeek/intel/feed-ip.dat", "/opt/zeek/intel/feed-domain.dat" };
```

## Intel file format
Tab-separated with a header line (literal tabs required):
```
#fields	indicator	indicator_type	meta.source	meta.desc	meta.url	meta.do_notice
203.0.113.50	Intel::ADDR	misp-org1	Cobalt Strike C2	https://misp.local/events/view/42	T
evil-update.example	Intel::DOMAIN	misp-org1	Phishing domain	-	F
0123456789abcdef0123456789abcdef	Intel::FILE_HASH	vt	example hash	-	F
```
Types (see `Intel::Type`): `Intel::ADDR`, `Intel::SUBNET`, `Intel::DOMAIN`, `Intel::URL` (without `http://`),
`Intel::FILE_HASH`, `Intel::FILE_NAME`, `Intel::CERT_HASH`, `Intel::EMAIL`, `Intel::USER_NAME`, `Intel::SOFTWARE`,
`Intel::PUBKEY_HASH`. Fields containing only `-` are null.

## Updating
Zeek re-reads intel files when they change (input framework in REREAD mode). In a cluster the files only need to
exist on the manager. Generate the files from your TIP on a schedule, write atomically (temp file then rename), and
keep indicator expiry in the TIP so stale IOCs drop out.

## Reading intel.log
Fields: `seen.indicator`, `seen.indicator_type`, `seen.where` (e.g. `DNS::IN_REQUEST`,
`HTTP::IN_HOST_HEADER`, `SSL::IN_SERVER_NAME`, `Conn::IN_RESP`), `seen.node`, `matched`, `sources`, and `uid` to
pivot into conn/dns/http/ssl logs.
Prioritise by `seen.where`: a DNS lookup of a bad domain from a resolver differs from a client
completing a TLS session to it.

## Tuning
- Shared infrastructure IPs (CDNs, cloud) in feeds generate floods; filter in the TIP using warning lists.
- By default the seen scripts report IP addresses only for established TCP connections, so UDP and one-sided
  traffic (such as unanswered inbound scans) do not match `Intel::ADDR`; consider direction in SIEM correlation.
- Every loaded indicator sits in an in-memory store and more `Intel::seen` calls cost CPU; curate large feeds.

## Gotchas
- Fields must be separated by a single tab; spaces break parsing. Check `reporter.log` for intel read errors.
- URLs must match Zeek's normalised form (host + URI, no `http://`).

## Verify
Add a test domain indicator, run `dig` for it from a monitored host, and confirm an `intel.log` entry
with `seen.where` `DNS::IN_REQUEST` within the file-reread interval.

## Checked

Checked 2026-10-25 against the Zeek documentation and scripts (Zeek sources (zeek/zeek master, last pushed 2026-10-23: doc/frameworks, tools/zeek-cut, base and policy scripts, event definitions)). Confirmed: tab-separated intel file with `#fields` header and `-` for null, `Intel::read_files`, the `Intel::Type` members listed, `frameworks/intel/seen` and `frameworks/intel/do_notice` (the `meta.do_notice` field), input framework REREAD mode, `seen.where` values (`DNS::IN_REQUEST`, `HTTP::IN_HOST_HEADER`, `SSL::IN_SERVER_NAME`, `Conn::IN_RESP`, `Files::IN_HASH`), intel.log fields, URLs without the `http://` prefix. Corrected: address indicators match only established TCP connections by default; there is no `Intel::JA3` type in the base framework. Removed MISP and OpenCTI export remarks and the example hash line that named a test file.

Method: documentation only; no commands were run.
