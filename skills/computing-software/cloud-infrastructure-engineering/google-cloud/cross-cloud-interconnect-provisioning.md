---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cross-cloud-interconnect-provisioning
name: cross-cloud-interconnect-provisioning
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cross-cloud-interconnect-provisioning, interconnect, aws-direct-connect, azure-expressroute, multicloud-networking, vlan-attachments]
level: practitioner
status: docs-checked
description: "Provision Cross-Cloud Interconnect to AWS, Azure, OCI or Alibaba: pick locations, order 10G/100G ports for redundancy, connect the other cloud side, VLAN attachments and BGP."
sources: ["https://cloud.google.com/network-connectivity/docs/interconnect/concepts/cci-overview", "https://cloud.google.com/sdk/gcloud/reference/compute/interconnects/create", "https://cloud.google.com/sdk/gcloud/reference/compute/interconnects/attachments/dedicated/create", "https://cloud.google.com/sdk/gcloud/reference/compute/interconnects/remote-locations/list"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-Cloud Interconnect provisioning

Google provisions a dedicated physical link between Google's edge and another cloud provider's
edge (AWS Direct Connect, Azure ExpressRoute Direct, OCI FastConnect, Alibaba Express Connect) in
the same metro. No colocation or cross-connect ordering on your side.

## Plan
1. Choose a supported location pair (docs list metros per remote cloud and Google regions).
2. Redundancy: at minimum, put connections in two edge availability domains (zones within a metro). To qualify for the 99.99% SLA use the multi-region topology (two pairs of connections in different regions) or the single-region topology described on the overview page.
3. Capacity: AWS and OCI offer 10, 100 and 400 Gbps; Azure and Alibaba Cloud offer 10 and 100 Gbps.

## Order (Google side)
```bash
gcloud compute interconnects create cci-aws-1 --interconnect-type=DEDICATED \
  --link-type=LINK_TYPE_ETHERNET_10G_LR --requested-link-count=1 \
  --remote-location=REMOTE_LOCATION --location=GOOGLE_EDGE_LOCATION \
  --noc-contact-email=netops@example.com --admin-enabled
gcloud compute interconnects describe cci-aws-1 --format="yaml(state,remoteLocation,provisionedLinkCount)"
```
List valid values with `gcloud compute interconnects remote-locations list` and `gcloud compute interconnects locations list`. After the order you buy matching ports from the remote provider using the details Google gives you.

## Remote side (AWS example)
Purchase the redundant ports at the remote provider with the information Google provides, then configure the provider's virtual interface (VLAN and BGP) to match the Google VLAN attachment. Follow the per-provider page (AWS, Azure, OCI, Alibaba Cloud).

## Google VLAN attachments and BGP
```bash
gcloud compute interconnects attachments dedicated create cci-aws-1-va --region=europe-west2 \
  --interconnect=cci-aws-1 --router=cr-cci-ew2 --vlan=1001 --bandwidth=10g
gcloud compute routers add-bgp-peer cr-cci-ew2 --region=europe-west2 --peer-name=aws-1 \
  --interface=INTERFACE_NAME --peer-ip-address=169.254.10.2 --peer-asn=64512
```
`--bandwidth` takes values such as `1g`, `10g`, `100g`, `400g`; `--mtu` must be 1440 (default), 1460, 1500 or 8896.

## Gotchas
- Provisioning time is listed as 1-4 weeks on the overview page; order early.
- MTU: Cross-Cloud Interconnect supports jumbo MTUs with any of the remote clouds, but check the remote provider's documentation for its supported values.
- Overlapping CIDRs between clouds break routing: plan IP space first.

## Verify
- [ ] BGP sessions up on both connections; failover test drops one link with no app impact.

## Checked

- Date: 2026-10-27; documentation release: Google Cloud documentation pages as published on that date.
- Found wrong: `--bandwidth=BPS_10G` is not accepted by gcloud (allowed values are 50m ... 10g, 20g, 50g, 100g, 400g); capacity list omitted 400 Gbps for AWS and OCI; the example remote location name was not a documented value.
- Confirmed (overview page): supported remote clouds (AWS, Azure, OCI, Alibaba Cloud), port sizes per provider, two edge availability domains minimum, 99.99% multi-region and single-region options, provisioning time 1-4 weeks, jumbo MTU support.
- Confirmed (gcloud reference): `interconnects create` flags --interconnect-type DEDICATED, --link-type, --requested-link-count, --remote-location, --location, --noc-contact-email, --admin-enabled; `attachments dedicated create` --interconnect --router --vlan --bandwidth --mtu (1440, 1460, 1500, 8896); `remote-locations list`.
- Removed: dedicated-Cloud-Router-per-connection advice and pricing remarks (not in documentation read). The connection order page URL redirected in a loop and was dropped from sources.

Method: documentation only; no commands were run.
