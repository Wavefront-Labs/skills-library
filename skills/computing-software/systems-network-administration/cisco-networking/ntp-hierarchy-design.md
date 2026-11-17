---
id: computing-software.systems-network-administration.cisco-networking.ntp-hierarchy-design
name: ntp-hierarchy-design
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ntp, ntp-pool, leap-second, leap-smearing, ntp-hierarchy, stratum, cisco-ios, time-design, ntp-architecture, rfc8633]
level: practitioner
status: docs-checked
description: "Design an NTP hierarchy from RFC 8633, NTP Pool and Cisco guidance: local servers, four diverse sources, pool etiquette, leap smearing rules and the panic threshold."
sources:
  - https://www.ntppool.org/en/use.html
  - https://datatracker.ietf.org/doc/html/rfc8633
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/bsm/configuration/xe-16/bsm-xe-16-book/bsm-time-calendar-set.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NTP hierarchy design

## Shape
- Stratum counts NTP hops from an authoritative source: stratum 1 has a reference clock attached, stratum 2 gets time
  from stratum 1, and so on. NTP never synchronises to a machine that is not itself synchronised, and does not sync to
  a machine whose time differs significantly from the others even at a lower stratum, which builds "a self-organizing
  tree of NTP servers" (Cisco guide).
- When many computers need time, RFC 8633 3.6 and the NTP Pool both advise running local NTP servers synchronised to the
  upstream and pointing everything else at them. The pool: "If you are synchronising a network to pool.ntp.org,
  set up one of your computers as a time server and synchronize the other computers to that one."
- RFC 8633 section 7 shows a hybrid design: stratum 1 servers at several sites, several stratum 2 servers per site
  taking time from them (and optionally peering with each other), clients at each site using a shared anycast address.
  Give each stratum 2 server a unique unicast address for monitoring.
- Cisco's IOS implementation does not support stratum 1 service (no radio or atomic clock; some platforms accept a GPS
  source) and recommends deriving network time from public NTP servers.

## Number and diversity of sources (RFC 8633 3.2-3.3)
- One source: any fault passes through. Two: if they disagree you cannot tell which is right. Three: tolerates one
  loss but then degrades to the two-source case. Four or more diverse sources is better.
- Operators who care about accuracy SHOULD use at least four independent, diverse sources; fewer is allowed (MAY) at
  the risks described.
- Diversity includes reference-clock type, vendor, chipset and firmware, since common bugs hit all. Satellite time
  can fail systemically (sunspot activity), so plan a backup scenario.
- Monitor all sources in use; if they disagree, investigate and stop using defective ones.

## Public pool etiquette
- Clients MUST only sync to servers they have permission to use (RFC 8633 3.6). The pool is volunteer-run with no
  guarantee. Do not depend on it if time errors can harm an organisation or human life; use local reliable service.
- Use `0` to `3.pool.ntp.org` or a continental or country zone (a country zone may hold only one or two servers).
  Names prefixed with `2` currently give IPv6 addresses as well as IPv4; the others give IPv4 only.
- Do not use more than four servers per config, and do not use burst or tweaked minimum poll.
- Vendors shipping devices can obtain their own pool subdomain.
- Control-message (mode 6) queries should be blocked from outside for public-facing servers (RFC 8633 3.4).

## Leap seconds (RFC 8633 3.7)
- Announced by IERS Bulletin C. A server that receives leap notification passes it on to clients. Leap indication is
  applied on the last day of the month; a server without that source can use a leap-seconds file from NIST, USNO or IERS.
- Leap smearing spreads the adjustment over a window (2 to 24 hours have been used successfully) so clocks can be
  offset from UTC by up to a full second but agree with each other. Operators with legal or strict UTC-traceability
  needs SHOULD NOT smear.
- Clients on smeared servers MUST NOT use standard leap handling (never load a leap file); smearing MUST NOT be used on
  public-facing servers. A client MUST NOT mix smeared and non-smeared servers, and all smeared servers a client uses
  must share the same smear configuration. The June 2015 event showed four-source clients failing for this reason.

## Cisco-side cautions
- Use `ntp master` with caution: easy to override valid sources, especially at low stratum; several that disagree
  cause instability (Cisco guide).
- Limit direct peer and client-server associations; syntax, authentication and access groups are covered in
  `computing-software.systems-network-administration.cisco-networking.ntp-client-server-and-authentication`.

## Panic threshold (RFC 8633 5.2)
RFC 5905 says offsets above 1000 s (PANICT) should make the client exit with a log message. Running a client that is
auto-restarted and ignores the panic threshold on every restart lets an attacker force a large step. Do not ignore the
threshold in all cold starts; monitor logs for panic exits and require manual intervention for large steps.

## Verify
- [ ] Each internal server has at least four independent sources, with no smeared/non-smeared mix.
- [ ] Devices sync to the internal servers only; the pool is touched only by the internal tier.
- [ ] Time sources are monitored and the logs are checked for panic and unsolicited NTP replies.

## Checked
Date: 2026-11-08
Method: documentation only; no commands were run. Read RFC 8633 sections 3.2-3.7, 5.2 and 7 (anycast hybrid design),
the NTP Pool "How do I use pool.ntp.org" page, and the Cisco Setting Time and Calendar Services chapter (stratum,
Cisco implementation limits, ntp master note). Removed as unconfirmed: the ASCII tier diagram with PTP/appliances,
named public providers other than the pool, the claim that Google and AWS smear, the 0.5 s disagreement figure, the
CGPM 2035 decision, the stratum-loop, NAT and VM warnings, and all IOS and chrony command lines and verify commands.
