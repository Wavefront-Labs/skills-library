---
id: computing-software.systems-network-administration.cisco-networking.eigrp-feasible-successors-and-variance
name: eigrp-feasible-successors-and-variance
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, eigrp, dual, successor, feasible-successor, feasibility-condition, feasible-distance, reported-distance, variance, unequal-cost-load-balancing, eigrp-topology, traffic-share]
level: advanced
status: docs-checked
description: "Use EIGRP DUAL deliberately: feasible distance vs reported distance, the feasibility condition, reading the topology table, and variance for unequal-cost load balancing."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/enhanced-interior-gateway-routing-protocol-eigrp/16406-eigrp-toc.html
  - https://datatracker.ietf.org/doc/html/rfc7868
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Feasible successors and variance

## Terms
- **Reported distance (RD)**: the neighbour's own metric to the destination.
- **Feasible distance (FD)**: my best metric to the destination.
- **Successor**: the neighbour on the best path; its route is used.
- **Feasibility condition**: a **feasible successor** is a path whose reported distance is less than the
  feasible distance.

EIGRP keeps each neighbour's advertisement in its topology table instead of discarding it. When the successor path
becomes unavailable, the router looks in the topology table for a feasible successor and, if it finds one, starts using
it immediately. If it finds none, it queries its neighbours.

## Read the topology table
```
show ip eigrp topology
show ip eigrp topology all-links
```
`show ip eigrp topology` shows only feasible successors; `all-links` shows all entries, including paths that fail the
feasibility condition.

## Variance (unequal-cost load balancing)
`variance` is a multiplier. Cisco's example uses variance 2 because a path with metric 1100 is balanced with a
path of 2200 (1100 x 2 = 2200). The path is used if it is a feasible successor and its metric is within
variance x best metric. A path whose reported distance is greater than the feasible distance is excluded whatever the
variance. The routing table then shows a traffic share count per path.

## Design note
Use **delay** to influence EIGRP path choice. EIGRP uses the interface bandwidth to set the rate at which it sends
packets, so bandwidth must be set correctly; do not use it to steer paths. At lower bandwidths bandwidth has more
influence on the total metric, at higher bandwidths delay has more.

## Verify
- [ ] `show ip eigrp topology` lists a feasible successor for each critical prefix.
- [ ] `show ip eigrp topology all-links` shows which paths fail the feasibility condition.

## Checked
Date: 2026-11-07. The Cisco EIGRP page (16406, about 100k characters) was searched by keyword and read around the
hits (DUAL overview, successor and feasible-successor text, variance and traffic share, delay and bandwidth guidance,
topology table change); it was not read cover to cover. RFC 7868 was searched for the feasibility condition and
terms only.
Confirmed: definitions of successor, feasible successor and the RD < FD condition, immediate use of a feasible
successor versus querying neighbours, `all-links`, variance as a multiplier with the 1100 x 2 = 2200 example, traffic
share count, exclusion of paths with RD above FD, delay (not bandwidth) for path steering.
Removed (not confirmed on the pages): the sample topology output and numbers (3072/2816, 5632 and the 35/65 split),
`traffic-share balanced`, `maximum-paths 4`, named-mode topology base syntax, the `| i` filter command, summarisation
and BFD convergence advice, the "tens of microseconds" delay unit on the interface, and the DUAL active/query log checks.
Method: documentation only; no commands were run.
