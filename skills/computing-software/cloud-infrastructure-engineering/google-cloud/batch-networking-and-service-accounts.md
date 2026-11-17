---
id: computing-software.cloud-infrastructure-engineering.google-cloud.batch-networking-and-service-accounts
name: batch-networking-and-service-accounts
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-batch, batch-networking, batch-service-account, private-ip, shared-vpc, iam]
level: practitioner
status: docs-checked
description: "Run Cloud Batch jobs on a private subnet (Shared VPC, no external IPs, NAT and Private Google Access) under a dedicated service account with exactly the roles the agent needs."
sources: ["https://cloud.google.com/batch/docs/networking-overview", "https://cloud.google.com/batch/docs/create-run-job-custom-service-account", "https://cloud.google.com/batch/docs/get-started#project-prerequisites"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Batch networking and service accounts

## 1. Service account for the job VMs
```bash
SA=batch-render@<P>.iam.gserviceaccount.com
gcloud iam service-accounts create batch-render --project=<P>
for r in roles/batch.agentReporter roles/logging.logWriter; do
  gcloud projects add-iam-policy-binding <P> --member=serviceAccount:$SA --role=$r; done
# add the data-access roles your tasks need (for example on the buckets or registries they use)
# the submitter must be able to act as it
gcloud iam service-accounts add-iam-policy-binding $SA --member=group:media-eng@example.com --role=roles/iam.serviceAccountUser
```
Submitters need `roles/batch.jobsEditor` on the project and `roles/iam.serviceAccountUser` on the job's service account. Without an explicit SA, jobs use the Compute Engine default service account. `roles/batch.agentReporter` lets the VMs report their state; `roles/logging.logWriter` lets jobs write logs.

## 2. Private networking in the job
```json
"allocationPolicy": {
  "serviceAccount": {"email": "batch-render@<P>.iam.gserviceaccount.com"},
  "network": {"networkInterfaces": [{
    "network": "projects/<HOST>/global/networks/prod",
    "subnetwork": "projects/<HOST>/regions/europe-west2/subnetworks/batch",
    "noExternalIpAddress": true
  }]},
  "instances": [{"policy": {"machineType": "c3-standard-8"}}],
  "tags": ["batch-workers"]
}
```
With `noExternalIpAddress`:
- use **Cloud NAT** or **Private Google Access** so the VMs can reach the APIs the job uses (all Batch jobs use the Batch and Compute Engine APIs, and very often Cloud Logging);
- other internet sources (for example public image registries) need Cloud NAT or external IPs;
- the network can be a Shared VPC network: give `network` and `subnetwork` as URLs of the host project's resources.

## 3. Firewall
Firewall rules for the network control connections between the job VMs. Use `allocationPolicy.tags` (for example `batch-workers`) to target them.

## Gotchas
- Org policy `compute.vmExternalIpAccess` makes jobs whose VMs would get external IPs fail with "Constraint constraints/compute.vmExternalIpAccess violated"; block external access for all VMs in the job or use an exempt project.
- Missing `roles/batch.agentReporter` on the job service account produces "No VM has agent reporting correctly" in `statusEvents`.
- Jobs that block external access need Cloud NAT or Private Google Access, and VPC Service Controls perimeters require jobs without external IPs.

## Verify
- [ ] Job VMs show no external IP in the Compute Engine console.
- [ ] Tasks reach the APIs they need and write logs; the job details show the job service account, not the default one.

## Checked
2026-10-27. Confirmed against Batch Get started prerequisites (agentReporter, logWriter, jobsEditor, serviceAccountUser on the job's service account, default Compute Engine SA), Networking overview (Cloud NAT or Private Google Access for VMs without external IPs, vmExternalIpAccess), Troubleshooting page (no agent reporting, vmExternalIpAccess message, VPC Service Controls with external IPs) and the Batch discovery document (NetworkInterface fields, tags, noExternalIpAddress). Removed: artifactregistry.reader and storage.objectAdmin grants, Shared VPC compute.networkUser claim, 199.36.153.8/30 egress advice, instance-template override claim, the labels filter in the verify step, the Artifact Registry and GCS list for Private Google Access.
Method: documentation only; no commands were run.
