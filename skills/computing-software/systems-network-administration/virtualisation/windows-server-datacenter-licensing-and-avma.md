---
id: computing-software.systems-network-administration.virtualisation.windows-server-datacenter-licensing-and-avma
name: windows-server-datacenter-licensing-and-avma
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [avma, windows-server-licensing, hyper-v, activation, licensing]
level: practitioner
status: docs-checked
description: "Activate and license Windows Server guests on Hyper-V: Datacenter versus Standard guest rights, and Automatic VM Activation (AVMA) setup, version matrix and checks."
sources:
  - https://learn.microsoft.com/en-us/windows-server/get-started/automatic-vm-activation
  - https://learn.microsoft.com/en-us/azure/azure-local/concepts/compare-windows-server
  - https://learn.microsoft.com/en-us/windows-server/get-started/editions-comparison
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Datacenter licensing and AVMA

**Goal:** compliant licensing for Windows guests and activation that works without a KMS in isolated environments.
This is not legal advice: confirm core minimums, stacking rules and licence mobility in Microsoft's current Product
Terms and licensing guide (not read for this review).

## Virtualisation rights
- **Datacenter**: unlimited Windows Server VMs on the licensed host.
- **Standard**: 2 VMs included per licensed host.
- Core counts, minimums, stacking more Standard licences and moving VMs between hosts are set by the licensing
  guide and Product Terms, not by the technical documentation: check them there before buying.
- In a failover cluster, every virtualisation host must be activated for guests to stay activated, regardless of
  which host runs them.

## Automatic VM Activation (AVMA)
AVMA activates Windows Server VMs on an activated Windows Server Hyper-V host, even when disconnected. It binds the
VM activation to the licensed virtualisation host and activates the VM when it starts.
- **Host**: Windows Server Datacenter edition with the Hyper-V role, activated. Azure Local also supports AVMA; with
  a Windows Server subscription it is enabled automatically on the hosts.
- **Guest**: a version the host can activate. A host activates its own version and older ones: for example a
  Windows Server 2025 host activates 2025, 2022, 2019, 2016 and 2012 R2 guests; a 2022 host activates 2022 down to
  2012 R2. All editions of an eligible version (Datacenter, Standard, Essentials) can be activated.
- The **Data Exchange** integration service (Key-Value Pair Exchange) must be enabled in the VM; it is on by default
  for new VMs.
- Install the generic AVMA client key for the guest's version and edition (the keys are published on the AVMA
  page):
```powershell
slmgr /ipk <AVMA_key>
```
The VM activates automatically while the host itself is activated. AVMA does not work with other virtualisation
technologies.

## Checks
- AVMA requests are logged in the host's Application log with Event ID 12310 and in the VM with Event ID 12309.
  VM-side notifications include AVMA Success, Invalid Host, Invalid Data and Activation Denied (AVMA ID mismatch).
- `Get-VMIntegrationService -VMName app01 -Name 'Key-Value Pair Exchange'` should show the service enabled.

## Gotchas
- KVP data is not secured and can be modified; remove it if you replace the AVMA key with a retail, OEM or volume
  key.
- AVMA only activates; it does not license anything. Compliance still rests on your licence agreement.
- Because activation is transparent, no error messages appear in the guest: use the events above.

## Checked

Date checked: 2026-10-27. Documentation: "Automatic Virtual Machine Activation in Windows Server" (ms.date 2025-07-14), editions comparison, Azure Local comparison and VM activation pages.
Confirmed: Datacenter host requirement and host-to-guest version matrix; Data Exchange service requirement and default; slmgr /ipk procedure; events 12309 and 12310; KVP caveat; cluster host activation note; Azure Local AVMA support; Datacenter unlimited and Standard 2 VMs per the Azure Local comparison. Core minimums, stacking and mobility rules are deferred to Microsoft's licensing terms.

Method: documentation only; no commands were run.
