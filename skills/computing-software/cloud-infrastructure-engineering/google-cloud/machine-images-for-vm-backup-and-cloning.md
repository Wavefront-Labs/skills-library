---
id: computing-software.cloud-infrastructure-engineering.google-cloud.machine-images-for-vm-backup-and-cloning
name: machine-images-for-vm-backup-and-cloning
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, compute-engine, machine-images, vm-backup, vm-cloning, multi-disk-backup]
level: practitioner
status: docs-checked
description: "Capture a whole VM (config, metadata, all disks) as a machine image for backup, cloning or cross-project copies, and know when an image or snapshot is the better tool."
sources: ["https://cloud.google.com/compute/docs/machine-images", "https://cloud.google.com/compute/docs/machine-images/create-machine-images", "https://cloud.google.com/compute/docs/machine-images/create-instance-from-machine-image"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Machine images

A machine image stores **everything to rebuild a VM**: machine type, metadata, labels, network
tags, SA, scheduling and all attached disks (stored as differential snapshots).

## When to use which
| Need | Use |
|---|---|
| Rebuild/clone one specific VM with all its disks | machine image |
| Base OS for many VMs / MIG templates | custom image |
| Regular disk backups with retention | snapshot schedules |

## 1. Create
```bash
gcloud compute machine-images create legacy-app-2026-10-16 --project=<P> \
  --source-instance=legacy-app --source-instance-zone=<Z> --storage-location=europe-west2
# --guest-flush asks the guest for an application-consistent image
```
Works on running VMs; data across disks is captured crash-consistently at one point in time (not application-consistent unless the OS and application take part).

## 2. Restore or clone
```bash
gcloud compute instances create legacy-app-clone --zone=<Z2> \
  --source-machine-image=projects/<P>/global/machineImages/legacy-app-2026-10-16 \
  --machine-type=n2-standard-4 --subnet=<OTHER_SUBNET> --no-address
```
Flags override the stored properties (machine type, network, zone). For clones, change the
hostname, network settings and any license/identity that must be unique.

## 3. Share across projects
```bash
gcloud compute machine-images add-iam-policy-binding legacy-app-2026-10-16 \
  --member=serviceAccount:<DEPLOYER>@<P2>.iam.gserviceaccount.com --role=roles/compute.admin
```
(Users need `compute.machineImages.useReadOnly`; `roles/compute.admin` or a custom role on the image.)

## Gotchas
- Local SSD contents are not captured (only the device mapping); instances with attached regional disks cannot be created from a machine image. Check the limitations pages.
- CSEK-protected disks need their keys at create and restore time.
- Data lives in `--storage-location`; residency policies apply.
- The machine image must be READY before you create instances from it; overrides cannot change disk properties other than the name.
- When cloning into another project, set the network and subnet explicitly with `--subnet`.

## Verify
- [ ] `gcloud compute machine-images describe <MI> --format='value(status,totalStorageBytes)'` is READY.
- [ ] A clone boots in a sandbox project and the application starts.

## Checked

Checked 2026-10-27 against Machine images, Create machine images, Create an instance from a machine image and the gcloud reference for machine-images create. Confirmed: differential snapshots, crash-consistent capture across disks, --guest-flush, --storage-location, --source-machine-image overrides, Local SSD contents not captured, no regional disks, READY state needed, compute.machineImages.useReadOnly. Removed the unconfirmed VSS and cross-project network claims.

Method: documentation only; no commands were run.
