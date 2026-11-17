---
id: computing-software.systems-network-administration.linux.vfio-pci-gpu-passthrough
name: vfio-pci-gpu-passthrough
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, vfio, vfio-pci, pci-passthrough, gpu-passthrough, iommu, intel-iommu, amd-iommu, iommu-groups, kvm, libvirt, hostdev, sysadmin]
level: advanced
status: docs-checked
description: "Pass a PCI device (GPU, NIC, HBA) through to a KVM guest with VFIO: enabling the IOMMU, checking groups, binding vfio-pci early, libvirt hostdev config, and common reset/ROM failures."
sources:
  - https://docs.kernel.org/driver-api/vfio.html
  - https://docs.kernel.org/admin-guide/kernel-parameters.html
  - https://docs.kernel.org/PCI/pci-iov-howto.html
  - https://libvirt.org/formatdomain.html#host-device-assignment
  - https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/configuring_and_managing_virtualization/managing-virtual-devices_configuring-and-managing-virtualization
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VFIO PCI / GPU passthrough

**Goal:** give a VM exclusive, near-native access to a physical PCI device, with the host
never touching it.

## 1. IOMMU on
- Firmware: enable VT-d (Intel) / AMD-Vi (IOMMU); check the board manual for any large-BAR ("Above 4G decoding") setting.
- Kernel cmdline: Intel `intel_iommu=on`; `iommu=pt` is documented as equivalent to `iommu.passthrough=1`. For AMD see the `amd_iommu=` entry in the kernel parameters list.
```bash
# add the arguments to the kernel command line with your distribution's bootloader tooling
reboot
dmesg | grep -Ei 'DMAR|IOMMU|AMD-Vi' | head   # look for lines showing the IOMMU initialised
```

## 2. IOMMU groups
Every device in a group must go to the same VM (or be a PCI bridge).
```bash
for g in /sys/kernel/iommu_groups/*; do echo "group ${g##*/}:"; for d in $g/devices/*; do echo "  $(lspci -nns ${d##*/})"; done; done
```
A GPU and its audio function usually share a group, so pass both. The kernel VFIO documentation explains that
devices behind a bridge without ACS support end up in one group; if the GPU is grouped with unrelated devices, try a different slot.

## 3. Bind vfio-pci before the host driver grabs it
```bash
lspci -nn | grep -i nvidia        # e.g. 10de:2684 (VGA) and 10de:22ba (audio)
echo 'options vfio-pci ids=10de:2684,10de:22ba' > /etc/modprobe.d/vfio.conf
echo 'softdep nvidia pre: vfio-pci' >> /etc/modprobe.d/vfio.conf     # also for nouveau/amdgpu as relevant
dracut -f --add-drivers "vfio vfio_iommu_type1 vfio_pci"              # Debian: add to /etc/initramfs-tools/modules; update-initramfs -u
reboot
lspci -nnk -s 01:00.0             # "Kernel driver in use: vfio-pci"
```
Alternatively the kernel argument `vfio-pci.ids=10de:2684,10de:22ba` (`ids` is a vfio-pci module parameter taking comma-separated `vendor:device` entries). Don't do this for the GPU driving the host console.

## 4. Attach in libvirt
```xml
<hostdev mode='subsystem' type='pci' managed='yes'>
  <source><address domain='0x0000' bus='0x01' slot='0x00' function='0x0'/></source>
</hostdev>
```
or `virt-install ... --host-device 01:00.0 --host-device 01:00.1`, or `virsh attach-device vm hostdev.xml --config`.
With `managed='yes'` libvirt detaches the device from its host driver at guest start and reattaches it afterwards; with `managed='no'` you must bind it to vfio-pci yourself.

## Gotchas
- Device fails after the first VM reboot: the device may lack a working reset; a host reboot is the fallback.
- Some guest drivers refuse to run under a hypervisor: libvirt offers `<kvm><hidden state='on'/></kvm>` to hide it.
- Memory: with an assigned device the VFIO IOMMU driver pins guest memory for DMA, so guest RAM cannot be overcommitted.
- NICs: prefer SR-IOV VFs (`echo 8 > /sys/class/net/eno1/device/sriov_numvfs`) over passing the whole NIC.

## Verify
- [ ] Host: `lspci -nnk` shows `vfio-pci` in use for every function in the group.
- [ ] Guest: device visible (`lspci` / Device Manager) with its native driver loaded and working under load; survives a guest reboot.

## Checked

Checked 2026-10-27 against Linux kernel docs (driver-api/vfio, kernel-parameters, PCI SR-IOV howto) and the vfio_pci.c source, libvirt virsh and formatdomain docs, kmod modprobe.d(5), dracut man page, virt-install man page (all current master, 2026-10-27). Confirmed: intel_iommu=on and iommu=pt kernel parameters, the vfio-pci ids module parameter, softdep syntax in modprobe.d, dracut -f and --add-drivers, hostdev managed attribute, virt-install --host-device, virsh attach-device --config, kvm hidden element, sriov_numvfs sysfs file. Removed or softened: AMD default-on claim, grubby command, dmesg message strings, ACS override patch, q35/OVMF requirement, vendor-reset, live-migration claim, hugepage advice.

Method: documentation only; no commands were run.
