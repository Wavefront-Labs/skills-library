---
id: computing-software.cybersecurity-defensive.network-defence.ddos-scrubbing-and-cdn-protection
name: ddos-scrubbing-and-cdn-protection
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [ddos-mitigation, ddos-scrubbing, cdn, anycast, aws-shield-advanced, cloudflare, origin-cloaking, volumetric-ddos, bgp-diversion]
level: practitioner
status: draft
description: "Protect internet services from volumetric DDoS with CDN/anycast and scrubbing services: always-on vs on-demand, origin cloaking, and provider onboarding."
sources: ["CISA/FBI/MS-ISAC Understanding and Responding to DDoS Attacks (2024)", "AWS Shield Advanced documentation", "CompTIA Security+ SY0-701 objectives 2.4 and 3.4"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DDoS scrubbing and CDN protection

**Goal:** survive volumetric and protocol attacks far larger than your own bandwidth by
absorbing them in a provider network before they reach you.

## Options
| Option | How | Fits |
|---|---|---|
| CDN / reverse proxy with DDoS protection (Cloudflare, Akamai, Fastly, Azure Front Door, CloudFront + Shield) | Anycast absorbs traffic; L3/4 filtered, L7 rules | Web and API |
| Cloud provider protection (AWS Shield Standard/Advanced, Azure DDoS Network Protection, Google Cloud Armor) | Protects cloud IPs, response team and cost protection in paid tiers | Cloud-hosted services |
| Scrubbing centre via BGP diversion (Akamai Prolexic, Radware, Lumen) | Announce your prefix through the provider during attack (on-demand) or always | On-prem data centres, non-HTTP services |
| ISP clean pipe | Upstream filtering | Simple volumetric protection |

## Always-on vs on-demand
Always-on: no switch-over delay, small latency cost. On-demand (BGP diversion when an attack
is detected): cheaper but minutes of impact during swing; requires a /24 or larger prefix you
control and tested runbooks.

## Origin cloaking
If attackers can reach origin IPs directly, the CDN is bypassed:
- Firewall origins to accept only provider IP ranges (or use authenticated origin pulls / mTLS, private connectivity like Cloudflare Tunnel or AWS VPC origins).
- Change origin IPs after onboarding; check DNS history and certificates (CT logs, Censys) that might reveal them.
- Do not send mail or expose other services from the origin IPs.

## Onboarding checklist
Inventory internet-facing services and their criticality; contacts and escalation numbers at
the provider; pre-approved emergency changes; alerting for traffic anomalies; annual test (some
providers run controlled DDoS tests, which need permission from your cloud provider too).

## Gotchas
- DNS is a common target: use an anycast DNS provider with DDoS protection, ideally two.
- Protecting the website but not the VPN, mail and API endpoints leaves the business down anyway.
- Auto-scaling under attack costs money; cost protection exists only in some paid tiers.

## Verify
- [ ] Direct connections to origin IPs from the internet fail.
- [ ] Runbook rehearsed; provider contact tested within the last year.
