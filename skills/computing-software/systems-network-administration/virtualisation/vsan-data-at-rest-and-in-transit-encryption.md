---
id: computing-software.systems-network-administration.virtualisation.vsan-data-at-rest-and-in-transit-encryption
name: vsan-data-at-rest-and-in-transit-encryption
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [vsan-encryption, data-at-rest-encryption, data-in-transit-encryption, kms, vsan, vmware, vsphere]
level: advanced
status: draft
description: "Enable vSAN data-at-rest encryption with a KMS or native key provider and data-in-transit encryption, rekey shallow or deep, and avoid locking yourself out."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html
  - https://core.vmware.com/resource/vsan-encryption-services
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vSAN encryption (at rest and in transit)

**Goal:** encrypted vSAN capacity and inter-host traffic with keys you can recover.

## Key provider first
vCenter -> Configure -> Security -> Key Providers:
- **Standard key provider** (external KMIP KMS: HyTrust/Entrust, Thales, etc.). Establish trust (certificates) from vCenter to the KMS cluster.
- **Native Key Provider (NKP)**: built into vCenter 7.0U2+. Back it up immediately (Back up -> password-protected .p12). Without that backup, losing vCenter can mean losing the data.
- Hosts with TPM 2.0 persist keys so they can boot and unlock without vCenter.

## Data-at-rest
Cluster -> Configure -> vSAN -> Services -> Data services -> Edit -> Data-at-rest encryption on, choose provider, optional *wipe residual data*.
- **OSA**: enabling reformats each disk group (rolling, like dedup). Allow time and free capacity.
- **ESA**: must be chosen when the cluster is created; cannot be turned on later.

## Data-in-transit (7.0U1+)
Same panel, *Data-in-transit encryption*, rekey interval (default 1 day). Uses AES-GCM between hosts, keys negotiated by hosts (no KMS needed). Small CPU cost.

## Rekey
- **Shallow rekey**: new KEK, fast, no data rewrite.
- **Deep rekey** (OSA): new DEKs, rewrites all data; schedule like a reformat.

## Gotchas
- KMS unreachable when a host reboots and no TPM: disk groups stay locked until KMS returns. Keep the KMS cluster outside the vSAN cluster it protects.
- Core dumps of encrypted hosts are encrypted; set a password for vm-support bundles.
- vSAN encryption is separate from VM encryption; using both double-encrypts and kills dedup.

## Verify
vSAN health: *Encryption* checks green (KMS connectivity, host key status); `esxcli vsan encryption info get` shows enabled; NKP backup stored offline.
