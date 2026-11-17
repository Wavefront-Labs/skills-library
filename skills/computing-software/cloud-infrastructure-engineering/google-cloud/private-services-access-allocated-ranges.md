---
id: computing-software.cloud-infrastructure-engineering.google-cloud.private-services-access-allocated-ranges
name: private-services-access-allocated-ranges
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, private-service-connect, psa-allocated-range, psa-peering-setup, cloud-sql, service-networking]
level: advanced
status: docs-checked
description: "Set up private services access for Cloud SQL and others: allocate ranges, create the servicenetworking peering, expand ranges, and export routes to on-prem."
sources: ["https://cloud.google.com/vpc/docs/configure-private-services-access", "https://cloud.google.com/vpc/docs/private-services-access", "https://cloud.google.com/sql/docs/mysql/configure-private-services-access"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Private services access allocated ranges

PSA = a VPC peering between your VPC and a Google-managed service producer VPC, using IP ranges you allocate.

## 1. Allocate and connect
```bash
gcloud compute addresses create google-managed-services-<VPC> --global \
  --purpose=VPC_PEERING --addresses=<RANGE_START> --prefix-length=16 --network=<VPC>
gcloud services vpc-peerings connect --service=servicenetworking.googleapis.com \
  --ranges=google-managed-services-<VPC> --network=<VPC>
```
- For Google services the minimum is one /24 block and the recommended size is a /16. Cloud SQL needs a free /24 for each new region or database type.
- Omit `--addresses` and give only `--prefix-length` to let Google pick an unused range.
- Pick the range from your IPAM so it does not overlap on-prem. Custom routes whose destinations match or fit inside an allocated range reduce its usable portion and can cause "allocation exhausted" errors.

## 2. Expand later
```bash
gcloud compute addresses create psa-range-2 --global --purpose=VPC_PEERING --addresses=<RANGE_START_2> --prefix-length=20 --network=<VPC>
gcloud services vpc-peerings update --service=servicenetworking.googleapis.com \
  --ranges=google-managed-services-<VPC>,psa-range-2 --network=<VPC>
```
List every range you want to keep in `--ranges`. After modifying or removing an allocated range the Cloud SQL guide says to update the peering with `--force`; read that page before using it.

## 3. Reach PSA services from on-prem
The peering is named `servicenetworking-googleapis-com`. Update it to export custom routes to the producer network, and make sure the allocated prefixes are advertised to on-prem through Cloud Router:
```bash
gcloud compute networks peerings update servicenetworking-googleapis-com --network=<VPC> \
  --export-custom-routes
```
Do not export custom routes that overlap ranges used for Private Google Access. VPC Network Peering is not transitive, so a private connection is not available to VPC networks peered with yours.

## Verify
- [ ] `gcloud services vpc-peerings list --network=<VPC>` shows the ranges; `gcloud compute networks peerings list --network=<VPC>` shows the peering ACTIVE.

## Checked
2026-10-28. Confirmed against Configure private services access, the private services access overview and the Cloud SQL private services access page: /24 minimum and /16 recommendation, Cloud SQL /24 per region or type, `--purpose=VPC_PEERING`, `--prefix-length`, address omission, peering name, custom-route interaction, exporting custom routes and Cloud Router advertisement, no transitivity, the `--force` note. gcloud commands checked against the reference with check_commands.py. Removed: PSC-support list, `--import-custom-routes`, "each service and region carves subnets" sizing detail, deletion-blocked claim, example ranges.
Method: documentation only; no commands were run.
