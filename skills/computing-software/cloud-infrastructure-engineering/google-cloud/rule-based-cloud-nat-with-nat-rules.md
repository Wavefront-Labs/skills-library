---
id: computing-software.cloud-infrastructure-engineering.google-cloud.rule-based-cloud-nat-with-nat-rules
name: rule-based-cloud-nat-with-nat-rules
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-nat, nat-rules, rule-based-nat, destination-based-nat, partner-allowlist, static-egress-ip]
level: practitioner
status: docs-checked
description: "Use Cloud NAT rules to pick different NAT IPs by destination, e.g. a dedicated egress IP for a partner allowlist, with CEL match expressions, rule numbers and drain IPs."
sources: ["https://cloud.google.com/nat/docs/nat-rules-overview", "https://cloud.google.com/nat/docs/using-nat-rules", "https://cloud.google.com/sdk/gcloud/reference/compute/routers/nats/rules/create", "https://cloud.google.com/sdk/gcloud/reference/compute/routers/nats/rules/update", "https://cloud.google.com/sdk/gcloud/reference/compute/routers/nats/rules/list"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rule-based Cloud NAT with NAT rules

By default a Cloud NAT gateway uses its IP pool for all destinations. **NAT rules** select specific
NAT IPs for traffic to specific destination ranges; everything else uses the default pool.

## Example: partner requires a fixed source IP
```bash
gcloud compute addresses create nat-partner-ip --region=europe-west2
gcloud compute addresses create nat-default-1 nat-default-2 --region=europe-west2
gcloud compute routers nats create egress-nat --router=cr-ew2 --region=europe-west2 \
  --nat-all-subnet-ip-ranges --nat-external-ip-pool=nat-default-1,nat-default-2
gcloud compute routers nats rules create 100 --router=cr-ew2 --region=europe-west2 --nat=egress-nat \
  --match='inIpRange(destination.ip, "198.51.100.0/24") || inIpRange(destination.ip, "203.0.113.10/32")' \
  --source-nat-active-ips=nat-partner-ip
gcloud compute routers nats rules list --router=cr-ew2 --region=europe-west2 --nat=egress-nat
```
- Rule numbers 0-65000, lower = higher priority; no two rules share a number; the first match wins; a default rule (65001) covers everything else.
- Public NAT matches use CEL on `source.ip` or `destination.ip` (not both in one rule) with `inIpRange()`, `==` and `||`.
- Rules require manual NAT IP allocation (`MANUAL_ONLY`) on the gateway; you cannot use 0.0.0.0/0 in a rule.
- Match ranges must not overlap across rules, and NAT IPs must not overlap across rules.

## Changing IPs safely
Move an IP to `--source-nat-drain-ips` before removal so existing connections finish:
```bash
gcloud compute routers nats rules update 100 --router=cr-ew2 --region=europe-west2 --nat=egress-nat \
  --source-nat-active-ips=nat-partner-ip-2 --source-nat-drain-ips=nat-partner-ip
```

## Private NAT
NAT rules also apply to Private NAT (NCC spokes / hybrid), with matches on `nexthop.hub` or `nexthop.is_hybrid` (optionally combined with `source.ip` using `&&`). Only source-based rules are supported there, and traffic that matches no rule is dropped.

## Gotchas
- A rule must have a non-empty active or drain IP set; with an empty active set, new matching connections are dropped.
- There is also a `nat/rule/nat_allocation_failed` gateway metric for per-rule allocation failures.

## Verify
- [ ] A test connection to the partner range arrives from the partner IP; other destinations use default pool IPs.

## Checked

- Date: 2026-10-27; documentation release: Google Cloud documentation pages as published on that date.
- Found incomplete: the match grammar was described as destination-only; the NAT rules overview supports source.ip or destination.ip (not both) for Public NAT and nexthop.hub, nexthop.is_hybrid and && for Private NAT.
- Confirmed (NAT rules overview): priority range 0-65000, default rule 65001, unique numbers, first match, MANUAL_ONLY requirement, no overlap of ranges or NAT IPs across rules, active/drain IP requirement, Private NAT source-based only.
- Confirmed (gcloud reference): `routers nats rules create/update/list` flags --match, --source-nat-active-ips, --source-nat-drain-ips; example inIpRange(destination.ip, ...) form; `nats create --nat-external-ip-pool`.
- Confirmed (monitoring page): nat/rule/nat_allocation_failed metric.
- Removed: the claim that rule IPs cannot be in the default pool and the nat_ip log field claim (not found in the pages read).

Method: documentation only; no commands were run.
