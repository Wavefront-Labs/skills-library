---
id: computing-software.systems-network-administration.virtualisation.vcenter-enhanced-linked-mode
name: vcenter-enhanced-linked-mode
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [enhanced-linked-mode, elm, vcenter-sso, sso-domain, vcenter-repoint, vdt, vmware, vcenter, vsphere, cmsso-util, sso-domain-repoint]
level: advanced
status: docs-checked
description: "Join vCenters in Enhanced Linked Mode: shared SSO domain limits, backup and restore consistency, replication health checks, repoint and unlink procedures."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vcenter-installation-and-setup/introduction-to-vsphere-installation-and-setup/creating-vcenter-server-linked-mode-groups.html
  - https://knowledge.broadcom.com/external/article?legacyId=2127057
  - https://knowledge.broadcom.com/external/article/450887/repointing-vcenter-server-to-a-new-sso.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# vCenter Enhanced Linked Mode (ELM)

**Goal:** several vCenters viewed and administered as one inventory with shared roles,
licences and tags, without creating an SSO domain that is impossible to restore.

## What ELM shares
SSO domain, roles/permissions, tags and categories, licences and global search. Each
vCenter keeps its own inventory and database. Limits (vSphere 8): up to 15 vCenters in
one SSO domain. Linking is decided at deployment (join an existing SSO domain in stage 2)
or later with `cmsso-util domain-repoint`.

## When not to link
- Separate security zones (DMZ, PCI) should not share an SSO domain: one admin
  compromise reaches all.
- A failure in the shared VMDir replication can block logins on all linked vCenters.
- Restore is harder: restoring one node to an older point can create replication
  conflicts; the whole domain should be backed up together.

## Health checks
```sh
# on each VCSA (shell)
/usr/lib/vmware-vmdir/bin/vdcrepadmin -f showpartners -h localhost -u administrator -w '<pw>'
/usr/lib/vmware-vmdir/bin/vdcrepadmin -f showpartnerstatus -h localhost -u administrator -w '<pw>'
```
Partner status should show the partner has seen your last change number within a few
minutes of a change (zero replication lag).

## Repoint / unlink
```sh
# repoint the first node
cmsso-util domain-repoint -m execute --src-emb-admin administrator --dest-domain-name <domain>
# subsequent ELM nodes: pre-check, then execute, naming an already-repointed partner
cmsso-util domain-repoint -m pre-check --src-emb-admin administrator --replication-partner-fqdn <partner> --replication-partner-admin administrator --dest-domain-name <domain>
cmsso-util domain-repoint -m execute --src-emb-admin administrator --replication-partner-fqdn <partner> --replication-partner-admin administrator --dest-domain-name <domain>
```
Take offline (powered-off) snapshots of **all** linked vCenters at the same time before
repoint or unregister. Snapshots of ELM nodes taken at different times are not a valid
rollback.

## Backup rules
File-based backups of every node on the same schedule; after restoring one node, the
restore workflow resyncs from partners. Never restore all nodes from different points.

## Verify
Log in to one vCenter and see all linked inventories; `showpartnerstatus` shows the
partner has seen your last change number.

## Checked
2026-10-31: Confirmed the 15-vCenter ELM limit and deployment/repoint options against
the vCenter Installation and Setup "Creating vCenter Server Linked Mode Groups" page;
vdcrepadmin location, showpartners/showpartnerstatus and the change-number output against
Broadcom KB 316504 (legacyId 2127057); the cmsso-util domain-repoint pre-check/execute
syntax and the simultaneous powered-off snapshot rule for ELM nodes against Broadcom KB
450887. Removed the unconfirmed VDT tool claim and the unregister flag line.
Method: documentation only; no commands were run.
