---
id: computing-software.cloud-infrastructure-engineering.google-cloud.gpu-vms-and-driver-installation
name: gpu-vms-and-driver-installation
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, compute-engine, gpu-vms, gpu-drivers, accelerator-optimized, nvidia, cuda, deep-learning-vm]
level: practitioner
status: docs-checked
description: "Create GPU VMs on accelerator-optimized (A3, A2, G2) or N1 machines, install NVIDIA drivers (installer or Secure Boot path), and handle maintenance and verification."
sources: ["https://docs.cloud.google.com/compute/docs/gpus/create-vm-with-gpus", "https://docs.cloud.google.com/compute/docs/gpus/install-drivers-gpu", "https://docs.cloud.google.com/compute/docs/accelerator-optimized-machines", "https://docs.cloud.google.com/deep-learning-vm/docs/images"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# GPU VMs and driver installation

## 1. Pick the shape
| GPU | Machine | Attach |
|---|---|---|
| L4 | G2 | implicit in machine type |
| A100 40/80 GB | A2 (`a2-highgpu-1g`, `a2-ultragpu-1g`) | implicit |
| H100 / H200 / B200 | A3 / A4 families | implicit; high-bandwidth networking (GPUDirect) |
| T4, V100, P4 | N1 + `--accelerator=type=<GPU_TYPE>,count=1` | explicit |
```bash
gcloud compute accelerator-types list --filter='zone:europe-west4-a'
gcloud compute instances create infer-1 --zone=europe-west4-a --machine-type=<G2_MACHINE_TYPE> \
  --maintenance-policy=TERMINATE --restart-on-failure \
  --image-family=debian-12 --image-project=debian-cloud --boot-disk-size=200GB \
  --no-address --service-account=<SA> --scopes=cloud-platform
```
Live migration support depends on the GPU: the accelerator-optimized machines page lists G2 (L4) and N1 with T4 or P4 as supporting it, and A2 and N1 with V100 as not. Use `--maintenance-policy=TERMINATE` where it is not supported. `a3-highgpu-1g`, `-2g` and `-4g` can only be created as Spot or Flex-start VMs.

## 2. Drivers
Option A — Google's installer for Linux VMs without Secure Boot (the script does not work on Linux VMs with Secure Boot; follow the "Install GPU drivers (Secure Boot VMs)" section of the install-drivers page there). If the Ops Agent (2.38.0 or later) is collecting GPU metrics, stop it first with `sudo systemctl stop google-cloud-ops-agent`. Tested on Debian 12/13, RHEL and Rocky 8/9/10, Ubuntu 22/24/26. (`--installation-mode=repo` default, uses DKMS so kernel updates rebuild the driver; `binary` mode holds kernel packages and is used automatically for `lts`; `--installation-branch` is `prod` default, `nfb` or `lts`):
```bash
curl -L https://storage.googleapis.com/compute-gpu-installation-us/installer/latest/cuda_installer.pyz -o cuda_installer.pyz
sudo python3 cuda_installer.pyz install_driver      # may restart the VM; rerun with the same parameters to continue
sudo python3 cuda_installer.pyz install_cuda        # optional toolkit
nvidia-smi
```
Option B — Deep Learning VM images (`--image-project=deeplearning-platform-release`, a
`common-cu*` family) for a ready CUDA stack.
Option C — bake drivers into a custom image so scale-out VMs boot ready.

## 3. Operate
- Capacity: when a zone has no GPUs, try other zones, reservations or Flex-start VMs.

## Gotchas
- Secure Boot VMs need the separate Secure Boot driver procedure; the installer script above is for VMs without it (Windows has its own script that supports Secure Boot).
- Patching tools that install explicit versioned kernel packages can bypass binary-mode kernel holds and break the driver after reboot; use `repo` mode or install matching kernel headers.

## Verify
- [ ] `nvidia-smi` lists the expected GPU count and driver version after a reboot.

## Checked
2026-10-31. Confirmed on the install-drivers-gpu, accelerator-optimized-machines and Deep Learning VM images pages: installer download URL and subcommands, `--installation-mode` repo (default) / binary and `--installation-branch` prod (default) / nfb / lts, DKMS rationale, patch-tool kernel-package caution, list of tested OSes, installer unsupported on Secure Boot Linux VMs, Ops Agent stop note, A2 machine types, A4/A3 Ultra families, `deeplearning-platform-release` project and `common-cu*` image names, live-migration support lines. Removed: `--shielded-secure-boot` in the installer example, machine-type and accelerator-type literals not on the fetched pages, the PyTorch check, and the signed-driver sentence. Commands checked with check_commands.py.
Method: documentation only; no commands were run.
