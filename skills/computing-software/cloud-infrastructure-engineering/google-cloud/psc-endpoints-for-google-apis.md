---
id: computing-software.cloud-infrastructure-engineering.google-cloud.psc-endpoints-for-google-apis
name: psc-endpoints-for-google-apis
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, private-service-connect, psc-google-apis-endpoint, psc-endpoints-googleapis, private-dns, vpc-service-controls]
level: advanced
status: docs-checked
description: "Create a Private Service Connect endpoint for Google APIs on your own internal IP: all-apis vs vpc-sc bundles, the auto-created p.googleapis.com DNS zone, and on-prem reachability."
sources: ["https://cloud.google.com/vpc/docs/configure-private-service-connect-apis", "https://cloud.google.com/vpc/docs/about-accessing-google-apis-endpoints", "https://cloud.google.com/vpc/docs/private-service-connect"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PSC endpoints for Google APIs

Alternative to the private/restricted VIPs: a global internal IP of your choice that fronts Google APIs.

## 1. Create
```bash
gcloud services enable compute.googleapis.com dns.googleapis.com servicedirectory.googleapis.com
gcloud compute addresses create psc-apis --global --purpose=PRIVATE_SERVICE_CONNECT \
  --addresses=10.255.255.254 --network=VPC
gcloud compute forwarding-rules create pscapis --global --network=VPC \
  --address=psc-apis --target-google-apis-bundle=all-apis
```
- Name: 1-20 characters, lowercase letters and digits only, starting with a letter (it becomes part of the DNS names).
- Bundles: `all-apis` (all supported APIs) or `vpc-sc` (APIs supported by VPC Service Controls).
- The IP must be a single IPv4 address that is not inside any subnet range of the VPC or of a VPC connected by VPC Network Peering. It counts toward the project's global internal IP address quota.
- Optionally add `--service-directory-registration=REGION_NAMESPACE_URI`.

## 2. DNS
The endpoint is registered with Service Directory, which creates DNS records named `API-ENDPOINT.p.googleapis.com` (for endpoint `xyz`: `storage-xyz.p.googleapis.com`, `compute-xyz.p.googleapis.com`). If a Cloud DNS private zone for `p.googleapis.com` already exists, delete it before creating the endpoint or the Service Directory DNS zone creation fails. Either:
- point clients at those names (client libraries support custom endpoints), or
- create your own private zone `googleapis.com` with `*.googleapis.com CNAME` / A records to 10.255.255.254 so default hostnames resolve to the endpoint.

## 3. On-prem
Configure a Cloud Router custom route advertisement for the endpoint IP on the BGP session of the Cloud VPN tunnel or VLAN attachment, and forward the endpoint DNS names to an inbound forwarder entry point (inbound DNS server policy) in the same region as the tunnel or attachment.

## Gotchas
- Endpoints for Google APIs use a global internal IP: VMs in any region of the VPC can use them; they are not reachable from peered VPC networks.
- VMs without an external IP need a subnet with Private Google Access enabled to use the endpoint.
- Egress firewall rules must permit traffic to the endpoint IP (the implied allow egress rule does).
- If the endpoint is used inside a VPC Service Controls perimeter, endpoints created before 1 September 2026 are not supported and must be recreated.

## Verify
- [ ] `gcloud compute forwarding-rules describe pscapis --global` shows the endpoint; the DNS name `storage-pscapis.p.googleapis.com` (or your own zone's `storage.googleapis.com`) resolves to the endpoint IP from a VM, and `gcloud storage ls` works without an external IP.

## Checked

- Date: 2026-10-27; documentation release: Google Cloud documentation pages as published on that date.
- Confirmed (configure endpoints for Google APIs page): required APIs (Compute Engine, Service Directory, Cloud DNS), `addresses create --global --purpose=PRIVATE_SERVICE_CONNECT --addresses --network`, `forwarding-rules create --global --target-google-apis-bundle` with all-apis and vpc-sc, endpoint name rule (1-20 lowercase letters and digits, starts with a letter), p.googleapis.com DNS names (storage-xyz.p.googleapis.com), existing p.googleapis.com private zone must be deleted, Private Google Access needed for VMs without external IPs, not accessible from peered networks, on-premises custom advertisement and inbound forwarder steps.
- Confirmed (about accessing Google APIs through endpoints page): IP address requirements, global internal IP quota, VPC Service Controls note about endpoints created before September 1, 2026.
- Removed: the claim that the endpoint creates a `p.googleapis.com` private zone directly (it is a Service Directory DNS zone), the pscConnectionStatus verification and the unconfirmed list of non-googleapis domains.

Method: documentation only; no commands were run.
