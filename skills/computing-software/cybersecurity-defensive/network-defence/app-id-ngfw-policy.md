---
id: computing-software.cybersecurity-defensive.network-defence.app-id-ngfw-policy
name: app-id-ngfw-policy
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [firewall, app-id-policy, ngfw, palo-alto, application-default, policy-optimizer, user-id]
level: advanced
status: draft
description: "Move NGFW rules from port-based to application-aware policy: App-ID with application-default service, User-ID, Policy Optimizer migration and handling unknown and SSL-hidden traffic."
sources: ["Palo Alto Networks PAN-OS Administrator's Guide - App-ID and Policy Optimizer", "Palo Alto Networks - Best Practices for Security Policy", "Fortinet FortiGate Administration Guide - Application control"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Application-aware NGFW policy

**Goal:** rules allow named applications for named user groups on their standard ports, not "any app on TCP 443".

## Principles
- Rule = source zone/user group + destination + **application** + **service `application-default`** + security profiles + log at session end.
- `application-default` forces each app onto its standard ports, blocking tunnelling of other apps over allowed ports.
- Explicitly block high-risk categories (remote access tools not sanctioned, P2P, anonymisers/proxies like Tor) above allow rules.
- Unknown traffic (`unknown-tcp`, `unknown-udp`) on internal custom apps: create custom App-IDs or application overrides; deny unknown to the internet.

## Migration with Policy Optimizer (PAN-OS)
1. Policies > Policy Optimizer > "Rules without App Controls" (port-based rules).
2. For each, view apps seen over 30-90 days; "Create Cloned Rule" with those apps above the original, or add apps to the rule.
3. Watch hit counts; when the port-based rule stops getting hits, disable then delete it.
4. Also review "Unused Apps" in app-based rules and "Unused rules".

## Dependencies
Some apps require others (e.g. `ms-office365` depends on `ssl`/`web-browsing`); PAN-OS shows implicit/dependent apps on commit warnings. Allow dependencies explicitly where the commit warns.

## Visibility prerequisites
- Decryption (SSL Forward Proxy) for meaningful App-ID on TLS traffic beyond SNI-based identification; exclude regulated categories and pinned apps.
- User-ID mapping from AD/IdP (agentless WMI, syslog from IdP, GlobalProtect, Cloud Identity Engine) to write group-based rules.

## Other platforms
FortiGate application control profiles plus `set application-list` on policies or NGFW policy-based mode; Check Point Application Control & URL Filtering blade; cloud firewalls (Azure Firewall application rules, AWS Network Firewall Suricata-compatible rules) are mostly FQDN/protocol based.

## Verify
- [ ] No internet-bound allow rule uses `any` application with `any` service.
- [ ] Policy Optimizer shows port-based rules trending to zero.
- [ ] Test: SSH over TCP 443 to the internet is blocked by `application-default`.
