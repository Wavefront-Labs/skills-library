---
id: computing-software.cybersecurity-defensive.security-architecture.defense-in-depth-reference-architecture
name: defense-in-depth-reference-architecture
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [defense-in-depth, layered-security, security-architecture, control-redundancy, single-point-of-failure, reference-architecture, compensating-controls, security-design-review, failure-mode-analysis]
level: sme
status: draft
description: "Design layered defenses so no single control's failure is catastrophic: pick genuinely independent layers, avoid redundant-in-name-only controls, and size the architecture to actual asset value."
sources: ["NIST SP 800-53 - control families and layered control guidance", "NSA/CISA - Network Infrastructure Security Guidance (public)", "SANS whitepapers on defense in depth (public course material)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Defense-in-depth reference architecture — layers that are actually independent

**Goal:** design a set of controls where one control's failure doesn't cascade
into total compromise — the discipline is picking layers that fail for
*different reasons*, not stacking more products that all share the same blind
spot.

## 1. Independence is the whole point
Two firewalls from different vendors in series look like defense in depth but
if both are bypassed by the same technique (an application-layer attack neither
inspects, a misconfiguration copied from the same runbook to both), they're not
actually independent — they share a common failure mode. Real independence
comes from controls operating at different layers (network, host, identity,
application, data) and ideally different trust assumptions (a control that
doesn't rely on the network perimeter being intact still works if the perimeter
is breached). Ask of every proposed layer: "if the layer in front of this one is
completely bypassed, does this one still do anything?" If the answer is no, it's
not an independent layer, it's a second instance of the same control.

## 2. Map layers to what they're actually defending against
A practical layered model for a typical enterprise, outside-in:
- **Perimeter/network** (firewall, IPS at the boundary) — stops unsolicited
  inbound and known-bad outbound, but assume it will be bypassed (phishing,
  VPN, supply chain) — never the only control on anything sensitive.
- **Identity** (MFA, conditional access, least privilege) — stops credential-
  based access even after network perimeter is crossed; this is now commonly the
  *de facto* perimeter, not the network.
- **Endpoint** (EDR, hardening, application allowlisting) — stops or detects
  execution on the host even after identity is compromised (phished session, stolen token).
- **Application** (secure coding, WAF, input validation) — stops exploitation of
  the application layer regardless of network/identity/endpoint state.
- **Data** (encryption at rest/in transit, DLP, access controls scoped to the
  data itself) — the last layer; if everything else fails, this is what limits
  the actual damage (encrypted data exfiltrated is far less useful to an attacker
  than plaintext).
- **Detection/response** (logging, SIEM, IR capability) — not a preventive layer,
  but the layer that bounds *how long* any bypass goes unnoticed, which is often
  the biggest lever on actual business impact regardless of which preventive
  layer failed.
A good design review walks this list for a given asset and asks which layers
genuinely apply, rather than assuming the generic list is complete for every asset.

## 3. Size the architecture to actual asset value
Not every system needs every layer at maximum strength — over-applying controls
to a low-value asset wastes budget and operational overhead that a genuinely
high-value asset needed. Classify assets by business impact first (data
sensitivity, availability requirement, blast radius if compromised), then
allocate layer depth accordingly — this is the architectural analogue of
risk-based prioritisation in vulnerability management.

## 4. Watch for the single point that undoes every layer
The classic failure: a shared admin credential, a single identity provider, or a
single network path that, if compromised, defeats every layer at once because
every layer trusted it. Identity infrastructure (AD, the IdP) is the most common
real-world single point of failure in an otherwise well-layered architecture —
treat it as its own Tier 0 problem (see privileged-access-management) rather
than just one more "identity layer" box on the diagram.

## 5. Review under failure, not just under normal operation
Table-top the architecture against "layer X has just failed completely" for
each layer in turn, and check whether the remaining layers actually contain the
scenario or whether the design silently assumed that layer would always hold.
This surfaces the controls that were load-bearing far beyond what anyone
intended.

## Gotchas
- Compliance checklists often reward having a control present, not whether it's
  independent of the others — a compliant architecture can still have hidden
  single points of failure.
- Vendor consolidation (buying the "everything" platform from one vendor) can
  quietly collapse what looked like independent layers into one vendor's shared
  codebase/outage domain.
- Logging/detection is frequently under-resourced relative to preventive
  controls, even though it's the layer that bounds damage after every other
  layer fails — budget for it as a first-class layer, not an afterthought.
- A layered design reviewed once at initial build and never re-walked after
  architecture changes accumulates silent single points of failure over time.

## Verify
- [ ] Each proposed layer passes the "still does something if the layer in front
      fails completely" test.
- [ ] Layer depth is allocated by asset business-impact classification, not
      applied uniformly.
- [ ] Identity infrastructure is treated as its own Tier 0 concern, not folded
      anonymously into "the identity layer."
- [ ] A failure-mode table-top (each layer assumed fully bypassed in turn) has
      been run against the current architecture.
- [ ] Detection/response capability is resourced as a first-class layer, not residual budget.

Related: computing-software.cybersecurity-defensive.security-architecture.zero-trust-segmentation,
computing-software.cybersecurity-defensive.identity-access-management.privileged-access-management,
computing-software.cybersecurity-defensive.threat-modelling.attack-trees-and-pasta
