---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.zeek-intelligence-framework
name: zeek-intelligence-framework
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [zeek-intel-framework, zeek, ioc-matching, intel-log, network-forensics, dfir]
level: practitioner
status: docs-checked
description: "Match incident IOCs in Zeek with the Intelligence Framework: intel file format and types, loading via Intel::read_files, seen policies, intel.log fields and replaying old pcaps."
sources: ["https://docs.zeek.org/en/master/frameworks/intel.html", "https://docs.zeek.org/en/master/scripts/base/frameworks/intel/main.zeek.html", "https://docs.zeek.org/en/master/scripts/policy/frameworks/intel/seen/__load__.zeek.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zeek Intelligence Framework

The Intel framework matches indicators against what Zeek sees (addresses, subnets, domains, URLs, file hashes and names, certificate hashes, emails, user names, software) and writes hits to `intel.log`. During an incident it turns new IOCs into live network detection and lets you retro-scan stored pcaps.

## Intel file format
Tab-separated with a header line (tabs, not spaces):
```text
#fields	indicator	indicator_type	meta.source	meta.desc	meta.do_notice
203.0.113.50	Intel::ADDR	case-2026-0147	Cobalt Strike team server	T
bad-update.example	Intel::DOMAIN	case-2026-0147	stage-2 host	T
bad-update.example/dl/a.bin	Intel::URL	case-2026-0147	payload URL (no scheme)	F
5d41402abc4b2a76b9719d911017c592	Intel::FILE_HASH	case-2026-0147	loader md5	T
```
Types include `Intel::ADDR`, `Intel::SUBNET`, `Intel::DOMAIN`, `Intel::URL` (without `http://`), `Intel::EMAIL`, `Intel::USER_NAME`, `Intel::FILE_HASH`, `Intel::FILE_NAME`, `Intel::CERT_HASH`, `Intel::PUBKEY_HASH`, `Intel::SOFTWARE`.

## Loading
In `local.zeek`:
```zeek
@load frameworks/intel/seen
@load frameworks/intel/do_notice
redef Intel::read_files += { "/opt/zeek/intel/case-2026-0147.intel" };
```
`frameworks/intel/seen` loads the scripts that feed observations (DNS queries, HTTP hosts and URLs, TLS SNI and certs, SMTP addresses, file hashes) into the framework. Files are re-read when changed (input framework in REREAD mode), so you can append IOCs without restarting.

## Reading hits
`intel.log` fields: `ts`, `uid`, `id.*`, `seen.indicator`, `seen.indicator_type`, `seen.where` (e.g. `DNS::IN_REQUEST`, `HTTP::IN_HOST_HEADER`, `SSL::IN_SERVER_NAME`, `Files::IN_HASH`), `matched`, `sources`. Join to `conn.log` and protocol logs by `uid` for context.

## Retro-scanning stored pcaps
Put the `@load` and `redef Intel::read_files` lines from above into a small script (for example `case-intel.zeek`) and run:
```bash
zeek -C -r old_capture.pcap local case-intel.zeek
```
`-C` ignores checksum errors common in captures. Run over each historical pcap (each in its own output directory, since logs are overwritten) to find earlier contact with new IOCs.

## Gotchas
- File hashes only match if Zeek hashed the file (`frameworks/files/hash-all-files` loaded) and saw it unencrypted.
- By default the seen scripts report IP addresses only for established TCP connections, so UDP and one-sided traffic never match an `Intel::ADDR` entry.
- Fields must be separated by a single tab (a lone `-` is null); spaces break parsing. Check `reporter.log` for parse errors.

## Verify
A test indicator (a domain you resolve deliberately from a lab host) appears in `intel.log` with the expected `seen.where`, before relying on absence of hits.

## Checked

Checked 2026-10-25 against the Zeek documentation and scripts (Zeek sources (zeek/zeek master, last pushed 2026-10-23: doc/frameworks, tools/zeek-cut, base and policy scripts, event definitions)). Confirmed: tab-separated format with `#fields` header, the `Intel::Type` members, `Intel::read_files`, `frameworks/intel/seen`, `frameworks/intel/do_notice`, REREAD mode, the `seen.where` values listed, intel.log fields, `frameworks/files/hash-all-files` for file hash matching. Corrected: address matching covers established TCP connections only; the command line `redef` form for retro scans was replaced by a script file. Removed the user agent indicator type (not an `Intel::Type`) and the unconfirmed subdomain matching claim.

Method: documentation only; no commands were run.
