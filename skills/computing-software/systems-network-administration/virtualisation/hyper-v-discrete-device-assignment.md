---
id: computing-software.systems-network-administration.virtualisation.hyper-v-discrete-device-assignment
name: hyper-v-discrete-device-assignment
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, discrete-device-assignment, dda, gpu-passthrough, pcie-passthrough, mmio, add-vmassignabledevice, windows-server]
level: advanced
status: docs-checked
description: "Pass a PCIe device (GPU, NVMe) straight to a Hyper-V VM with Discrete Device Assignment: survey, dismount from host, MMIO sizing, assignment and safe return to the host."
sources:
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/deploy/deploying-graphics-devices-using-dda
  - https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/plan/plan-for-deploying-devices-using-discrete-device-assignment
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Discrete Device Assignment (DDA)

**Goal:** give a VM exclusive, near-native access to a PCIe device.

## Check the device can be assigned
Run Microsoft's `SurveyDDA.ps1` machine profile script (from the MicrosoftDocs Virtualization-Documentation repository); it reports whether each device can be assigned, its location path, and the MMIO space it needs.

## Prepare the VM
```powershell
Set-VM -Name gpu01 -AutomaticStopAction TurnOff
Set-VM -Name gpu01 -GuestControlledCacheTypes $true -LowMemoryMappedIoSpace 3GB -HighMemoryMappedIoSpace 33280MB
```
Defaults are 128 MB low and 512 MB high MMIO space per VM. Set them to the SurveyDDA figure for each device plus a buffer; the values above are reasonable for a single GPU, and the guest reports a resources error if they are too small.

## Move the device from host to VM
```powershell
$dev = Get-PnpDevice -FriendlyName '*NVIDIA*' -Class Display
$loc = ($dev | Get-PnpDeviceProperty DEVPKEY_Device_LocationPaths).Data[0]
Disable-PnpDevice -InstanceId $dev.InstanceId -Confirm:$false
Dismount-VMHostAssignableDevice -LocationPath $loc -Force   # -Force bypasses the warning when the vendor supplies no partitioning driver
Add-VMAssignableDevice -LocationPath $loc -VMName gpu01
Start-VM gpu01      # install the vendor driver inside the guest
```

## Return to the host
```powershell
Stop-VM gpu01
Remove-VMAssignableDevice -LocationPath $loc -VMName gpu01
Mount-VMHostAssignableDevice -LocationPath $loc
```
Then re-enable the device in Device Manager.

## Limits
- While a device is attached the VM cannot use save/restore, live migration or dynamic memory, and cannot join a high-availability cluster.
- Microsoft supports two device classes: graphics adapters and NVMe storage; other devices may work and need a hardware vendor statement of support.

## Verify
`Get-VMAssignableDevice -VMName gpu01` lists the location path, and the guest Device Manager shows the device without errors.

## Checked
Checked 2026-10-25 against Microsoft Learn Hyper-V documentation (MicrosoftDocs/windowsserverdocs, latest commit 2026-10-23) and the Windows Server 2025 PowerShell reference (MicrosoftDocs/windows-powershell-docs, latest commit 2026-10-23). Confirmed: the DDA command sequence (Set-VM AutomaticStopAction, GuestControlledCacheTypes, LowMemoryMappedIoSpace 3Gb, HighMemoryMappedIoSpace 33280Mb, Dismount-VMHostAssignableDevice, Add/Remove-VMAssignableDevice, Mount-VMHostAssignableDevice), default MMIO sizes, SurveyDDA, restricted features, and the supported device classes. Removed because no documentation page confirmed them: the checkpoint restriction, the consumer-GPU remark, the PCI error code 12 reference, and the Enable-PnpDevice step.
Method: documentation only; no commands were run.
