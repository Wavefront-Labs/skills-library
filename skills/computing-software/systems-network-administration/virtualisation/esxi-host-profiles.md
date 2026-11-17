---
id: computing-software.systems-network-administration.virtualisation.esxi-host-profiles
name: esxi-host-profiles
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [host-profiles, host-profile, esxi-host-setup, compliance, configuration-drift, host-customization, vmware, esxi, vsphere, vcenter]
level: practitioner
status: draft
description: "Extract, edit, attach and remediate vSphere host profiles: per-host customisations, compliance checks, what to disable in the profile and common remediation failures."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/host-profiles-8-0.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ESXi host profiles

**Goal:** every host in a cluster has identical networking, storage, NTP, syslog and
security settings, and drift shows up as a compliance failure instead of an outage.

## Workflow
1. Configure one **reference host** fully and test it.
2. **Extract** a profile: Policies and Profiles → Host Profiles → Extract (or
   `New-VMHostProfile -ReferenceHost <host> -Name <name>`).
3. **Edit** the profile: untick sub-profiles you do not want enforced. Commonly disabled:
   storage device-specific settings (device NAA IDs, PSA claim rules for local disks),
   iSCSI IQNs, and anything vSAN or hardware-vendor specific that differs per host.
4. **Attach** to the cluster (not to individual hosts) so new hosts inherit it.
5. **Host customisations:** per-host values (vmk IPs, hostname, iSCSI IQN). Export the
   customisation CSV, fill it, import it back.
6. **Check compliance**, then **Remediate** (host into maintenance mode; some changes
   need a reboot, flagged in the pre-check).

```powershell
$hp = Get-VMHostProfile -Name <name>
Test-VMHostProfileCompliance -VMHost (Get-Cluster <cl> | Get-VMHost)
Invoke-VMHostProfile -Entity <host> -Profile $hp -ApplyOnly   # after maintenance mode
```

## Failure modes
- **Every host non-compliant on storage:** the reference host's local disk or LUN IDs
  were captured. Disable those sub-profiles or mark settings "user specified".
- **Remediation hangs on network:** the profile moves vmk0 to a vDS port group that does
  not exist yet; create the vDS and add the host before remediating.
- **Password in profile:** the root password policy can push a password; avoid unless
  intended, and rotate via a secure process instead.
- **Profile stale after upgrade:** re-extract from an upgraded reference host or use
  "Copy settings from host" so new options exist.

## Verify
Cluster → Monitor → Host Profiles shows all hosts Compliant; schedule a weekly compliance
check task and alarm on non-compliance.
