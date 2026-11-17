---
id: computing-software.systems-network-administration.network-design.bgp-hijacking-and-route-leaks
name: bgp-hijacking-and-route-leaks
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-attacks, bgp-hijacking, route-leak, rpki, irr-filtering, bgp-monitoring, manrs]
level: practitioner
status: docs-checked
description: "Defend prefixes against BGP hijacks and leaks: ROAs and IRR objects, monitoring and alerting, customer and peer filtering, and a response playbook."
sources:
  - https://www.manrs.org/netops/guide/
  - https://www.rfc-editor.org/rfc/rfc7908
  - https://bgp.tools/kb/api
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP hijacking and route leaks

- Hijack: someone originates your prefix (or a more specific) without authorisation.
- Route leak (RFC 7908): an AS propagates routes beyond their intended scope (e.g. re-advertising
  a provider's full table to another provider), pulling traffic through it.

## Prevent
1. RPKI ROAs for every announced prefix, with a max length no looser than what you announce.
2. IRR route objects (RADB or RIR IRR) so upstreams that build prefix filters from IRR accept you
   and reject others.
3. Filter what you accept: from customers only their registered prefixes (built from IRR
   data), from peers a prefix limit and route origin validation (ROV), never accept your own
   prefixes from outside.
4. Never leak: outbound to providers/peers only your and your customers' prefixes
   (an explicit outbound prefix-list, deny everything else).
5. Join MANRS actions as a checklist.

## Detect
- Use a BGP monitoring service (see the bgp.tools knowledge base). Alert on: new origin AS for
  your prefixes, more-specifics appearing, unexpected upstream in AS paths.
- Your own vantage: compare public looking glasses.

## Respond when hijacked
1. Confirm from several vantage points (RIPEstat, looking glasses).
2. Announce more-specifics (e.g. /24s if the hijacker took a /23) to win longest-prefix match, if
   your ROAs and filters allow it (another reason to keep ROAs tight but have a plan).
3. Contact the offending AS and its upstreams (PeeringDB contacts, NOC emails) and your transit
   providers; post to operator lists if needed.
4. Record timeline and impacted traffic for the post-incident review.

## Verify
- [ ] RPKI status valid for all your prefixes, IRR objects present, and an alert test (e.g.
  announcing a test more-specific in a lab AS) triggers notification.

## Checked
2026-10-28. Confirmed against the MANRS network operator guide (IRR route objects, RPKI/ROV, PeeringDB contacts, looking glasses) and RFC 7908 (route leak definition, leak types including transit-provider prefixes leaked to a peer or to another transit provider). Removed: bgpq4, RFC 9234 BGP Role, the named monitoring vendors, router command examples and the max-length equality claim.
Method: documentation only; no commands were run.
