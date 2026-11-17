---
id: computing-software.systems-network-administration.windows-server.cluster-name-object-and-vco-permissions
name: cluster-name-object-and-vco-permissions
category: computing-software
field: systems-network-administration
product: windows-server
tags: [failover-clustering, cluster-name-object, vco, active-directory, prestaged-computer-objects]
level: advanced
status: docs-checked
description: "Manage cluster AD objects: CNO creation rights, prestaging CNO and VCOs in locked-down OUs, fixing event 1194 and the Reset password permission."
sources:
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/prestage-cluster-adds
  - https://learn.microsoft.com/en-us/windows-server/failover-clustering/failover-cluster-accounts-overview
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Cluster Name Object and VCO permissions

The cluster creates a **CNO** (cluster name computer object) and, for each clustered role with a network name, a
**VCO** (virtual computer object). The CNO creates VCOs using its own rights.

## Default behaviour
`New-Cluster` creates the CNO using the creator's rights, which need Create Computer objects on the OU or container where
the cluster servers reside. The cluster name account goes in the default computer container (Computers unless
redirected). Clustered roles with a client access point get a VCO in the same OU as the CNO, so the CNO needs Create
Computer objects there.

## Prestage in a locked-down OU
1. Create the CNO computer object (e.g. `SQLCL01`), then **disable** it (the cluster enables it).
2. Grant the user running New-Cluster Full Control on it.
3. Grant the CNO **Create Computer objects** on the OU, or prestage each VCO (Account Operators membership is the
   documented minimum for prestaging a VCO):
   - Create the VCO object with the role's network name and give the CNO Full Control on it.
```powershell
New-Cluster -Name SQLCL01 -Node N1,N2 -StaticAddress 10.0.5.50 -AdministrativeAccessPoint ActiveDirectoryAndDns
```

## Event 1194 / role fails to come online
"Cluster network name resource failed to create its associated computer object in domain": the CNO lacks rights or
the domain-wide computer-account quota (default 10) is reached. Event IDs 1193, 1194, 1206 and 1207 point to this class of
problem. Fix the OU permissions or quota, then bring the resource online. In the default Computers container a cluster
administrator can create up to 10 VCOs without extra configuration.

## Repair
- Give cluster administrators the **Reset password** permission on the cluster name account, so they can reset its password.
- Protect CNO/VCOs from accidental deletion (Object tab in Active Directory Users and Computers) and document them.

## Verify
- [ ] Role network names online; CNO and VCOs enabled and protected from accidental deletion.

## Checked

Confirmed 2026-10-25 against the Windows Server docs (prestage-cluster-adds and failover-cluster-accounts-overview, repository last commit 2026-10-23): disabling the prestaged CNO, Full Control for the creating user, Create Computer objects for the CNO, the default quota of 10, events 1193/1194/1206/1207, the Reset password permission and the accidental-deletion protection. Removed the unconfirmed Recycle Bin and Repair procedure, Read All Properties and ObjectGUID check.

Method: documentation only; no commands were run.
