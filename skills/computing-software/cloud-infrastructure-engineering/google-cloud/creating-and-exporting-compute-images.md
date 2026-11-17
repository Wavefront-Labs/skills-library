---
id: computing-software.cloud-infrastructure-engineering.google-cloud.creating-and-exporting-compute-images
name: creating-and-exporting-compute-images
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, custom-images, create-image-from-disk, image-from-snapshot, image-export, export-image, image-families]
level: practitioner
status: docs-checked
description: "Create custom images from disks, snapshots or other images into families with storage locations, and export images to Cloud Storage as raw tarballs or VMDK/VHDX/QCOW2."
sources: ["https://cloud.google.com/compute/docs/images/create-custom", "https://cloud.google.com/compute/docs/images/export-image", "https://cloud.google.com/compute/docs/import/import-existing-image#create_image_file", "https://cloud.google.com/sdk/gcloud/reference/compute/images/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Creating and exporting Compute Engine images

## 1. From a disk (stop the VM first)
```bash
gcloud compute instances stop builder-1 --zone=<Z>
gcloud compute images create app-2026-10-16 --project=<P> \
  --source-disk=builder-1 --source-disk-zone=<Z> \
  --family=app --storage-location=europe-west2 \
  --guest-os-features=UEFI_COMPATIBLE,GVNIC --labels=app=web
```
By default creation fails if the disk is attached to a running instance; `--force` proceeds anyway (the data may be inconsistent, so avoid it for golden images).

## 2. From a snapshot or another image
```bash
gcloud compute images create app-from-snap --source-snapshot=builder-snap-0412 --family=app
gcloud compute images create app-copy --source-image=app-2026-10-16 --source-image-project=<P> \
  --storage-location=us   # copy to another location/project
```
Snapshots let you image a running VM's disk without stopping the original.

## 3. Export to Cloud Storage
```bash
gcloud compute images export --image=app-2026-10-16 --project=<P> \
  --destination-uri=gs://<B>/exports/app-2026-10-16.vmdk --export-format=vmdk
# formats include vmdk, vhdx, vpc, vdi, qcow2; omit --export-format for a disk.raw tar.gz
```
The export runs through Cloud Build (`--timeout` defaults to 2h). The Compute Engine service account used
(`--compute-service-account`) needs at minimum `roles/compute.storageAdmin`, `roles/storage.objectAdmin` and
`roles/storage.admin`; see the export page for the Cloud Build service account roles (`--cloudbuild-service-account`).

Manual fallback (no Cloud Build): attach a disk created from the image to a worker VM with device name `image-disk` and
```bash
sudo dd if=/dev/disk/by-id/google-image-disk of=/mnt/tmp/disk.raw bs=4096
sudo tar czvf myimage.tar.gz disk.raw
gcloud storage cp myimage.tar.gz gs://<B>/exports/
```
The raw file inside the archive must be named `disk.raw`.

## Gotchas
- Set the guest OS features your target VMs need (for example `UEFI_COMPATIBLE`, `GVNIC`, `SEV_CAPABLE`).
- Clean secrets, SSH host keys, machine IDs and logs before imaging.
- Check licence terms before using an exported Windows or licensed image elsewhere.

## Verify
- [ ] `gcloud compute images describe-from-family app` returns the new image as `READY`.
- [ ] Exported file downloads and boots in the target hypervisor.

## Checked

Checked 2026-10-27 against Create custom images, Export an image and the gcloud reference for images create and images export. Fixed: the roles needed by the Compute Engine service account used for export (roles/compute.storageAdmin, roles/storage.objectAdmin, roles/storage.admin), the manual export commands (dd from /dev/disk/by-id/google-image-disk, tar czvf, file named disk.raw) and the --force description. Confirmed export formats (vmdk, vhdx, vpc, vdi, qcow2), the 2h default timeout and the family, storage-location and labels flags.

Method: documentation only; no commands were run.
