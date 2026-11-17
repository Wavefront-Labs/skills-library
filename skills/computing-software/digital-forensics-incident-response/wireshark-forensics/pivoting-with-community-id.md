---
id: computing-software.digital-forensics-incident-response.wireshark-forensics.pivoting-with-community-id
name: pivoting-with-community-id
category: computing-software
field: digital-forensics-incident-response
product: wireshark-forensics
tags: [community-id, zeek, suricata, network-security-monitoring, dfir]
level: practitioner
status: docs-checked
description: "Use Community ID flow hashing to pivot between Zeek, Suricata and other monitor records of the same connection: how the hash works, how to enable it, and the seed and NAT gotchas."
sources: ["https://github.com/corelight/community-id-spec", "https://docs.zeek.org/en/master/scripts/policy/protocols/conn/community-id-logging.zeek.html", "https://docs.suricata.io/en/latest/output/eve/eve-json-output.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pivoting with Community ID

**Goal:** the same flow appears in Zeek `conn.log`, Suricata EVE records and other monitors with
different field names and IDs. Community ID gives every tool the same string for the same
flow so the pivot is a string comparison.

## The hash
Version 1 is `1:` plus the base64 of SHA1 over seed, source address, destination address,
protocol, a zero pad byte, source port and destination port. The endpoints are ordered so both
directions hash identically (numerically smaller IP:port first; ports decide if the addresses
are equal). The seed defaults to 0 and is an unsigned 16-bit value. ICMP uses type and code
in place of ports.

## Enable
- **Zeek**: load `policy/protocols/conn/community-id-logging` (`@load policy/protocols/conn/community-id-logging`);
  it adds a `community_id` string field to the conn log.
- **Suricata**: set `community-id: true` in the eve-log output section of `suricata.yaml`
  (default false); optional `community-id-seed`. Records then carry `community_id`.
- Other implementations are listed in the spec repository (pycommunityid for Python,
  Elastic Beats and Elasticsearch processor, Security Onion, and more); check each for support.

## Workflow
1. Suricata alert: copy `community_id`.
2. Search Zeek logs (or your SIEM) for the same value to get the `uid`, then every protocol
   log for that connection.
3. Use the same value in any other tool that records it to retrieve PCAP or find the process.

## Gotchas
- NAT changes the tuple: hashes differ on each side of a NAT boundary; compute at a consistent
  observation point.
- The seed must be the same value on all tools that output the ID.
- The ID includes a version number; do not compare IDs from different versions.

## Verify
One flow is found in at least two tools via its Community ID with matching timestamps and byte counts.

## Checked
2026-11-01. Confirmed in the Community ID spec (hash inputs and order, seed default, version
prefix, endpoint ordering, ICMP handling, implementation list), the Zeek script page
(`community_id` field on conn) and the Suricata EVE page (`community-id` boolean default false,
`community-id-seed`, `community_id` output, seed must match across tools). Removed: Wireshark
GUI menu path and `communityid` filter, Arkime and EDR claims, the `pip install` command and
sample hash line, none of which the fetched pages confirm.
Method: documentation only; no commands were run.
