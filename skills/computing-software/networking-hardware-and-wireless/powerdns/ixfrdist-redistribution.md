---
id: computing-software.networking-hardware-and-wireless.powerdns.ixfrdist-redistribution
name: ixfrdist-redistribution
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, ixfrdist, ixfr, axfr, zone-distribution, soa]
level: practitioner
status: docs-checked
description: "Use ixfrdist to pull zones from an authoritative server and redistribute them over AXFR and IXFR: command options, SOA polling, ACL checks and IXFR diff merging."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/manpages/ixfrdist.1.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ixfrdist

Options: `--help`, `--verbose` (INFO), `--debug` (INFO and DEBUG), `--version`, `--config <PATH>` (YAML file; default `ixfrdist.yml` in SYSCONFDIR).

Behaviour:
- Transfers zones from an authoritative server and re-serves them over AXFR and IXFR.
- Checks the SOA serial of every configured domain and downloads new versions to disk.
- Answers SOA queries from clients allowed by the ACL with the latest SOA it holds.
- Serves AXFR or IXFR when the client follows up the SOA query.
- For IXFR it combines all stored differences for the domain into one response.

Configuration lives in YAML (see the ixfrdist.yml skill). Related tool: `ixplore(1)`.

## Checked

2026-11-04. Read manpages/ixfrdist.1.rst in full and confirmed the options, the SOA, AXFR and IXFR behaviour, ACL check, IXFR condensing and the related ixplore(1) tool. Nothing removed.

Method: documentation only; no commands were run.
