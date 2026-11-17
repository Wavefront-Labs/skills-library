---
id: computing-software.cybersecurity-defensive.security-architecture.secure-network-design-review
name: secure-network-design-review
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [network-design-review, security-architecture-review, dmz, east-west-traffic, vpc-design, vlan-segmentation, threat-model-input, design-gate, architecture-decision-record, m-and-a-network-integration]
level: sme
status: draft
description: "Run a security architecture review on a new network/cloud design before it's built: the questions that find flaws a later pen test would find anyway, cheaper, before deployment."
sources: ["NIST SP 800-53 - SC (System and Communications Protection) control family", "AWS/Azure/GCP network reference architecture documentation (public)", "SANS whitepapers on secure network design review (public)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Secure network design review — catch the architectural flaw before it's poured in concrete

**Goal:** review a network or cloud network design (new VPC, new segment, new
site-to-site connection, an M&A network integration) before it's built, and find
the structural flaws that are cheap to fix on a diagram and expensive to fix
after production traffic depends on them.

## 1. Ask what this design assumes about adjacent trust
The most common flaw: a new segment/VPC is designed assuming its neighbours are
trustworthy because they're "internal," without checking what's actually
reachable. Walk every connection the design introduces (peering, VPN, transit
gateway, shared services VPC) and ask explicitly what that connection grants —
not what it's *intended* to grant, what the actual routing/firewall rules permit.
A permissive default (allow all within the VPC, allow all from the corporate
range) silently defeats the segmentation the design diagram implies.

## 2. East-west traffic gets less scrutiny than it deserves
Most review effort historically goes to the perimeter (what can reach this from
the internet) and far less to east-west (what can this segment reach, and what
can reach it, within the internal/cloud network). Since lateral movement after
an initial foothold is one of the most common real attack patterns, review
east-west rules with the same rigor as perimeter rules: does every internal
service actually need to talk directly to every other service it currently can,
or would a narrower allow-list (or a service mesh with mutual TLS and explicit
authorization) contain a compromise better? This connects directly to
zero-trust-segmentation's microsegmentation guidance — apply it at design time,
not as a later retrofit.

## 3. DMZ and shared-services design
For anything with an internet-facing or partner-facing component, confirm there's
a genuine DMZ pattern: the exposed component cannot reach the internal network
directly, only through a controlled, narrow path (an API gateway, a message
queue, a database proxy with least-privilege credentials) — not a flat network
where the public-facing web server has direct, broad database access just
because that's the simplest thing to configure. Shared-services segments (DNS,
NTP, logging, identity) deserve particular scrutiny because a compromise there
tends to cascade everywhere that depends on them.

## 4. Specific traps in cloud network design
- **Default security groups/NSGs** often allow broader intra-VPC traffic than
  intended — review the *effective* rule set, not the stated intent.
- **Shared VPC/transit gateway architectures** can accidentally grant broader
  reachability than a single account's own security groups suggest — review the
  routing table, not just the security group, since routing determines whether
  traffic can even arrive to be evaluated by a security group.
- **Public IP assignment by default** on new resources (common in some cloud
  defaults) silently exposes things the designer assumed were private — check
  the actual default for the specific service/region, don't assume.

## 5. M&A and third-party network integration
A newly acquired company's network, or a partner's network connected via VPN/
direct connect, should be reviewed as a **new, unverified trust zone** until its
own security posture is assessed — connecting it with full internal trust before
that assessment is a very common real-world breach vector (the attacker
compromises the weaker-security acquired/partner network first, then pivots in).
Default to a restrictive, narrow-purpose connection (specific application ports,
not full network reachability) until the other side's posture is verified.

## Gotchas
- A design reviewed against its documentation/diagram, not against the actual
  deployed configuration (Terraform state, live security group rules), misses
  drift that happened during implementation — review the as-built, not just the
  as-designed, before sign-off.
- "Temporary" broad access granted during a migration or cutover window that's
  never tightened afterward is one of the most common ways a reviewed, approved
  design ends up with unreviewed broad access in production.
- Logging/visibility requirements are often an afterthought in network design —
  confirm flow logs/VPC flow logs or equivalent are enabled on new segments
  *before* they carry production traffic, not added after an incident shows the gap.
- Reviewing only new resources and skipping the existing segments they connect to
  misses inherited risk from whatever the new design is now trusting.

## Verify
- [ ] Every new connection/peering's actual permitted traffic was checked against
      effective rules/routing, not stated intent.
- [ ] East-west traffic received the same scrutiny as perimeter/ingress traffic.
- [ ] Internet/partner-facing components route through a genuine DMZ pattern,
      not direct internal access.
- [ ] New/acquired/partner networks are treated as unverified trust zones until
      their posture is assessed.
- [ ] The as-built configuration (not just the design diagram) was reviewed
      before sign-off, and flow logging is enabled before production traffic flows.

Related: computing-software.cybersecurity-defensive.security-architecture.zero-trust-segmentation,
computing-software.cybersecurity-defensive.network-defence.firewall-and-egress-policy,
computing-software.cybersecurity-defensive.cloud-security.cspm-and-least-privilege-remediation
