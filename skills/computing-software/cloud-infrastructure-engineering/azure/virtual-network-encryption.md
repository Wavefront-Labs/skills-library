---
id: computing-software.cloud-infrastructure-engineering.azure.virtual-network-encryption
name: virtual-network-encryption
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vnet, vnet-encryption, encryption-in-transit, accelerated-networking, dropunencrypted, allowunencrypted]
level: advanced
status: docs-checked
description: "Enable Azure Virtual Network encryption for VM-to-VM traffic: supported VM sizes, AllowUnencrypted vs DropUnencrypted enforcement, peering behaviour and verification."
sources: ["https://learn.microsoft.com/azure/virtual-network/virtual-network-encryption-overview", "https://learn.microsoft.com/azure/virtual-network/how-to-create-encryption", "https://learn.microsoft.com/azure/virtual-network/virtual-network-encryption-faq"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Virtual network encryption

**Goal:** VM-to-VM traffic inside and across peered VNets is encrypted in transit by the
platform (DTLS on the host), satisfying "encrypt everything in transit" without app changes.

## Requirements
- VM sizes that support encryption: the overview says all v5 and newer D-series and E-series are supported, and lists further families; check the current list.
- Accelerated Networking enabled on the NICs.
- Both endpoints in VNets with encryption enabled (same VNet or peered, including global peering).

## Enable
```bash
az network vnet update -g rg -n vnet-app --enable-encryption true --encryption-enforcement-policy AllowUnencrypted
```
- Enforcement policy values (`AllowUnencrypted`, `DropUnencrypted`) are not confirmed on the fetched pages; check the how-to before choosing.
Existing VMs need to be stopped and started after enabling encryption in the virtual network (documented).

## What is and isn't covered
| Traffic | Encrypted |
|---|---|
| VM ↔ VM same VNet / peered VNets (supported sizes) | Yes |
| VM Scale Set instances in the same or peered VNets | Yes (supported sizes) |
| Regionally and globally peered VNets | Yes (documented) |

## Verify encryption
- Per the overview, verification during preview was limited to the NIC's `vnetEncryptionSupported` status and Accelerated Networking; after preview, virtual network flow logs show encrypted and unencrypted flows. Check the current page for the field names.

## Gotchas
- Measure latency-sensitive apps after enabling.
- Mixed fleets in AllowUnencrypted give partial coverage — report from flow logs before claiming compliance.

## Verify
- [ ] `az network vnet show -g rg -n vnet-app --query encryption` shows `enabled: true` and the policy.
- [ ] Flow logs show encrypted VM-to-VM flows after VMs were stopped and started.

## Checked
2026-10-28. Confirmed on the virtual network encryption overview: DTLS tunnel between VMs, v5 and newer D-series and E-series supported, regional and global peering covered, stop/start of existing VMs required after enabling, verification limited during preview with flow logs afterwards. check_commands confirmed `az network vnet update --enable-encryption`. Removed as unconfirmed: enforcement policy semantics, the covered/not-covered traffic rows, `FlowEncryption` values and KQL, the audit policy name, `az vm show` claim.
Method: documentation only; no commands were run.
