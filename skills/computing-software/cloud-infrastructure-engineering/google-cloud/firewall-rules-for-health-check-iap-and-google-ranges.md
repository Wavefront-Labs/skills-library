---
id: computing-software.cloud-infrastructure-engineering.google-cloud.firewall-rules-for-health-check-iap-and-google-ranges
name: firewall-rules-for-health-check-iap-and-google-ranges
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, vpc-firewall, health-check-firewall-ranges, iap-source-range, proxy-only-subnet, google-front-end-ranges]
level: practitioner
status: docs-checked
description: "Write the firewall rules Google services need: health check ranges, IAP TCP forwarding range, proxy-only subnets for Envoy LBs, and why GFE ranges are not a stable allowlist."
sources: ["https://cloud.google.com/load-balancing/docs/health-check-concepts", "https://cloud.google.com/iap/docs/using-tcp-forwarding", "https://cloud.google.com/load-balancing/docs/proxy-only-subnets", "https://cloud.google.com/vpc/docs/configure-private-google-access", "https://cloud.google.com/dns/docs/zones/forwarding-zones"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Firewall rules for health checks, IAP and Google ranges

## Health checks
| LB type (instance group or zonal NEG backends) | Probe source ranges |
|---|---|
| Global/classic external ALB and proxy NLB; regional and cross-region ALB and proxy NLB; internal passthrough NLB | IPv4 `35.191.0.0/16`; IPv6 `2600:2d00:1:b029::/64` |
| Regional external passthrough NLB | IPv4 `35.191.0.0/16`, plus `209.85.152.0/22` and `209.85.204.0/22` for target pools; IPv6 `2600:1901:8001::/48` |
| Global external passthrough NLB | IPv4 `136.124.104.0/22`, `136.124.108.0/22`; IPv6 `2600:1904:7::/48`, `2600:1904:8::/48` |
Allow every probe range listed for your LB type: Google can add probers without notice. Check the health check concepts page for the current table (it also covers hybrid NEGs and Cloud Service Mesh).
```bash
gcloud compute firewall-rules create allow-gfe-hc --network=prod --direction=INGRESS --priority=900 \
  --source-ranges=35.191.0.0/16 --allow=tcp:80,tcp:443,tcp:8080 \
  --target-service-accounts=web@PROJECT_ID.iam.gserviceaccount.com
```

## Envoy-based regional/internal LBs
Backends accept connections from the **proxy-only subnet** range in that region and VPC (the docs example uses `10.129.0.0/23`), so create an ingress rule allowing it to the backend ports. Health checks for instance group and zonal NEG backends still come from the probe ranges above; for regional internet and hybrid NEG backends the probes come from the proxy-only subnet. Allow both.

## IAP TCP forwarding (SSH/RDP)
```bash
gcloud compute firewall-rules create allow-iap-ssh --network=prod --direction=INGRESS \
  --source-ranges=35.235.240.0/20 --allow=tcp:22,tcp:3389 --target-tags=ssh-via-iap
```
For VMs with IPv6 use `2600:2d00:1:7::/64` for IAP TCP forwarding.

## Others
- Cloud DNS outbound forwarding to on-premises targets: queries come from `35.199.192.0/19`, so allow it on the on-premises firewall.
- Private Google Access VIPs (egress, if egress is restricted): `199.36.153.8/30` for private.googleapis.com, `199.36.153.4/30` for restricted.googleapis.com.
- Do not allowlist "all Google IPs" (`goog.json`) as a security control: any GCP customer's VM uses Google IPs.

## Gotchas
- Implied deny ingress means missing health check rules make every backend unhealthy.
- Use firewall policies with address groups for these ranges across many VPCs.

## Verify
- [ ] Backend health shows HEALTHY and IAP SSH works.

## Checked

- Date: 2026-10-27; documentation release: Google Cloud documentation pages as published on that date.
- Confirmed (health check concepts page, probe IP ranges section): 35.191.0.0/16 and 2600:2d00:1:b029::/64 for GFE-based, managed Envoy and internal passthrough backends; the regional external passthrough and global external passthrough ranges; managed Envoy regional internet and hybrid NEG probes come from the proxy-only subnet.
- Removed: 130.211.0.0/22 and 2600:2d00:1:1::/64 (no longer on the page) and the claim that external ALB backend traffic comes from the same ranges (not confirmed).
- Confirmed (IAP TCP forwarding page): 35.235.240.0/20, IPv6 2600:2d00:1:7::/64. Confirmed (proxy-only subnets page): firewall rule for the proxy-only subnet, example 10.129.0.0/23.
- Confirmed (Private Google Access page): 199.36.153.8/30 private, 199.36.153.4/30 restricted. Confirmed (forwarding zones page): 35.199.192.0/19 is the Cloud DNS source range for outbound forwarding.
- Confirmed (gcloud reference): firewall-rules create flags used in the examples.

Method: documentation only; no commands were run.
