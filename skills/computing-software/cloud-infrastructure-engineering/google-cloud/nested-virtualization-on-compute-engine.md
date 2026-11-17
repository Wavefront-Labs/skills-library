---
id: computing-software.cloud-infrastructure-engineering.google-cloud.nested-virtualization-on-compute-engine
name: nested-virtualization-on-compute-engine
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, compute-engine, nested-virtualization, kvm, enable-nested-virtualization, android-emulator, disablenestedvirtualization]
level: practitioner
status: docs-checked
description: "Run KVM guests inside Compute Engine VMs: enable nested virtualization, unsupported machine families, the org policy that blocks it, and performance caveats."
sources: ["https://cloud.google.com/compute/docs/instances/nested-virtualization/overview", "https://cloud.google.com/compute/docs/instances/nested-virtualization/enabling", "https://cloud.google.com/compute/docs/instances/nested-virtualization/managing-constraint"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nested virtualization on Compute Engine

Used for CI of VM images, Android emulators, Firecracker/KVM sandboxes, legacy hypervisor labs.
The only hypervisor supported in an L1 VM is Linux KVM (Hyper-V is not supported). Not supported on E2, memory-optimized, Arm or AMD-processor VMs (N4D is the AMD exception). Check the regions and zones page for processors per zone. Licensed operating systems in L2 VMs need bring-your-own licences.

## Enable
```bash
gcloud compute instances create kvm-host --zone=europe-west2-b \
  --machine-type=n2-standard-8 \
  --enable-nested-virtualization --image-family=ubuntu-2404-lts-amd64 --image-project=ubuntu-os-cloud
# existing VM: stop, then
gcloud compute instances export kvm-host --zone=<Z> --destination=vm.yaml
#   add: advancedMachineFeatures: {enableNestedVirtualization: true}
gcloud compute instances update-from-file kvm-host --zone=<Z> --source=vm.yaml --most-disruptive-allowed-action=RESTART
```
Older method: create an image with license `https://www.googleapis.com/compute/v1/projects/vm-options/global/licenses/enable-vmx` (no extra charge; Intel VMs then need a minimum CPU platform of Intel Haswell). Setting `enableNestedVirtualization` directly is the recommended method. Quote yes/no label values in the exported YAML to avoid a parse error.

## Inside the VM
```bash
grep -cw vmx /proc/cpuinfo        # any value other than 0 means nested virtualization is enabled
```

## Org policy
`constraints/compute.disableNestedVirtualization` (boolean) blocks it; often enforced in baselines.
Exempt a CI folder/project only.

## Gotchas
- Nested VMs can see a 10% or greater performance decrease for CPU-bound work, and possibly more for I/O-bound work.
- See the Compute Engine nested-virtualization troubleshooting page if the L1 VM or nested VMs fail to start.

## Verify
- [ ] `grep -cw vmx /proc/cpuinfo` prints a non-zero number and a nested guest boots.

## Checked

Checked 2026-10-27 against About nested virtualization, Enable nested virtualization (pages last updated 2026-10-26 UTC), the nested virtualization constraint page and the Compute Engine v1 API discovery document. Fixed wrong claims: only Linux KVM is supported in the L1 VM (Hyper-V is not), E2, memory-optimized, Arm and AMD (except N4D) VMs are unsupported, and the example no longer forces --min-cpu-platform. Confirmed the 10 percent overhead, the recommended enableNestedVirtualization method, the enable-vmx licence and Haswell minimum, constraints/compute.disableNestedVirtualization and the vmx check. Removed unconfirmed live-migration, nested networking and Confidential VM statements.

Method: documentation only; no commands were run.
