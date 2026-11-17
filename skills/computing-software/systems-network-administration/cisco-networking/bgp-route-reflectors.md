---
id: computing-software.systems-network-administration.cisco-networking.bgp-route-reflectors
name: bgp-route-reflectors
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, bgp, route-reflector, ibgp, cluster-id, originator-id, cluster-list, full-mesh, rfc-4456]
level: practitioner
status: docs-checked
description: "Replace an iBGP full mesh with route reflectors per RFC 4456: clients and non-clients, reflection rules, redundant RRs and CLUSTER_ID, loop attributes, best-path caveats."
sources:
  - https://www.rfc-editor.org/rfc/rfc4456
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP route reflectors (RFC 4456)

Without reflection, every iBGP speaker in an AS must be fully meshed: n speakers need n*(n-1)/2 iBGP sessions. A route reflector (RR) is a BGP speaker that advertises iBGP-learned routes to other iBGP peers (a reflected route), so clients need not be fully meshed.

## Concepts
- The internal peers of an RR are client peers or non-client peers. An RR along with its clients forms a cluster.
- Non-client peers must be fully meshed; client peers need not be.
- The protocol gives a client no way to identify itself dynamically, so RR-to-client roles are set by manual configuration.
- Conventional BGP speakers that do not understand route reflection can be clients or non-clients, which allows gradual migration: start with one designated RR and add clusters over time.
- An RR treats other RRs like any other internal BGP speaker; they can be configured as clients or non-clients. In the simple design each cluster's RRs are non-clients of each other (fully meshed) and clients peer only with the RR of their cluster.

## Reflection rules
After the RR selects its best path:
- Route from a non-client iBGP peer: reflect to all clients.
- Route from a client peer: reflect to all non-client peers and also to the other clients.

(RFC 4456 specifies reflection only for iBGP-learned routes; it does not restate how eBGP routes are advertised.)

## Redundancy and loop prevention
- A cluster usually has a single RR and is identified by that RR's BGP Identifier. For multiple RRs in the same cluster, give all of them the same 4-byte CLUSTER_ID so an RR can discard routes from other RRs in the same cluster. The RFC notes a single RR is a single point of failure.
- ORIGINATOR_ID: optional non-transitive attribute, type 9, 4 bytes, created by the RR when reflecting and carrying the BGP Identifier of the route's originator in the local AS. A speaker should not create one if it already exists. A router should ignore a route received with its own BGP Identifier as ORIGINATOR_ID.
- CLUSTER_LIST: optional non-transitive attribute, type 10, a sequence of CLUSTER_ID values. A reflecting RR must prepend its local CLUSTER_ID (creating the list if empty). If the local CLUSTER_ID is already in the list, the advertisement should be ignored.

## Best path and attributes
- Tie-breaking changes: if a route carries ORIGINATOR_ID it is treated as the BGP Identifier of the advertising speaker, and a speaker should prefer the shorter CLUSTER_LIST (length zero when absent), inserted between steps f) and g) of the RFC 4271 decision process.
- An RR should not modify NEXT_HOP, AS_PATH, LOCAL_PREF or MED when reflecting, and the loop-prevention attributes must not be modifiable by configuration between RRs, clients and non-clients.
- The RR reflects only its best path, so reflection may not give the same selection as a full iBGP mesh when MEDs are incomparable or IGP metrics differ between the RR and its clients. The RFC suggests keeping intra-cluster IGP metrics better than inter-cluster metrics with a full mesh inside the cluster, and handling MEDs by setting local preference at the border router, making AS-path lengths differ, or using community-based policy.
- Make the reflection topology congruent with the network topology when multiple paths exist. A commonly used design is one set of RRs per point of presence, with all RRs fully meshed.

## Vendor configuration
This skill does not give Cisco IOS commands (route-reflector-client, bgp cluster-id and similar): the Cisco configuration page originally cited could not be read. Take syntax from the Cisco BGP command reference for your release.

## Verify
- [ ] Every client has a session to each RR serving it and receives the expected prefixes.
- [ ] A reflected route on a client carries ORIGINATOR_ID and a CLUSTER_LIST that includes the RR's cluster ID.

## Checked
Date: 2026-11-08. Read in full: RFC 4456 (about 22k characters).
Confirmed: full-mesh formula, client/non-client terminology, cluster definition, manual client configuration, reflection rules from non-client and client, coexistence with conventional speakers, CLUSTER_ID for redundant RRs, ORIGINATOR_ID and CLUSTER_LIST types and handling, decision-process modification, attributes an RR should not modify, best-path-only and IGP/MED caveats, POP-based design.
Removed: all Cisco IOS configuration (the cited Cisco page returns 404), the "from eBGP" reflection rule, the claim that unique cluster IDs are modern practice and that same-ID RRs lose client paths, next-hop-self advice, add-path, `bgp bestpath igp-metric ignore`, `table-map`/`no-fib` options and the show command example.
Method: documentation only; no commands were run.
