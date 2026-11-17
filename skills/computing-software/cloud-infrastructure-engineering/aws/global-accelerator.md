---
id: computing-software.cloud-infrastructure-engineering.aws.global-accelerator
name: global-accelerator
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, global-accelerator, aws-global-accelerator, anycast, static-ip, byoip, endpoint-group, traffic-dial, endpoint-weights, client-affinity, client-ip-preservation, custom-routing-accelerator, multi-region, failover, tcp-udp-acceleration, edge-network, listener, health-checks, accelerator-flow-logs, cross-region-load-balancing, networking]
level: practitioner
status: docs-checked
description: "Front multi-region ALB/NLB/EC2 with Global Accelerator: static anycast IPs, endpoint groups with traffic dials and weights, quotas, client IP preservation, vs CloudFront."
sources: ["https://docs.aws.amazon.com/global-accelerator/latest/dg/limits-global-accelerator.html", "https://docs.aws.amazon.com/global-accelerator/latest/dg/about-listeners.html", "https://docs.aws.amazon.com/global-accelerator/latest/dg/about-endpoint-groups-traffic-dial.html", "https://github.com/boto/botocore/tree/develop/botocore/data/globalaccelerator"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# AWS Global Accelerator — static anycast front door for multi-region TCP/UDP

**Goal:** one pair of static IP addresses that customers can allowlist, traffic that
enters the AWS network at the nearest edge, and regional steering without a DNS change.
The backends it fronts are built in `...aws.elastic-load-balancing`; the alternative
DNS-based steering is in `...aws.route53-routing-and-health-checks`.

## 1. When it is the right tool (and when CloudFront is)
| Need | Global Accelerator | CloudFront |
|---|---|---|
| Static IPs for allowlisting | yes (static anycast IPs, optional dual-stack) | no |
| Non-HTTP (TCP or UDP) | yes (listeners take TCP and UDP) | no |
| Caching | no | yes |
| Deterministic per-client routing | yes (custom routing accelerator) | no |
HTTP(S) with cacheable content → CloudFront. Everything else that must be global, or
anything whose clients hardcode IPs, → Global Accelerator. Both can be stacked.
Costs: see the Global Accelerator pricing page.

## 2. Build one
```
aws globalaccelerator create-accelerator --name api-prod --ip-address-type IPV4 --enabled \
  --region <API_REGION>
aws globalaccelerator create-listener --accelerator-arn <ARN> --protocol TCP \
  --port-ranges FromPort=443,ToPort=443 --client-affinity NONE --region <API_REGION>
aws globalaccelerator create-endpoint-group --listener-arn <LARN> \
  --endpoint-group-region eu-west-1 --traffic-dial-percentage 100 \
  --endpoint-configurations EndpointId=<ALB_ARN>,Weight=128,ClientIPPreservationEnabled=true \
  --health-check-protocol HTTPS --health-check-path /healthz --health-check-interval-seconds 10 \
  --threshold-count 3 --region <API_REGION>
```
- The accelerator is global, but the `aws globalaccelerator` control-plane API is served from
  one Region: look up the Region to pass as `--region` in the API reference.
- **Listeners** take port ranges and a protocol (`TCP` or `UDP`; there is no combined value).
  **Client affinity** `SOURCE_IP` pins a client to one endpoint across connections;
  `NONE` is the default per-flow behaviour.
- **Endpoint groups** map to one Region each. **Traffic dial** (0-100, default 100) controls the
  percentage of traffic already directed to that group; set 0 to cut a Region off (a dial
  change applies to new connections only, existing connections are not terminated, and
  health checks are unaffected). **Endpoint weights** (0-255) split traffic within the group.
- Health check settings: protocol `TCP`, `HTTP` or `HTTPS`; interval 10-30 seconds;
  threshold count 1-10; up to 10 endpoints per `create-endpoint-group` call.
- Dual-stack: `--ip-address-type DUAL_STACK` (the other value is `IPV4`).

## 3. Client IP preservation
- `ClientIPPreservationEnabled` is a per-endpoint setting in the endpoint configuration.
  Which endpoint types support it, and the security group and subnet requirements, are on the
  "Preserve client IP addresses" page of the Global Accelerator guide: read it before relying
  on it, and test that targets see the real client IP.

## 4. Custom routing accelerators
A separate accelerator type for workloads where your own application chooses the exact
destination; the account quota for these is separate from standard accelerators (below).
Details are in the custom routing section of the guide.

## 5. Quotas (from the Global Accelerator quotas page)
- 20 standard accelerators and 10 custom routing accelerators per account (both can be raised).
- 10 listeners per accelerator (raisable); 10 port ranges per listener.
- 42 endpoint groups per accelerator across all listeners: (listeners x endpoint groups)
  must not exceed 42.
- 10 port overrides per endpoint group (raisable).
- Endpoints per endpoint group: 10 in each case (raisable for NLB, EC2, Elastic IP and subnet
  endpoints; ALB-only and mixed-type groups are fixed at 10).

## Gotchas
- An endpoint group with a traffic dial of 100 can still receive little traffic: the dial is
  applied only to traffic already directed to the group, so a closer healthy group serves
  its own clients first. "Why is that Region idle" is often geography, not a bug.
- Deleting the accelerator releases its static IPs; protect it in your IaC tooling.

## Verify
- [ ] `describe-accelerator` shows the accelerator deployed with its static IPs.
- [ ] Target logs show the real client IP (preservation on) or the expected forwarding header.
- [ ] Setting a Region's traffic dial to 0 moves new connections away from it.
- [ ] The decision vs CloudFront is documented.

## Checked
2026-10-31. Confirmed in the Global Accelerator quotas page, the traffic-dial page, the listeners page and the botocore globalaccelerator model: all quota figures above; traffic dial 0-100 default 100 and its behaviour; endpoint weights 0-255; protocols TCP/UDP; client affinity NONE/SOURCE_IP; IPv4/DUAL_STACK; health check protocols, interval 10-30 and threshold 1-10; `ClientIPPreservationEnabled` field. Removed as unconfirmed: the 30-second failover figure, the fixed API Region, endpoint-type and internal-ALB details, ENI and security group behaviour, flow-log and CloudWatch metric names, idle timeouts, BYOIP and Shield statements, zonal shift integration, deletion order, and pricing.
Method: documentation only; no commands were run.
