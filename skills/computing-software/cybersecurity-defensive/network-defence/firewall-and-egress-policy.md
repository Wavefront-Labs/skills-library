---
id: computing-software.cybersecurity-defensive.network-defence.firewall-and-egress-policy
name: firewall-and-egress-policy
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [network-defence, firewall, egress-filtering, outbound-filtering, default-deny, ngfw, firewall-rule-review, explicit-proxy, dns-filtering, protective-dns, rpz, security-groups, nacl, aws-network-firewall, azure-firewall, nftables, iptables, palo-alto, fortigate, c2, data-exfiltration, change-management]
level: practitioner
status: draft
description: "Design and maintain firewall rulesets with default-deny egress: server allowlists, proxied user traffic, protective DNS, rule hygiene and logging that catches C2."
sources: ["NIST SP 800-41 Rev. 1 - Guidelines on Firewalls and Firewall Policy", "CIS Critical Security Controls v8 - Controls 4, 9, 12, 13", "NCSC - Protective DNS guidance", "CISA - Egress filtering / network segmentation recommendations in advisories"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Firewall and egress policy — block outbound by default, prove what's allowed

**Goal:** most rulesets filter inbound and allow any outbound. Malware C2, data
exfiltration and stolen-credential use all need outbound. Make servers default-deny
outbound, push users through inspected paths, and keep the ruleset reviewable.

## 1. Rule design principles
- Every rule: source, destination, service (port/protocol or App-ID), action, **log**,
  **owner**, **ticket/justification**, **review date**. Put these in the rule
  description or tags.
- No `any` in more than one of source/destination/service; never `any any any allow`.
- Explicit cleanup rule at the bottom: `deny any any log` — don't rely on an implicit
  deny that doesn't log.
- Order specific before general; put high-hit allow rules near the top for performance.
- Use objects/groups (address groups, FQDN objects, dynamic tags from cloud/EDR) rather than raw IPs.

## 2. Egress for servers: allowlist
1. Collect 2–4 weeks of outbound flow logs per server group.
2. Typical legitimate needs: OS/package updates (prefer an internal mirror or proxy),
   NTP, DNS **to your resolvers only**, EDR/monitoring cloud, specific SaaS/API FQDNs.
3. Write allow rules per group by FQDN (NGFW FQDN objects, AWS Network Firewall
   domain lists, Azure Firewall application rules, Squid ACLs).
4. Deny everything else from server subnets, with logging. Start with log-only
   "would deny" for a week if your platform supports it.
Servers browsing the internet directly is a red flag in itself.

## 3. Egress for users
- Route web through an explicit or cloud proxy / SSE with category blocking
  (newly registered domains, uncategorised, dynamic DNS, known-malicious), TLS
  inspection where legal and practical (exempt banking/health categories and pinned apps).
- Block direct outbound from user subnets except via proxy, DNS to internal resolvers,
  and required real-time apps (e.g. Teams/Zoom media UDP ranges per vendor docs).
- Block outbound SMB (TCP 445), NetBIOS, RDP (3389) and SMTP (25) from clients to the internet.

## 4. DNS as a control
- Only internal resolvers may query external DNS (block TCP/UDP 53 and DoT 853 to
  the internet from everything else). Forward to a protective DNS service (e.g.
  national PDNS schemes, Quad9, commercial) or use RPZ feeds.
- Handle DNS-over-HTTPS: disable it via browser policy (e.g. Chrome
  `DnsOverHttpsMode=off`, Firefox canary domain / enterprise policy) and block known DoH endpoints.
- Log all queries; DNS logs are your best C2 and exfil dataset.

## 5. Cloud
- Security groups: no `0.0.0.0/0` inbound except load balancers on 443; outbound
  default in AWS SGs is allow-all — replace it for sensitive tiers.
- Use centralised egress (NAT + network firewall / Azure Firewall / Cloud NGFW) per
  VPC/VNet hub so policy and logging are in one place.
- Prefer private endpoints (PrivateLink, Private Endpoint, Private Service Connect) for cloud services over internet egress.

## 6. Rule hygiene
Quarterly: export hit counts; remove rules with zero hits over 90 days (after owner
check — DR/annual jobs exist), expired temporary rules, and shadowed/redundant rules
(tools: vendor policy optimisers, AlgoSec/Tufin/FireMon-type analysers). Changes go
through change management with a peer review of the diff.

## Gotchas
- FQDN rules resolve at the firewall; CDN-hosted services rotate IPs and can break or
  over-allow (a CDN IP allowed for one domain serves thousands). Prefer proxy/SNI-based control.
- TLS 1.3 and ECH reduce what SNI inspection sees; plan for proxies and endpoint controls.
- IPv6 often has a parallel, unfiltered path — apply the same policy or disable it deliberately.
- Logging only denies leaves you blind to successful C2; log allowed sessions too
  (at least session start/end summaries).
- "Temporary" any-allow rules from incidents outlive the incident; give them a hard expiry.

## Verify
- [ ] Every rule has owner, justification and review date; no any/any/any allows.
- [ ] A test server cannot reach an arbitrary internet host (e.g. `curl -m 5 https://example.com` fails and is logged).
- [ ] Clients cannot reach external DNS directly (`nslookup example.com 8.8.8.8` fails).
- [ ] Outbound SMB/RDP/SMTP from clients to the internet is blocked.
- [ ] Allowed and denied sessions are logged to the SIEM.
- [ ] Zero-hit and expired rules were reviewed this quarter.

Related: computing-software.cybersecurity-defensive.security-architecture.zero-trust-segmentation
