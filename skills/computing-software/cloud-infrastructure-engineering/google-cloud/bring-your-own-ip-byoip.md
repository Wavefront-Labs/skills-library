---
id: computing-software.cloud-infrastructure-engineering.google-cloud.bring-your-own-ip-byoip
name: bring-your-own-ip-byoip
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, vpc, bring-your-own-ip, byoip, public-delegated-prefix, roa]
level: advanced
status: docs-checked
description: "Bring your own public IPv4/IPv6 range to Google Cloud: ROA and reverse-DNS validation, public advertised and delegated prefixes, announcing, and using the addresses."
sources: ["https://docs.cloud.google.com/vpc/docs/bring-your-own-ip", "https://docs.cloud.google.com/vpc/docs/create-pdp", "https://docs.cloud.google.com/sdk/gcloud/reference/compute/public-advertised-prefixes/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bring your own IP (BYOIP)

Use when customers allowlist your existing public IPs, or you migrate services without changing addresses.
A v2 Premium Tier IPv4 public advertised prefix (PAP) is /16 to /24, so /24 is the smallest IPv4 PAP.

## 1. Prove ownership
1. Ownership of every IPv4 prefix and external-access IPv6 prefix is verified with a **ROA** and **reverse DNS validation**.
2. Do not announce the prefix (or any overlapping prefix) elsewhere: Google does not support overlapping BYOIP announcements, and
   overlap can cause unexpected routing and packet loss.
3. After validation the prefix is not advertised until provisioned: roughly two to four weeks. Plan the cutover for that window.

## 2. Create prefixes
```bash
gcloud compute public-advertised-prefixes create acme-pap --range=203.0.113.0/24 \
  --dns-verification-ip=203.0.113.1 --pdp-scope=REGIONAL
gcloud compute public-delegated-prefixes create acme-pdp-euw1 --region=europe-west1 \
  --public-advertised-prefix=acme-pap --range=203.0.113.0/26
# global PDP: use --global instead of --region (project must be allowlisted; file a support case)
gcloud compute public-delegated-prefixes describe acme-pdp-euw1 --region=europe-west1 --format='value(status)'
```
`--dns-verification-ip` must be inside `--range`. A PAP creates either global or regional PDPs, not both. A PDP can be
split into sub-prefixes (same scope as the parent). For IPv6 the top-level PDP uses `--mode=DELEGATION` and you must
divide it into sub-prefixes before using addresses.

## 3. Announce and use
For regional v2 prefixes the PAP is not announced automatically when provisioned: you decide when to announce or withdraw
(see "Manage BGP announcement (v2)" in the BYOIP docs for the exact commands). PDP status values include `READY_TO_ANNOUNCE`,
`ANNOUNCED`, `ANNOUNCED_TO_GOOGLE` and `ANNOUNCED_TO_INTERNET`. v1 prefixes announce automatically after provisioning.
Addresses created from a PDP can be used only in the project and scope they are allocated to; every address in the range is usable
(no reserved network or broadcast address). Follow the BYOIP "create IP addresses" guide for the address-reservation
command for your gcloud version.

## Gotchas
- Provisioning takes multiple weeks and cannot be accelerated; start early.
- A PDP can be sub-delegated up to three times from a PAP.

## Verify
- [ ] `describe` shows the PDP status you expect (for example `ANNOUNCED_TO_INTERNET`) and traffic to a resource using a BYOIP address works.

## Checked
2026-10-28. Confirmed against the VPC "Bring your own IP" page, "Create a public delegated prefix" page and the gcloud
`public-advertised-prefixes create` reference: ROA plus reverse DNS validation, two-to-four-week provisioning, /16-/24 PAP range,
global PDP allowlist, DELEGATION mode, PDP statuses, `--dns-verification-ip`, `--pdp-scope`, three sub-delegations.
Removed: AS number, `public-advertised-prefixes announce|withdraw` (no such command), `addresses create --public-delegated-prefix`
(not a gcloud flag), "global PDP serves global LBs only" and "delete requires addresses released" (not confirmed).
Method: documentation only; no commands were run.
