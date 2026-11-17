---
id: computing-software.cybersecurity-defensive.security-architecture.pci-dss-segmentation
name: pci-dss-segmentation
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [network-segmentation, pci-segmentation, pci-dss, cde, scope-reduction, segmentation-testing, connected-to-systems]
level: advanced
status: draft
description: "Reduce PCI DSS scope with segmentation: define the CDE and connected systems, isolate with controls, tokenisation and P2PE options, and segmentation penetration testing."
sources: ["https://www.pcisecuritystandards.org/document_library/", "https://docs-prv.pcisecuritystandards.org/Guidance%20Document/PCI%20DSS%20General/Guidance-PCI-DSS-Scoping-and-Segmentation.pdf", "https://www.pcisecuritystandards.org/standards/pci-dss/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PCI DSS scope reduction by segmentation

**Goal:** shrink the set of systems subject to PCI DSS by isolating the cardholder data
environment (CDE) so that out-of-scope systems genuinely cannot affect its security.

## Scope categories (PCI SSC scoping guidance)
- **CDE systems:** store, process or transmit cardholder data (CHD) or sensitive
  authentication data, or are on the same unsegmented network.
- **Connected-to / security-impacting:** can connect to or affect CDE security (AD, jump
  hosts, patch servers, logging, DNS, admin workstations). In scope too.
- **Out of scope:** no connectivity to the CDE and cannot affect it. Segmentation must
  prove this.

## Reduce what is in the CDE first
- Tokenisation (replace PAN with tokens in downstream systems), hosted payment pages or iframes
  from the payment provider, validated P2PE solutions for card-present. Each removes systems
  from CHD flows entirely.
- Data discovery to find stray PANs in file shares, logs and databases; delete or move.

## Segment
- Dedicated network zones/VLANs/VPCs for the CDE, with firewalls enforcing deny-by-default
  and documented business justification for every allowed flow (Requirement 1).
- Separate identity where practical (CDE admin accounts, MFA for all CDE access, Req 8).
- Admin access only via hardened jump hosts in a connected-to zone.
- Shared services (AD, SIEM, NTP) become connected-to systems; harden and include them.
- Cloud: separate accounts/subscriptions for CDE workloads, security groups and network
  policies, no peering to general environments without filtering.

## Validate
- Network diagrams and CHD flow diagrams kept current (Req 1.2.3/1.2.4).
- **Segmentation penetration testing** (Req 11.4.5): at least annually and after changes to
  segmentation (every six months for service providers), testing from out-of-scope networks
  that no path reaches the CDE.
- Firewall rule review every six months (Req 1.2.7).

## Gotchas
- A single flat management network touching CDE and corporate puts everything back in scope.
- Over-permissive rules "temporarily" added for projects; review catches them.
- Segmentation via VLAN ACLs only, without enforcement on the trunk/router, fails testing.

## Verify
Segmentation test report shows no reachable CDE ports from each out-of-scope segment, and
the QSA accepts the scope boundaries in the ROC/SAQ.
