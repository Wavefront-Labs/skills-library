---
id: computing-software.systems-network-administration.dns-dhcp.zonemaster-delegation-checks
name: zonemaster-delegation-checks
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, zonemaster, delegation-checks, dns-testing, dnssec]
level: practitioner
status: docs-checked
description: "Test a domain's delegation and zone health with Zonemaster (web, CLI, API): reading levels, common findings and fixing lame or inconsistent setups."
sources:
  - https://zonemaster.net/
  - https://github.com/zonemaster/zonemaster
  - https://github.com/zonemaster/zonemaster-cli
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zonemaster delegation checks

Zonemaster runs a test suite against a domain; the test plans in the project's specifications cover Basic, Address, Connectivity, Consistency, Delegation, DNSSEC, Nameserver, Syntax and Zone.

## Running
- Web: zonemaster.net, enter the domain (optionally undelegated test with proposed NS and DS).
- CLI: zonemaster-cli is available as a Docker image from the zonemaster organisation on Docker Hub (see the CLI README), or as a Perl package:
```
zonemaster-cli example.com
zonemaster-cli example.com --level NOTICE --ns ns1.new.net/192.0.2.53 --ns ns2.new.net
```
- `--ns` (a domain name, or `domain/IP`; a bare name is looked up in live DNS) and `--ds` (`keytag,algorithm,type,digest`, as in a zone file) provide information for an **undelegated test**: check new name servers before changing the registrar.

## Levels
The CLI `--level` option takes CRITICAL, ERROR, WARNING, NOTICE (the default), INFO, DEBUG, DEBUG2 or DEBUG3 and prints messages at that level or higher; treat CRITICAL and ERROR as must-fix and read WARNING and NOTICE messages.

## Typical findings and fixes (see the test specifications for exact test cases)
| Finding | Fix |
|---------|-----|
| Name servers on same AS/prefix | add a server on a different network |
| SOA serial differs between servers | secondaries not transferring |
| NS set at parent differs from child | align registrar delegation with apex NS |
| Glue missing/mismatched | correct registrar glue for in-bailiwick NS |
| Server not authoritative (lame) | remove or configure the zone there |
| No TCP response | allow TCP 53 |
| DS points to missing DNSKEY | update DS or restore key |
| Recursive name server | disable recursion on authoritative servers |

## Automate
Run the CLI in CI for zone changes or on a schedule for all domains, and fail the job when messages at ERROR or CRITICAL level appear (`--level ERROR` limits the output to those; `--json` gives machine-readable output).

## Verify
- [ ] Zonemaster reports no ERROR or CRITICAL messages for the domain (and for the undelegated test before migrations).

## Checked

Date: 2026-10-26. Documentation: zonemaster/zonemaster-cli (script/zonemaster-cli POD and lib/Zonemaster/CLI.pm) and zonemaster/zonemaster docs/public/specifications, read 2026-10-26. Confirmed: --level values and default NOTICE, --ns forms, --ds format, --json, test-plan names. Removed the unconfirmed sponsor names, hard-coded Docker image command, severity advice wording and the jq expression; the findings table is general DNS practice and is labelled as typical.

Method: documentation only; no commands were run.
