---
id: computing-software.systems-network-administration.cisco-networking.bgp-rpki-route-origin-validation
name: bgp-rpki-route-origin-validation
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, bgp, rpki-rov, route-origin-validation, rpki, roa, routinator, rtr, bgp-security]
level: practitioner
status: docs-checked
description: "Reason about RPKI route origin validation: RFC 6811 Valid/Invalid/NotFound rules, ROA maxLength, RTR cache timers (RFC 8210), and policy options for invalids."
sources:
  - https://www.rfc-editor.org/rfc/rfc6811
  - https://www.rfc-editor.org/rfc/rfc8210
  - https://routinator.docs.nlnetlabs.nl/en/stable/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RPKI route origin validation (ROV)

ROV checks that the AS originating a BGP route is authorised by the prefix holder. It validates the origin only: it
provides no path validation and does not stop AS-in-the-middle attacks, and an attacker who prepends the valid
source AS to a forged announcement defeats it. RFC 6811 says to think of it more as protection against
misconfiguration than as strong security.

## How a route is classified (RFC 6811)
A Validated ROA Payload (VRP) is (IP prefix, prefix length, maximum length, origin AS). The Route Origin ASN is the
rightmost AS in the final AS_PATH segment if it is an AS_SEQUENCE; the speaker's own AS if the path is empty or ends
in a confed segment; otherwise NONE.
- Covered: a VRP covers a route prefix when its length is less than or equal to the route's and the leading bits
  match (the route is identical to, or more specific than, the VRP prefix).
- Matched: covered, route prefix length less than or equal to the VRP maximum length, and route origin ASN equals
  the VRP ASN.
- **Valid**: at least one VRP matches. **Invalid**: at least one VRP covers but none matches. **NotFound**: no VRP
  covers the prefix.
- Consequences: a more-specific longer than every covering VRP's maximum length is Invalid even from the right AS,
  so set each ROA's maximum length to what you actually announce. AS 0 VRPs and a NONE origin never match.
- Validation state is a local attribute of the route, set for received UPDATEs (and SHOULD be for redistributed
  routes). A route not validated starts as NotFound. An implementation must not drop a route because of its state
  unless configured to.
- When VRPs change, affected prefixes must be re-validated and the decision process rerun.

## Policy (RFC 6811 section 5)
Implementations must let you match and set validation state in route policy. Options: reject Invalid routes, or lower
preference (for example LOCAL_PREF) by state. Considering Invalid routes in best-path selection is purely local
policy and should be done with utmost care. When preference is influenced by something not carried in iBGP, the
state may need propagating to iBGP peers, by setting a community or extended community on the sender and matching
it on the receiver. Blocking Invalid routes also creates a denial-of-service vector if an attacker can alter the
validation database.

## Getting data to routers
Routers do not validate certificates themselves: a validating cache (a Relying Party such as Routinator, which has a
built-in RTR server and an HTTP server with API endpoints and metrics) feeds them over the RPKI-to-Router protocol
(RFC 8210). Different caches or routers can hold different data at a given moment.
RTR timing parameters come from the cache in the End Of Data PDU:
- Refresh Interval: 1 to 86400 s, recommended default 3600 s. A Serial Notify PDU prompts an immediate query.
- Retry Interval: 1 to 7200 s, recommended default 600 s.
- Expire Interval: 600 to 172800 s, recommended default 7200 s; the router must not keep data past it, and the cache
  must set it larger than Refresh and Retry.
Transport options are SSH, TLS, TCP-MD5 and TCP-AO (RFC 8210 section 9). A router starts each connection with a
Reset Query or Serial Query.

## Operational consequences
- If every cache is unreachable, the data expires after the Expire Interval; with no VRPs, routes are NotFound (not
  Invalid), so traffic keeps flowing. Using two caches limits this.
- Enable dropping of Invalids only after your own and your customers' ROAs exist.
- Router-side commands (for example `bgp rpki server`, `match rpki`) differ by release; look up your platform's BGP
  configuration guide. This skill does not cover them.

## Checked
Checked 2026-11-08 against RFC 6811 (state definitions, VRP matching, policy, security considerations), RFC 8210
(timer ranges and defaults, transport list) and the Routinator home page (RTR and HTTP server). Removed: all IOS-XE
commands, Routinator CLI flags, ports, RIR portal steps, MANRS and looking-glass remarks, because the Cisco page
cited earlier returned 404 and the other pages do not state them.
Method: documentation only; no commands were run.
