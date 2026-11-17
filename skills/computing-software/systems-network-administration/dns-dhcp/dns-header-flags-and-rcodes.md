---
id: computing-software.systems-network-administration.dns-dhcp.dns-header-flags-and-rcodes
name: dns-header-flags-and-rcodes
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, dns-flags, rcode, dns-message-format, aa-flag, ad-bit, servfail, refused]
level: practitioner
status: verified
description: "Read DNS header flags (QR, AA, TC, RD, RA, AD, CD) and RCODEs (NOERROR, NXDOMAIN, SERVFAIL, REFUSED, FORMERR, NOTIMP) and know what each combination says about the server."
sources:
  - https://www.rfc-editor.org/rfc/rfc1035#section-4.1.1
  - https://www.iana.org/assignments/dns-parameters/dns-parameters.xhtml#dns-parameters-6
  - https://www.rfc-editor.org/rfc/rfc4035#section-3.2
  - https://www.rfc-editor.org/rfc/rfc8914
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DNS header flags and RCODEs

## Flags (dig prints them on the `;; flags:` line)
| Flag | Set by | Meaning |
|---|---|---|
| qr | responder | this is a response |
| aa | authoritative server | answer comes from the zone itself, not cache |
| tc | responder | truncated; retry over TCP |
| rd | client | recursion desired |
| ra | responder | recursion available (this server will recurse for you) |
| ad | validating resolver | answer DNSSEC-validated (only meaningful from a resolver you trust) |
| cd | client | checking disabled: give me data even if validation fails |

## RCODEs
| Code | Name | Typical meaning |
|---|---|---|
| 0 | NOERROR | success (an empty answer section with a SOA in the authority section = NODATA) |
| 1 | FORMERR | server could not parse the query (EDNS/option problem, broken middlebox) |
| 2 | SERVFAIL | server failed: upstream unreachable, DNSSEC validation failure, lame delegation, zone not loaded |
| 3 | NXDOMAIN | name does not exist (authoritative denial) |
| 4 | NOTIMP | query type/opcode not implemented |
| 5 | REFUSED | policy: recursion not allowed for you, zone not served, ACL |
Extended DNS Errors (RFC 8914, EDNS option code 15, shown as `EDE` by tools that decode it) add
detail such as `DNSSEC Bogus` (6), `Stale Answer` (3), `Network Error` (23) and `Prohibited` (18).
Only servers that implement and enable EDE send them (Unbound: `ede: yes`, default no), so check
your resolver's documentation. RCODE 23 is `BADCOOKIE` (RFC 7873), seen only with DNS cookies.

## Reading combinations
```
dig @ns1.example.net www.example.net +norec
```
- `flags: qr aa` NOERROR with an answer: authoritative and correct.
- `flags: qr` (no aa), NOERROR, empty answer and NS records in the authority section: a referral
  (delegation) from a parent.
- `flags: qr rd` with `status: REFUSED` from an authoritative server you asked recursively: it
  correctly refuses to recurse.
- `flags: qr rd ra ad`: a validating resolver returned DNSSEC-validated data.
- `SERVFAIL` from a resolver but `+cd` works: DNSSEC validation failure (check with `delv`).
- `aa` missing on a server that should be authoritative: zone not loaded (expired secondary,
  syntax error), so it answers from cache or refers.

## Reading them without dig
```python
import dns.message, dns.query, dns.flags, dns.rcode   # dnspython 2.x
r = dns.query.udp(dns.message.make_query("www.example.net", "A"), "192.0.2.53", timeout=3)
print(dns.flags.to_text(r.flags), dns.rcode.to_text(r.rcode()))   # e.g. "QR AA RD NOERROR"
```
Against a local authoritative server (CoreDNS 1.15 serving a zone) this printed `QR AA RD NOERROR`
for an existing name, `NOERROR` with an empty answer and a SOA for a missing type, `NXDOMAIN` for a
missing name, `QR RD REFUSED` for a zone it does not serve, and `QR RD NOERROR` with only NS records
in the authority section for a delegated child.

## Verify
- [ ] For a DNS ticket, record the server queried, flags, status and EDE text for each hop
  (resolver, then each authoritative server with +norec).
