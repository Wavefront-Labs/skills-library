---
id: computing-software.systems-network-administration.active-directory.virtual-dc-generation-id-safeguards
name: virtual-dc-generation-id-safeguards
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, virtualized-domain-controller, vm-generation-id, dc-snapshot-safety, invocationid, rid-pool, usn-rollback, checkpoints, hyper-v, vmware, snapshot-restore]
level: advanced
status: docs-checked
description: "How VM-GenerationID protects virtual DCs from snapshot rollback, what it does and does not save you from, and safe checkpoint/backup practice."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/virtual-dc/virtualized-domain-controller-architecture
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/virtual-dc/virtualized-domain-controllers-hyper-v
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/virtual-dc/support-for-using-hyper-v-replica-for-virtualized-domain-controllers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Virtual DCs: VM-GenerationID safeguards

**Goal:** know why reverting a virtual DC no longer guarantees USN rollback, and where that
protection ends.

## What VM-GenerationID does
A hypervisor that supports VM-GenerationID exposes a generation ID that changes when the
VM's position in time changes (for example a snapshot is applied or the VM is copied). A
Windows Server 2012+ DC stores the last value it saw in `msDS-GenerationId` on its own
computer object (in its database). It compares the value with the one from the VM driver
at boot and before writes. On mismatch it:
- resets its **invocationID** (so partners treat its changes as new, avoiding USN reuse),
- discards its current **RID pool** (avoids duplicate security principals),
- sets an initial synchronization requirement before it will assume an operations master role,
- logs event **2170** (a generation ID change has been detected).

Whether your hypervisor supports VM-GenerationID is a question for the hypervisor vendor's
documentation; Microsoft's guidance says to confirm it before relying on the safeguards.

## What it does not do
- It does not make snapshots a backup strategy. Changes made after the snapshot that had not
  replicated are lost.
- Copying the disk files manually to a "new VM" without the hypervisor changing the ID
  bypasses it.
- Hypervisors that do not expose the ID give you no protection: treat a revert as a
  USN-rollback event.
- Restoring **all** DCs of a domain from snapshots is a forest recovery, not a safeguard case.

## Practice
- Microsoft's guidance for virtual DCs: do not take or use snapshots of virtual DCs, do not
  copy or clone VHDs by hand, do not use Export on a VM running a DC, and back up with a
  supported Active Directory-compatible method (system state) instead.
- After any revert/restore, confirm event 2170 appeared in the Directory Service log and
  that replication resumed.

## Verify
- [ ] The hypervisor documents VM-GenerationID support for every host that runs a virtual DC.
- [ ] Backups of DCs are Active Directory-compatible system-state backups.

## Checked

Documentation: Microsoft Learn virtualized DC architecture, Hyper-V replica support and
virtualized-DC-on-Hyper-V pages, from MicrosoftDocs/windowsserverdocs and MicrosoftDocs/windows-powershell-docs, main branch (latest commits 2026-10-23).
Confirmed: msDS-GenerationId stored on the DC computer object, invocationID reset, RID pool
discarded, initial synchronization requirement before assuming an operations master role,
event 2170 (Directory Service), and the "no snapshots, no VHD copies, no Export" guidance.
Removed unconfirmed claims: named hypervisor versions, the Device Manager device check,
SYSVOL marking on a safeguard trigger, the tombstone-lifetime pause rule and Hyper-V production
checkpoints advice.

Method: documentation only; no commands were run.
