---
id: computing-software.systems-network-administration.cisco-networking.route-map-logic-and-continue
name: route-map-logic-and-continue
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, route-map, route-map-continue, match-set, implicit-deny, prefix-list, policy-routing]
level: practitioner
status: draft
description: "Write route-maps that do what you mean: permit/deny entries vs ACL permit/deny, AND/OR matching, implicit deny, set actions, continue clauses, and testing before applying."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/border-gateway-protocol-bgp/49111-route-map-bestp.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_pi/command/iri-cr-book/iri-cr-r1.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Route-map logic and continue

## Evaluation rules
1. Entries run in sequence order; the first entry whose match conditions are all true wins.
2. Entry type decides the outcome: `permit` = accept (and apply `set`), `deny` = reject.
3. Inside the match list (ACL/prefix-list), `permit` means "matches this entry", `deny` means
   "does not match", not "drop".
4. No entry matches: implicit deny at the end.
5. An entry with no `match` matches everything.

## AND vs OR
```
route-map X permit 10
 match ip address prefix-list A B       ! OR: A or B (same line)
 match community 10                      ! AND: (A or B) and community list 10
```

## Typical structure
```
ip prefix-list CUSTOMER seq 5 permit 198.51.100.0/24
ip prefix-list BOGONS seq 5 permit 10.0.0.0/8 le 32
route-map FROM-PEER deny 10
 match ip address prefix-list BOGONS
route-map FROM-PEER permit 20
 match ip address prefix-list CUSTOMER
 set local-preference 200
route-map FROM-PEER permit 30            ! accept the rest unchanged
```
Forgetting entry 30 drops everything else (implicit deny), a classic outage when applying a new
inbound policy.

## continue (BGP only)
Normally processing stops at the first match. `continue` jumps to another entry and keeps applying
sets:
```
route-map OUT permit 10
 match ip address prefix-list CUSTOMER
 set community 65001:100 additive
 continue 30
route-map OUT permit 20
 set community 65001:999 additive
route-map OUT permit 30
 match ip address prefix-list CUSTOMER
 set as-path prepend 65001 65001
```
If the target entry does not match, processing continues with the following entries. Last matching
permit/deny decides. Use sparingly; it makes policies hard to read.

## Test before applying
```
show route-map FROM-PEER                  ! policy routing matches counters
show ip bgp neighbors 203.0.113.1 received-routes   ! needs soft-reconfiguration inbound
show ip bgp route-map FROM-PEER           ! what the map selects from the current table
```
Apply with soft reset: `clear ip bgp 203.0.113.1 soft in`.

## Gotchas
- Referencing a non-existent prefix-list in a match: IOS treats it as match-all on some features,
  match-none on others. Create the list first.
- Route-maps in redistribution without an explicit final permit redistribute nothing else.
- Sequence gaps (10, 20, 30) leave space for inserts.

## Verify
- [ ] `show ip bgp neighbors x advertised-routes` / received routes match the intended policy.
