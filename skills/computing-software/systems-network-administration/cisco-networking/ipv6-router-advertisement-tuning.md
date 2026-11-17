---
id: computing-software.systems-network-administration.cisco-networking.ipv6-router-advertisement-tuning
name: ipv6-router-advertisement-tuning
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, ipv6, router-advertisement, slaac, managed-config-flag, rfc4861]
level: practitioner
status: docs-checked
description: "Tune IPv6 router advertisements with the RFC 4861 router variables: intervals, router lifetime, prefix lifetimes, L/A/M/O flags and their defaults."
sources:
  - https://datatracker.ietf.org/doc/html/rfc4861
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IPv6 router advertisement tuning

RFC 4861 section 6.2.1 defines the per-interface variables a router uses in Router Advertisements. Cisco IOS command
names and IOS defaults are not covered here (the Cisco page was unreadable); map each variable to the command in
your release's IPv6 configuration guide, and read the effective values from the device.

## Router variables (defaults are the RFC's)
| Variable | Rule | Default |
|---|---|---|
| MaxRtrAdvInterval | no less than 4 s, no greater than 1800 s | 600 s |
| MinRtrAdvInterval | no less than 3 s, no greater than 0.75 * MaxRtrAdvInterval | 0.33 * Max if Max >= 9 s, else Max |
| AdvDefaultLifetime (Router Lifetime) | zero, or between MaxRtrAdvInterval and 9000 s; zero means not a default router | 3 * MaxRtrAdvInterval |
| AdvManagedFlag (M) / AdvOtherConfigFlag (O) | placed in the RA flags; see address autoconfiguration | FALSE / FALSE |
| AdvLinkMTU | zero means no MTU option sent | 0 |
| AdvReachableTime | 0 = unspecified; at most 3,600,000 ms | 0 |
| AdvRetransTimer | 0 = unspecified | 0 |

Per advertised prefix:
| Variable | Rule | Default |
|---|---|---|
| AdvValidLifetime | all 1s (0xffffffff) = infinity; may be fixed or decrementing | 2592000 s (30 days), fixed |
| AdvPreferredLifetime | must not exceed AdvValidLifetime; all 1s = infinity | 604800 s (7 days), fixed |
| AdvOnLinkFlag (L) | on-link flag | TRUE |
| AdvAutonomousFlag (A) | SLAAC flag | TRUE |

- The default prefix list is every prefix the router advertises via routing protocols as on-link for that
  interface; the link-local prefix SHOULD NOT be included.
- AdvSendAdvertisements MUST be false by default so a node does not act as a router unless configured to.
- On point-to-point links the RFC allows the lifetime limits to be overridden by link-layer documents, since
  advertisements are needed less frequently.

## Design notes from the RFC variables
- A router that should stop being a default gateway advertises Router Lifetime zero.
- Preferred lifetime must not exceed valid lifetime.
- MaxRtrAdvInterval bounds the time between unsolicited multicast RAs, so a smaller value means more frequent RAs.

## Verify
Capture on a host and read the RA: interval between unsolicited RAs, Router Lifetime, prefix lifetimes, and the L, A,
M and O flags should match the intended variables.

## Checked
Checked 2026-11-08 against RFC 4861 section 6.2.1 (router configuration variables and defaults). Removed: IOS
command syntax and IOS defaults (about 200 s interval, 1800 s lifetime), suppression behaviour, router-preference,
Android DHCPv6 remark, and `show` and host tool commands, because the Cisco page returned 404 and the RFC does not
state them.
Method: documentation only; no commands were run.
