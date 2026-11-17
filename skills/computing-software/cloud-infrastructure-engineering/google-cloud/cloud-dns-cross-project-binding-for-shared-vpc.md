---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-dns-cross-project-binding-for-shared-vpc
name: cloud-dns-cross-project-binding-for-shared-vpc
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-dns, cross-project-binding, dns-shared-vpc, private-zones, service-project-dns, dns-peering]
level: practitioner
status: docs-checked
description: "Let Shared VPC service projects own private DNS zones bound to the host VPC with cross-project binding, versus DNS peering, plus IAM and zone visibility checks."
sources: ["https://cloud.google.com/dns/docs/zones/cross-project-binding", "https://cloud.google.com/dns/docs/zones/zones-overview", "https://cloud.google.com/dns/docs/access-control", "https://cloud.google.com/dns/docs/vpc-name-res-order"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud DNS cross-project binding for Shared VPC

Problem: private zones must be authorised for the VPC network, which lives in the host project;
app teams in service projects want to manage their own records.

## Cross-project binding
A service project creates a private zone and binds it to the host project's network:
```bash
gcloud dns managed-zones create app-a-internal --project=app-a-prod \
  --dns-name="app-a.internal.example.com." --visibility=private \
  --networks=https://www.googleapis.com/compute/v1/projects/net-host-prod/global/networks/prod \
  --description="owned by app-a"
```
IAM: the creator needs the permission `dns.networks.bindPrivateDNSZone` on the project that owns the VPC network and `dns.managedZones.create` on the zone's project (`roles/dns.admin` covers the zone side). Both projects must be in the same organization. The zone is then resolvable by every VM in the Shared VPC network.

## Alternatives
- **Central zones in host project**: network team owns all records; simple but bottleneck.
- **DNS peering** zone: VPC A queries are answered from VPC B's resolution context (used for hub
  and spoke, or a separate DNS VPC). Transitive peering works through a single hop (at most three networks).

## Conflicts and visibility
- Overlapping zones (identical origin or a subdomain of another zone's origin) are resolved by longest suffix match. Coordinate namespaces (`TEAM.internal.example.com`).
- Check effective zones for a network:
  ```bash
  gcloud dns managed-zones list --project=net-host-prod --filter="visibility=private"
  gcloud dns managed-zones list --project=app-a-prod --filter="privateVisibilityConfig.networks.networkUrl~net-host-prod"
  ```

## Gotchas
- Cross-project binding cannot attach a zone to a VPC network outside the organization.

## Verify
- [ ] A VM in another service project resolves `api.app-a.internal.example.com` to the record set.

## Checked

- Date: 2026-10-27; documentation release: Google Cloud documentation pages as published on that date.
- Found wrong: `roles/dns.networkUser` is not a role listed on the Cloud DNS access control page; the cross-project binding page requires the permission dns.networks.bindPrivateDNSZone on the network's project and dns.managedZones.create on the zone's project. The peering note said no transitivity beyond one hop; the zones overview allows a single transitive hop.
- Confirmed (cross-project binding page): same-organization limitation, `gcloud dns managed-zones create --visibility=private --networks=NETWORK_URL` run in the zone's project, URL form https://www.googleapis.com/compute/v1/projects/.../global/networks/....
- Confirmed (zones overview and resolution order pages): overlapping zones resolved by longest suffix; Shared VPC zones associated directly with the host network.
- Removed: identical-name creation failure, host-network deletion and Asset Inventory statements (not found in documentation).

Method: documentation only; no commands were run.
