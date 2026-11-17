---
id: computing-software.cybersecurity-defensive.network-defence.geo-blocking
name: geo-blocking
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [geo-blocking, geoip, country-blocking, conditional-access-locations, waf-geo-match, firewall-policy, attack-surface-reduction]
level: practitioner
status: docs-checked
description: "Apply geo-blocking where it helps: AWS WAF geo match, Entra named locations in Conditional Access, firewall country rules, exceptions, and limits against VPNs and proxies."
sources: ["https://docs.aws.amazon.com/waf/latest/developerguide/waf-rule-statement-type-geo-match.html", "https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-assignment-network"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Geo-blocking

Reduces noise and opportunistic attacks from countries you never do business with. It does not stop a
determined attacker using a VPN, cloud host or residential proxy in an allowed country.

## Where to apply
| Layer | Mechanism |
|---|---|
| Edge firewall (inbound to VPN, RDP gateway, mail) | Country or region objects in deny rules (check your vendor's documentation for the object type) |
| WAF (web apps) | AWS WAF geo match statement |
| IdP | Entra named locations (countries) in Conditional Access: block, or require stronger auth |
| Outbound | Optional: block egress to high-risk countries for servers (not users) |

## AWS WAF geo match
- Matches the request's country of origin by ISO 3166-1 alpha-2 code (for example `HK`). Region matching
  cannot be done by a geo match rule alone: follow it with a label match rule on the region label.
- Location comes from the request's IP address using MaxMind GeoIP databases. By default it uses the origin
  IP; enable forwarded IP configuration to use a header such as X-Forwarded-For.
- The statement adds country and region labels (for example `awswaf:clientip:geo:country:US`,
  `awswaf:clientip:geo:region:US-OR`) to every request it inspects, whether or not it matches. Labels are
  added at the end of a rule's evaluation, so a label match must be in a separate, later rule. When a code is
  unavailable the label uses `XX`.

## Entra Conditional Access
- Named locations (Entra admin center > Entra ID > Conditional Access > Named locations) can hold IPv4/IPv6
  ranges or countries/regions; country locations can resolve by IP address or by GPS coordinates from the
  Microsoft Authenticator app, and can optionally include unknown countries/regions.
- A policy can include or exclude locations; Microsoft names "blocking access from specific countries your
  organization never operates from" and requiring MFA off the corporate network as common uses.
- Conditional Access is enforced after first-factor authentication and is not meant as a front line against DoS.
- IP-range named locations: no more than 195 named locations, 2000 ranges per location, CIDR masks greater
  than /8 only.

## Rules of thumb
- Deny inbound access to remote-access services (VPN portals, OWA, Citrix) from countries outside the business footprint.
- Prefer "require MFA/compliant device" over hard block at the IdP for travellers; keep a travel exception group with time-limited membership.

## Gotchas
- GeoIP databases are not perfectly accurate (AWS says MaxMind accuracy varies by country and IP type, and
  offers a correction process); review blocks reported by users.
- SaaS and cloud provider egress (email delivery, webhooks, monitoring probes) may come from blocked countries; allow by service rather than geography.
- Do not block countries on MX if partners send mail from there.

## Verify
- [ ] Test from a VPN exit in a blocked country is denied and logged.
- [ ] Exception process documented and expiring.

## Checked
Checked 2026-11-09 against the AWS WAF "Geographic match rule statement" page and the Microsoft Entra
Conditional Access "Network assignment" page, both read in full or by section. Removed as unconfirmed: the
PAN-OS source (page 404), FortiGate, Cloudflare, Azure Front Door and Okta mentions, the "unknown/anonymous
proxy" category advice, and the IPv6 accuracy remark.
Method: docs-checked 2026-11-09 against the AWS WAF and Microsoft Entra pages named above.
