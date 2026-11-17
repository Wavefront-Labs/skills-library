---
id: computing-software.cloud-infrastructure-engineering.google-cloud.external-ip-charges-and-unused-static-ips
name: external-ip-charges-and-unused-static-ips
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, network-service-tiers, external-ip-charges, unused-static-ips, ipv4-pricing, cleanup, recommender]
level: practitioner
status: docs-checked
description: "Control external IPv4 charges: in-use versus reserved-unused rates, finding RESERVED static IPs, the idle IP address recommender, removing VM external IPs and org-policy control."
sources: ["https://cloud.google.com/vpc/network-pricing#ipaddress", "https://cloud.google.com/compute/docs/ip-addresses/reserve-static-external-ip-address", "https://cloud.google.com/recommender/docs/recommenders#unused_ip"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# External IP charges and unused static IPs

For current rates see the VPC network pricing page (External IP address pricing); this skill keeps structure, not prices.

## How charging works (VPC pricing page)
- Static and ephemeral external IPv4 addresses are charged. A static external IP that you reserve but do not assign to a resource such as a VM or a forwarding rule is charged at a higher rate than an address in use.
- Separate in-use rates exist for standard VMs and for preemptible and Spot VMs. Addresses used by Cloud NAT are charged at their own listed rate. Addresses attached to forwarding rules or used as the public IP of a Cloud VPN tunnel are not charged.
- Standard-VM addresses have a free tier limited to one hour per month per account.
- No charge for internal IPs, for external IPv6 ranges assigned to subnets or VMs, or for static regional IPv6 addresses (Preview).
- "In use" for a static IP means associated with a VM, running or stopped. If the VM is deleted or the IP is dissociated, the IP is not in use. An ephemeral IP counts as in use only while its VM runs; it is released when the VM stops or is deleted.
- An external IP assigned to a VPN gateway but not used by a tunnel is charged.

## Find unused
```bash
gcloud compute addresses list            # STATUS column: RESERVED (not in use) or IN_USE
gcloud compute addresses list --global
gcloud compute addresses list --regions=REGION1,REGION2
gcloud compute addresses describe ADDRESS_NAME --region=REGION   # `users` lists the consumer
```
The Recommender page lists an Idle IP address recommender, ID `google.compute.address.IdleResourceRecommender` ("Remove unused IPs", included in BigQuery export). It gives a per-project view of what to remove.

## Remove VM external IPs
Find the access config name with `gcloud compute instances describe INSTANCE_NAME` (typically `external-nat`, type `ONE_TO_ONE_NAT`), then:
```bash
gcloud compute instances delete-access-config INSTANCE_NAME --access-config-name="ACCESS_CONFIG_NAME"
```
To stop new external IPs, the organisation policy list constraint `constraints/compute.vmExternalIpAccess` allows only listed instances to have an external IP, ephemeral or static. Google recommends an allowedValues list; it applies only to compute instances (including GKE nodes created in an in-scope project) and, with Shared VPC, must be applied to each service project too.

## Release
Deleting an instance does not release a static external IP: delete the address resource yourself (see "Release a static external IP address" in the VPC docs). Check DNS, allowlists and firewall references first.

## Verify
- [ ] `gcloud compute addresses list` shows no RESERVED external addresses without an owner.

## Checked
Confirmed 2026-11-08 against the VPC network pricing page (External IP address pricing, "In use or not"), the static external IP page, and the Recommenders page. Removed claims the pages do not state: the `gcloud asset search-all-resources` command, the `--filter` expressions, the billing SKU names, Cloud NAT-as-in-use wording for manual IPs, the claim a released IP cannot be reclaimed, the 30-day rule, and the Cloud Run-style price comparisons. Prices deliberately not kept.
Method: docs-only read of cited pages, 2026-11-08
