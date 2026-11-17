---
id: computing-software.cloud-infrastructure-engineering.google-cloud.serverless-vpc-access-connectors
name: serverless-vpc-access-connectors
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, app-engine, serverless-vpc-access-connector, vpc-access-connector, cloud-run, cloud-run-functions, shared-vpc, egress-settings]
level: practitioner
status: docs-checked
description: "Create Serverless VPC Access connectors for App Engine, Cloud Run and functions: /28 subnet, sizing, Shared VPC, network tags, and Direct VPC egress as the alternative."
sources: ["https://cloud.google.com/vpc/docs/serverless-vpc-access", "https://cloud.google.com/vpc/docs/configure-serverless-vpc-access"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Serverless VPC Access connectors

A connector lets serverless products (App Engine, Cloud Run, Cloud Run functions) send requests
to private IPs in a VPC. Google recommends **Direct VPC egress** for Cloud Run services and jobs
(no connector required); use a connector when Direct VPC egress is not an option.
Connector creation fails in Assured Workloads environments: use Direct VPC egress there.

## Create
```bash
gcloud compute networks subnets create vpcconn-ew2 --network=prod --region=europe-west2 --range=10.8.0.0/28
gcloud compute networks vpc-access connectors create conn-ew2 --region=europe-west2 \
  --subnet=vpcconn-ew2 --machine-type=e2-micro --min-instances=2 --max-instances=10
```
- Each connector needs its own dedicated `/28` subnet (purpose PRIVATE) that nothing else uses
  (VMs, Private Service Connect, load balancers); it cannot be expanded.
- Machine type is one of `f1-micro`, `e2-micro` (default) or `e2-standard-4`; minimum instances
  default 2, maximum defaults to 10; connectors cannot mix machine types.
- Enable the API first: `gcloud services enable vpcaccess.googleapis.com`.
- Shared VPC, connector in a service project: a Shared VPC network administrator must create the
  subnet first, then you create the connector against that existing subnet. Connectors in a
  standalone VPC or a host project get their firewall rules created automatically; service-project
  connectors need firewall rules you add yourself.

## Use
```bash
gcloud run deploy api --vpc-connector=conn-ew2 --vpc-egress=private-ranges-only
gcloud functions deploy fn --gen2 --vpc-connector=conn-ew2 --egress-settings=private-ranges-only
```

## Sizing
Throughput scales with machine type and instance count. Connectors **scale out but do not scale
in**; to shrink after a scale-out, recreate the connector, and set a low maximum to cap scale-out.

## Gotchas
- Firewall network tags: universal `vpc-connector` (all connectors) and unique
  `vpc-connector-REGION-CONNECTOR_NAME` (one connector); target them in firewall rules.
- To reach resources across several VPC networks or projects, also configure Shared VPC or VPC Network Peering.

## Verify
- [ ] `gcloud compute networks vpc-access connectors describe conn-ew2 --region=europe-west2` shows READY and the service reaches a private IP.

## Checked
2026-10-28. Confirmed against the Serverless VPC Access overview and Configure Serverless VPC Access pages: Direct VPC egress recommendation, /28 dedicated subnet, machine types and instance defaults, no scale-in, Shared VPC subnet and firewall behaviour, network tags, Assured Workloads limitation. gcloud commands checked against the reference with check_commands.py. Removed: `roles/vpcaccess.user`, region-match and CPU claims, app.yaml sample, latency and cost comparisons, App Engine claim.
Method: documentation only; no commands were run.
