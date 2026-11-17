---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-dns-zones-policies-and-dnssec
name: cloud-dns-zones-policies-and-dnssec
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-dns, dns, public-zones, private-dns-zones, dnssec, dns-forwarding, forwarding-zones, dns-peering, inbound-forwarding, server-policies, response-policies, response-policy-zones, routing-policies, geo-routing, failover-routing, split-horizon, metadata-dns, 169-254-169-254, dns-logging]
level: practitioner
status: docs-checked
description: "Run Cloud DNS: DNSSEC public zones, private zones per VPC, forwarding and peering zones, inbound server policies, response policies, geo/failover routing and query logging."
sources: ["https://cloud.google.com/dns/docs/zones/zones-overview", "https://cloud.google.com/dns/docs/vpc-name-res-order", "https://cloud.google.com/dns/docs/dnssec", "https://cloud.google.com/dns/docs/zones/forwarding-zones", "https://cloud.google.com/dns/docs/policies", "https://cloud.google.com/dns/docs/zones/manage-response-policies", "https://cloud.google.com/dns/docs/routing-policies-overview", "https://cloud.google.com/dns/quotas", "https://cloud.google.com/sdk/gcloud/reference/dns/managed-zones/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud DNS zones, policies and DNSSEC

**Goal:** public names signed, private names resolvable from every VPC and from on-prem,
on-prem names resolvable from GCP, and a response policy that can sinkhole a domain org-wide in one change.

## 1. Zones
```bash
# public, signed
gcloud dns managed-zones create example-com --dns-name=example.com. --description=prod --dnssec-state=on
gcloud dns managed-zones describe example-com --format='value(dnssecConfig.state)'
gcloud dns dns-keys list --zone=example-com   # take the KSK DS record to the registrar
# private, visible to listed VPCs
gcloud dns managed-zones create corp-internal --dns-name=internal.example. --visibility=private \
  --networks=prod-vpc,dev-vpc --description="private names"
```
- Private zones resolve only from VMs in the attached VPCs via the metadata resolver `169.254.169.254` (Compute Engine internal DNS zones are matched after private, forwarding and peering zones).
- Records: `gcloud dns record-sets create api.internal.example. --zone=corp-internal --type=A --ttl=300 --rrdatas=10.0.1.5`; transactions (`record-sets transaction start/add/execute`) for atomic multi-record changes; Terraform `google_dns_record_set` for everything in prod.
- DNSSEC: `on` signs the zone; **the chain is incomplete until the DS record is at the registrar** (`dig +dnssec DS example.com` to verify). Algorithm/key rotation is managed; turning DNSSEC off before removing DS breaks resolution.

## 2. Hybrid resolution
| Direction | Mechanism |
|---|---|
| GCP → on-prem names (`corp.local`) | **Forwarding zone**: `--visibility=private --forwarding-targets=10.10.0.53,10.10.0.54` (`--private-forwarding-targets` to force VPC routing over VPN/Interconnect). Queries egress from `35.199.192.0/19` — allow that range in the on-prem firewall and DNS ACLs. |
| On-prem → GCP private names | **Inbound server policy**: `gcloud dns policies create inbound --description="inbound" --networks=prod-vpc --enable-inbound-forwarding`; creates an inbound forwarder IP per subnet region (`gcloud compute addresses list --filter='purpose=DNS_RESOLVER'`); point on-prem conditional forwarders at those IPs. |
| VPC A → VPC B's private zones | **Peering zone**: `--target-network=vpc-b --target-project=…` (transitive DNS peering works through a single hop: at most three VPC networks, the middle one being the hop). Hub-and-spoke: peering zones in spokes targeting the hub VPC that holds forwarding zones. |
| Shared VPC | attach zones to the **host** network; service-project VMs resolve through it. |
Outbound **server policy** (`--alternative-name-servers`) overrides *all* resolution for a VPC — rarely wanted; prefer forwarding zones for specific domains.

## 3. Response policies (RPZ)
```bash
gcloud dns response-policies create sec-rpz --description="org sinkhole" --networks=prod-vpc,dev-vpc
gcloud dns response-policies rules create block-evil --response-policy=sec-rpz --dns-name=evil.example. \
  --local-data=name=evil.example.,type=A,ttl=60,rrdatas=0.0.0.0
gcloud dns response-policies rules create allow-partner --response-policy=sec-rpz --dns-name=ok.example. --behavior=bypassResponsePolicy
```
Rules are `--local-data` (override the answer: sinkhole to `0.0.0.0`, or point `*.googleapis.com` at the `private.googleapis.com` ranges for Private Google Access) or `--behavior=bypassResponsePolicy` (exempt a name from a wildcard rule). In the VPC name resolution order, an outbound server policy's alternative name servers are used first, then network-scoped response policy rules, then private, forwarding and peering zones, then Compute Engine internal zones. Response policies are therefore the org-wide override, and a common way to map `*.googleapis.com` to the restricted VIP (`199.36.153.4/30`) in VPC-SC estates.

## 4. Routing policies (public or private zones)
- **Geolocation**: `--routing-policy-type=GEO --routing-policy-data='europe-west1=10.0.1.5;us-central1=10.0.2.5'` (client's GCP region or geo for public); `--enable-geo-fencing` to never fall back.
- **Weighted round robin**: `WRR` with weights (canary at DNS level, coarse).
- **Failover**: `FAILOVER` with `--routing-policy-primary-data` and `--routing-policy-backup-data`, optionally with `--enable-health-checking`.
- A routing policy holds at most 100 items (fixed system limit).
- Prefer a global or cross-region LB over DNS tricks when you can; resolver caching delays DNS failover.

## 5. Logging and ops
- `gcloud dns policies create log --description="logging" --networks=prod-vpc --enable-logging` turns on query logging for private resolution (logs use the `dns_query` resource type); public zone query logs via `managed-zones update --log-dns-queries`. Logging can be costly at scale.
- Resolvers honour the old TTL after a change: lower the TTL before a migration.
- Quotas such as managed zones per project and record sets per zone are listed on the Cloud DNS quotas page and console; check them early for large estates.

## Gotchas
- A VM with a custom `/etc/resolv.conf` (not `169.254.169.254`) bypasses private zones, forwarding, and RPZ — enforce with OS policies.
- Forwarding-zone targets must accept queries from the **35.199.192.0/19** range, which is only reachable from a VPC network or a network connected to it; Cloud DNS cannot reach a forwarding target through transitive routing (use a peering zone instead).
- Peering zones + VPC Network Peering are unrelated features; DNS peering works without network peering.
- If you cannot add a DS record at the registrar, enabling DNSSEC in Cloud DNS has no effect; the registrar and TLD registry must both support DNSSEC.

## Verify
- [ ] `dig @8.8.8.8 example.com +dnssec` shows `ad` flag; DNSViz/`delv` reports a secure chain.
- [ ] From a VM: `dig api.internal.example` resolves; `dig host.corp.local` resolves via the forwarding zone; from on-prem, `dig @<inbound-forwarder-ip> api.internal.example` resolves.
- [ ] RPZ rule for a test domain returns `0.0.0.0` from every attached VPC within a minute.
- [ ] DNS query logs show the test queries with the correct `vmInstanceName`.

## Checked

- Date: 2026-10-27; documentation release: Google Cloud documentation pages as published on that date.
- Found wrong: `gcloud dns policies create` and `gcloud dns response-policies create` require `--description` (synopsis pages), so the examples failed without it; DNS peering supports one transitive hop, not none (zones overview); the default quota numbers were not published on the quotas page.
- Confirmed (gcloud reference): managed-zones create flags --dnssec-state, --visibility, --networks, --forwarding-targets, --private-forwarding-targets, --target-network, --target-project, --log-dns-queries; policies create --enable-inbound-forwarding, --enable-logging, --alternative-name-servers; response-policies rules create --local-data and --behavior=bypassResponsePolicy; record-sets routing policy flags.
- Confirmed (name resolution order page): outbound server policy, then network-scoped response policies, then zones, then Compute Engine internal zones; VMs must use the metadata server 169.254.169.254. Confirmed (forwarding zones page): 35.199.192.0/19 source range. Confirmed (policies page): DNS_RESOLVER address purpose filter. Confirmed (DNSSEC page): DS record needed at the registrar.
- Confirmed (quotas page): items per routing policy 100. Removed: the DNSSEC quirks, GKE and SERVFAIL gotchas, failover health-check origin and propagation-speed claims (not found in documentation).

Method: documentation only; no commands were run.
