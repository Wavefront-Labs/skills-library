---
id: computing-software.systems-network-administration.cisco-networking.acl-hit-counters-and-logging
name: acl-hit-counters-and-logging
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, acl, acl-counters, acl-log, log-input, clear-access-list-counters, ip-access-list-logging]
level: practitioner
status: docs-checked
description: "Verify which ACL entries match on IOS with hit counters, log and log-input ACEs, logging rate limits, and before/after counter comparisons during a change."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/access-lists/26448-ACLsamples.html
  - https://www.cisco.com/c/en/us/about/security-center/access-control-list-logging.html
  - https://www.cisco.com/c/en/us/support/docs/ip/access-lists/13608-21.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ACL hit counters and logging

## Counters
```
show access-list
clear ip access-list counters
```
`show access-list` prints each entry with its match count, for example `10 deny tcp any any eq 139 (10 matches)`.
`clear ip access-list counters` resets the counters, so a classification ACL can be re-read from zero.

Workflow for "is this rule used?": clear counters, wait a full business cycle (a week, month
end), recheck. Zero matches over a cycle = candidate for removal (see firewall rule review).
Counter values keep updating even when `ip access-list logging interval` is configured.

## Logging ACEs
The `log` and `log-input` options apply to a single ACE; `log-input` adds the ingress interface and source MAC
address to the logged source and destination addresses and ports.
```
ip access-list extended OUTSIDE-IN
 deny ip any any log-input
!
ip access-list log-update threshold 10
ip access-list logging interval 10
logging rate-limit 100 except 4
```
- `ip access-list log-update threshold N` sends an additional message after every N packets of a flow (a packet
  count, not a time interval); it is per flow and does not remove the initial message or the five-minute update.
- `ip access-list logging interval N` is in milliseconds and allows only one process-switched packet per
  interval for all log-enabled ACEs in all ACLs on all interfaces (10 ms = 100 packets per second). It needs CEF
  (`ip cef`) and has no IPv6 equivalent: IPv6 log-enabled ACEs are all process switched.
- `logging rate-limit 100 except 4` limits syslog generation to 100 messages per second except for severity 4 to 0;
  it applies to all syslog messages and does not reduce process switching, so use it together with the logging
  interval command.
- ACL logging can be CPU intensive: it process-switches matching packets and generates log messages. Use `log`
  only on low-rate entries, never on a busy permit.

Log line shape (log-input, IPv4 TCP): `%SEC-6-IPACCESSLOGP: list ACL-IPv4-E0/0-IN permitted tcp 192.168.1.3(1025) (Ethernet0/0 000e.9b5a.9839) -> 192.168.2.1(22), 1 packet`.
The message identifier changes with protocol (TCP/UDP `%SEC-6-IPACCESSLOGP`, ICMP `%SEC-6-IPACCESSLOGDP`,
IPv6 TCP/UDP `%IPV6-6-ACCESSLOGP`).
- The first matching packet logs immediately. Later packets with identical characteristics are counted and
  reported every five minutes; so are matches by any log-enabled ACE within one second of the initial message.

## Verify
- [ ] `show access-list` counters on the expected entries increase during a test.
- [ ] Deny-log entries are reviewed and the logging interval and syslog rate limit are in place.

## Checked
Date: 2026-11-07. Read in full: the ACL Logging security-center page (about 12k characters). The ACL samples page
(20k) was searched for log/log-input and counter commands; the Cisco IOS hardening guide (13608-21, 157k, added as a
source) was read only around the `show access-list` and `clear ip access-list counters` passages (lines near 1972-1991).
Confirmed: log vs log-input behaviour, five-minute update and one-second rule, identifiers, log-update threshold
(packets, per flow), logging interval (ms, one process-switched packet per interval, CEF needed, IPv4 only),
logging rate-limit syntax and example, CPU warning, `clear ip access-list counters`, `show access-list` match counts.
Removed: the claim that the logging interval is "ms between logged packets", the Catalyst TCAM counter claim and its
`show platform software fed ... acl counters hardware` command, the probe-ACE section (`no ip access-list extended
... 5` is not on any page), `show ipv6 access-list`, and the invented `logging buffered 64000` line (the page
uses `logging buffered informational`).
Method: documentation only; no commands were run.
