---
id: computing-software.cloud-infrastructure-engineering.aws.route53-routing-and-health-checks
name: route53-routing-and-health-checks
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, route53, route-53, dns, dns-routing, health-check, health-checks, failover-routing, weighted-routing, latency-routing, geolocation-routing, geoproximity-routing, multivalue-answer, alias-record, hosted-zone, private-hosted-zone, route53-resolver, resolver-endpoints, hybrid-dns, dnssec, query-logging, ttl, evaluate-target-health, application-recovery-controller, zonal-shift]
level: practitioner
status: docs-checked
description: "Design Route 53 DNS: alias records, routing policies, health checks that fail over, private zones and Resolver endpoints for hybrid DNS, DNSSEC and query logging."
sources: ["https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-determining-health-of-endpoints.html", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-choosing-alias-non-alias.html", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zone-private-considerations.html", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-configuring-dnssec-enable-signing.html", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/DNSLimitations.html", "https://docs.aws.amazon.com/r53recovery/latest/dg/arc-zonal-shift.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Route 53 routing and health checks — DNS that steers and fails over

**Goal:** clients reach the nearest healthy endpoint, a regional outage disappears from
DNS within a TTL, internal names resolve from on-prem and from every VPC, and nobody
can spoof your zone. Load balancers that sit behind these records are in
`...aws.elastic-load-balancing`; multi-region design is in
`...cloud-architecture.multi-region-high-availability-design`.

## 1. Records: alias over CNAME
- **Alias** records point at AWS resources (ALB/NLB, CloudFront, API Gateway, S3
  website, Global Accelerator, VPC endpoint, another record in the same zone). They
  carry no query charge for AWS-resource targets, work at the **zone apex** (`example.com`), resolve to the current
  IPs with no extra lookup, and can `EvaluateTargetHealth`. Use them whenever the
  target is an AWS resource; CNAME only for external names.
- TTL: you cannot set a TTL on an alias record to an AWS resource (Route 53 uses the resource's
  default). For your own records use 60 s on anything that participates in failover, 300–3600 s on static names.
  Lower TTL costs nothing with alias; with non-alias it raises the per-query bill.
- Change with a batch so it is atomic:
  `aws route53 change-resource-record-sets --hosted-zone-id Z… --change-batch file://rr.json`
  (`UPSERT` is idempotent; wait on `get-change` for `INSYNC`).

## 2. Routing policies — pick by question
| Question | Policy | Note |
|---|---|---|
| One target | **Simple** | multiple values returned in random order, no health check |
| Canary / blue-green by percentage | **Weighted** | weights 0–255, relative not percent; weight 0 stops traffic unless every nonzero record is unhealthy |
| Lowest latency per user | **Latency** | per-region records; measured from the resolver, not the user |
| Active-passive DR | **Failover** | PRIMARY/SECONDARY, health check on primary required |
| Compliance by country/continent/US state | **Geolocation** | add a default (`*`) record or unmatched locations get a "no answer" response |
| Bias traffic toward a region by distance | **Geoproximity** | bias −99..99: positive expands a resource's catchment, negative shrinks it; maps are in Traffic Flow |
| Cheap client-side load balancing | **Multivalue answer** | up to 8 healthy records per response, random selection, optional health check per record |
| Route by the client's resolver CIDR | **IP-based** | ISPs/branches with known ranges |
Combine them with **Traffic Flow** policies (a versioned tree: geolocation → failover →
weighted), charged per policy record per month; for one or two layers nested alias
records (`example.com` → `region.example.com`) can do the same without Traffic Flow.

## 3. Health checks that fail over
- Types: **endpoint** (HTTP/HTTPS/TCP to an IP or name, every 30 s — or 10 s "fast",
  from checkers in several Regions; healthy if more than 18% of checkers report healthy), **calculated**
  (threshold over child checks), **CloudWatch alarm** (for **private** resources — checkers sit
  outside your VPC and cannot reach a private IP; the alternative is a public IP).
- Endpoint checks: use HTTPS with a `/health` path that tests dependencies, enable
  **string matching** (first 5,120 bytes) so a 200 from a maintenance page still fails,
  set `FailureThreshold 3` (range 1–10), and allow the checker IP ranges (`ROUTE53_HEALTHCHECKS` in
  `ip-ranges.json`) in the SG. HTTPS checks do not validate the certificate.
- **Alias + EvaluateTargetHealth = true** makes Route 53 consult the ELB's own target
  health (an ALB with zero healthy targets is unhealthy) — no separate health check
  needed.
- Failover rule: a record with an unhealthy health check is removed from answers; if
  **every** record is unhealthy, Route 53 answers as if all were healthy (fail-open).
  Put a health check or `EvaluateTargetHealth` on every record in a failover-capable set; an
  unchecked record cannot be taken out of answers.
- The `Inverted` flag simulates failure without touching the endpoint:
  `update-health-check --inverted` flips the result; a disabled check (`--disabled`) is
  treated as healthy by a calculated parent. Use inverted for DR drills.

## 4. Private DNS and hybrid resolution
- A **private hosted zone** attaches to VPCs (`associate-vpc-with-hosted-zone`);
  cross-account association needs `create-vpc-association-authorization` in the zone
  owner's account first. The VPC must have `enableDnsHostnames` and `enableDnsSupport` enabled.
- Split-horizon: the same name in a public and a private zone; VPC clients see the
  private answer.
- **Route 53 Resolver** answers DNS queries from VPC resources.
  To reach it from on-prem create an **inbound endpoint** (IP addresses in your subnets, reachable
  over Direct Connect or VPN; point on-prem conditional forwarders at those IPs). To resolve on-prem names
  from VPCs, an **outbound endpoint** plus **Resolver rules** (`corp.example.com` →
  on-prem DNS IPs), shareable with RAM. Quotas (read 2026-10-27): 6 IP addresses per endpoint and per rule,
  4 endpoints per Region, up to 10,000 UDP queries per second per endpoint IP address (actual QPS varies).
- **Query logging** (`create-resolver-query-log-config` → CloudWatch Logs/S3/Firehose)
  shows every VPC query including answers — the fastest way to find who still calls a
  retired hostname. **DNS Firewall** rule groups block domain lists per VPC.

## 5. DNSSEC, delegation, protection
- Sign a public zone: KMS asymmetric customer managed key (`ECC_NIST_P256`, in US East N. Virginia) → KSK
  (`create-key-signing-key`) → `enable-hosted-zone-dnssec` → publish the DS record in the
  parent zone. Validate with `dig +dnssec`; a wrong DS breaks resolution for validating resolvers, so
  first lower the zone's maximum TTL (the guide recommends 3600 s) and the SOA TTL/minimum so you can roll back quickly.
- Delegate subdomains to other accounts by creating the child zone there and an NS
  record in the parent.
- Prefer **Application Recovery Controller zonal shift** over DNS tricks for an
  AZ-level problem: after you opt resources in (and prescale), a zonal shift moves traffic away
  from an AZ for a time you set, from one minute up to three days, and you can cancel it. It is a temporary mitigation.

## Gotchas
- Latency routing uses the **resolver's** location; users on a global public resolver
  without EDNS Client Subnet land in whatever region is close to that resolver.
- Health checks are global resources but their CloudWatch metrics live in **us-east-1**.

## Verify
- [ ] Apex and sub-records are alias where the target is AWS; `dig example.com` returns A records with TTL ≤ 60 where failover applies.
- [ ] Every failover/latency/geo record has a health check or `EvaluateTargetHealth`; the health-check status page shows all regions green.
- [ ] Inverting the primary's health check moves `dig` answers to the secondary within TTL + 30 s.
- [ ] On-prem resolves a private-zone name via the inbound endpoint; a VPC instance resolves a corp name via the outbound rule.
- [ ] `dig +dnssec +multi example.com SOA` shows `ad` flag from a validating resolver after DS publication.

## Checked

Checked 2026-10-27 against the Route 53 Developer Guide (routing policies, alias vs non-alias, health checks, failover algorithm, private hosted zones, Resolver, DNSSEC, quotas), the ARC zonal shift guide and the aws-cli route53 reference.
- Corrected: geolocation with no default returns a "no answer" response (not NXDOMAIN); geoproximity is a normal routing policy with bias -99..99 (only the maps are Traffic Flow); alias records to AWS resources have a resource-defined TTL; CloudWatch-alarm checks cannot use metric math or high-resolution metrics (see route53-health-check-types).
- Corrected: Resolver endpoint quotas (6 IPs per endpoint and per rule, 10,000 QPS per endpoint IP address); zonal shift needs opt-in and prescaling and lasts up to 72 hours.
- Confirmed: weights 0-255, multivalue up to eight healthy records, fail-open when all records are unhealthy, KMS key must be asymmetric ECC_NIST_P256 in US East (N. Virginia), cross-account PHZ association authorization, `enableDnsHostnames`/`enableDnsSupport`.
- Removed: hosted-zone and ENI price claims, "~15 checkers", ".2 address", `aws.internal`, readiness-check wording and several unconfirmed gotchas.

Method: documentation only; no commands were run.
