---
id: computing-software.cloud-infrastructure-engineering.google-cloud.creating-vms-and-choosing-machine-types
name: creating-vms-and-choosing-machine-types
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, compute-engine, instance-creation, gcloud-compute-instances-create, custom-machine-types, machine-family-comparison, e2-vs-n2, hyperdisk]
level: practitioner
status: docs-checked
description: "Create Compute Engine VMs with gcloud and pick the machine series (E2, N2/N4, C3/C4, C4A Arm, M, accelerator) or a custom shape, with the documented custom-shape rules."
sources: ["https://docs.cloud.google.com/compute/docs/instances/create-start-instance", "https://docs.cloud.google.com/compute/docs/machine-resource", "https://docs.cloud.google.com/compute/docs/instances/creating-instance-with-custom-machine-type", "https://docs.cloud.google.com/compute/docs/access/service-accounts"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Creating VMs and choosing machine types

## 1. Series cheat sheet (from the Machine families page)
| Series | Pick for | Watch |
|---|---|---|
| E2 | low-cost day-to-day: low-traffic web, back-office, dev/test; shared-core `e2-micro`, `e2-small`, `e2-medium` | up to 32 vCPUs; CPU vendor chosen for you at creation |
| N2 / N2D / N4 | balanced price-performance (N2 Intel, N2D AMD EPYC, N4 Intel Emerald Rapids) | N4 supports Hyperdisk only, no Persistent Disk |
| C3 / C3D / C4 / C4D | consistently high performance: high-traffic web, databases, caches | C4 lists Hyperdisk types, no Persistent Disk |
| C4A / N4A / T2A (Arm) | scale-out web, containers, microservices | need arm64 images and binaries |
| T2D | scale-out x86 (AMD EPYC Milan), up to 60 vCPUs | no custom machine types |
| M3 / M4 / X4 / X5 | memory-optimized: SAP HANA, Redis, SQL Server (M4); X4 and X5 are bare metal | very large memory shapes |
| H3 / H4D | HPC | H4D adds Cloud RDMA for multi-node workloads |
| A2 / A3 / G2 (and newer A4, G4) | GPUs: A2 A100, A3 H100/H200, G2 L4 | GPUs attach automatically except on N1 |
```bash
gcloud compute machine-types list --zones=<ZONE> --filter='name~^(n4|c4)-standard' --format='table(name,guestCpus,memoryMb)'
```

## 2. Custom shapes
Custom machine types exist for N4, N4A, N4D, N2, N2D, N1 and E2 (and G2 in a limited form).
```bash
--custom-vm-type=n2 --custom-cpu=6 --custom-memory=20GB      # same as --machine-type=n2-custom-6-20480
--custom-extensions                                           # needed for extended memory with the --custom-* flags
```
- Unitless `--custom-memory` defaults to GB and must be an integer; use `MB`/`GB` suffixes for others (for example `5.75GB`). In `--machine-type` names memory is an integer in MB with no suffix; the API needs a multiple of 256 MB (1,024 MB for G2). Units are binary (1 GB = 1,024 MB).
- Extended memory appends `-ext`, for example `n2-custom-48-720896-ext`; E2, G2 and predefined types do not support it.
- Allowed shapes differ per series: N2 takes 2 to 80 vCPUs, even up to 32 then multiples of 4, with 0.5 to 8 GB per vCPU; E2 takes 2 to 32 even vCPUs with 0.5 to 8 GB per vCPU. E2 shared-core custom uses `e2-custom-<micro|small|medium>-<MB>`. Check the custom machine type page for the other series.
- On-demand custom types cost about 5% more than the equivalent predefined type; see Google's pricing pages for amounts.

## 3. A production-style create
```bash
gcloud compute instances create api-1 --project=<PROJECT_ID> --zone=<ZONE> \
  --machine-type=n4-standard-4 \
  --image-family=debian-12 --image-project=debian-cloud \
  --boot-disk-type=hyperdisk-balanced --boot-disk-size=50GB \
  --subnet=projects/<HOST_PROJECT>/regions/<REGION>/subnetworks/app --no-address \
  --service-account=api-vm@<PROJECT_ID>.iam.gserviceaccount.com --scopes=cloud-platform \
  --shielded-secure-boot --shielded-vtpm --shielded-integrity-monitoring \
  --labels=app=api,env=prod --tags=api --deletion-protection
```
The flags above passed `check_commands.py` against the gcloud reference. Creating instances needs `roles/compute.instanceAdmin.v1` (permission `compute.instances.create`); specifying a subnet needs `compute.subnetworks.use`; giving a VM an external IP on a VPC network needs `compute.subnetworks.useExternalIp`.
`gcloud compute instances create` cannot create bulk instances (use `gcloud compute instances bulk create`) or container-based instances (use `create-with-container`). The console's Equivalent code button generates gcloud, REST or Terraform for a configuration.

## Gotchas
- Pick a boot disk type the series supports (N4 is Hyperdisk only; the machine families page lists disk types per series).
- Without an explicit service account, VMs created with gcloud or the console get the default Compute Engine service account, which depending on organization policy may be granted Editor on the project. Google strongly recommends disabling the automatic Editor grant (organizations created after 3 May 2024 enforce that policy by default) and replacing Editor with narrower roles; check impact with Policy Simulator first.
- Machine type names ending in `-metal` are bare metal instances without a hypervisor.

## Verify
- [ ] `gcloud compute instances describe api-1 --zone=<ZONE> --format='value(machineType,serviceAccounts[0].email)'` matches intent.

## Checked
Checked 2026-11-08 against the Compute Engine Machine families, Create and start an instance, Custom machine types and service accounts pages. Removed: "no GPUs or local SSD" for E2, the MIG advice, the Cloud NAT / Private Google Access note for `--no-address`, the OS Login and OS Config metadata keys, the zone-availability command and the "shielded VM output" check, none of which those pages state. Prices are not kept.
Method: documentation only; no commands were run.
