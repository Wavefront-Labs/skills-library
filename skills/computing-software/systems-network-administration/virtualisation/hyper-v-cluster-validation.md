---
id: computing-software.systems-network-administration.virtualisation.hyper-v-cluster-validation
name: hyper-v-cluster-validation
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [hyper-v, test-cluster, cluster-validation, failover-clustering, validation-report, windows-server]
level: practitioner
status: docs-checked
description: "Run failover cluster validation (Test-Cluster) for Hyper-V clusters safely, including on live clusters without taking CSVs offline, and read the validation report."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/failoverclusters/test-cluster
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/high-availability/validate-hardware-failover-cluster
  - https://learn.microsoft.com/en-us/windows-server/storage/storage-spaces/deploy-storage-spaces-direct
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Failover cluster validation

**Goal:** prove a cluster configuration is supportable before creation and after any change (new node, driver, firmware, storage).

## Before creating the cluster
```powershell
Test-Cluster -Node hv01, hv02, hv03 -Include 'Inventory','Network','Storage','System Configuration','Hyper-V Configuration'
Test-Cluster -List        # lists the test and category names
```
Microsoft supports a cluster solution only if the complete configuration passes validation (warnings can be acceptable). Hyper-V configuration tests are only needed if you use or plan clustered VMs. For Storage Spaces Direct the deployment guide adds the `Storage Spaces Direct` category: `-Include "Storage Spaces Direct","Inventory","Network","System Configuration"`.

## On a running cluster
Storage tests can take disks offline. Either skip storage or name the disks:
```powershell
Test-Cluster -Cluster hvclu01 -Ignore 'Storage'
Test-Cluster -Cluster hvclu01 -Include 'Storage' -Disk 3 -Force      # -Force takes an online clustered disk offline for the tests
```
`-Disk` takes disk numbers (or signatures); an online disk that belongs to a clustered role or CSV needs `-Force`. Plan this for a maintenance window.

## Reading the report
Validation writes an HTML report under the Cluster\Reports folder of the system root (`%SystemRoot%\Cluster\Reports`). Passed tests are supported, a warning means supportable but short of best practice, and a failed test means that aspect is not supported until fixed.

## Gotchas
- Re-run validation after changing firmware, drivers or hardware, and after restoring a node from backup; a restored system is not considered supported until validation completes.
- Keep the report if you need Microsoft support.

## Verify
Report summary shows all categories passed or justified warnings, with no failed tests.

## Checked
2026-10-26, Windows Server 2025 documentation (MicrosoftDocs windowsserverdocs and windows-powershell-docs, current as of 2026-10-23). Confirmed: Test-Cluster -Node/-Include/-Ignore/-List/-Disk/-Force syntax and the test categories (Hyper-V configuration, Inventory, Network, Storage, System configuration) in the validation article; the Storage Spaces Direct validation command in the S2D deployment page; the report location under the Cluster\Reports folder; Microsoft supports a cluster only if the whole configuration passes validation. Corrected: -Disk takes disk numbers or signatures (not a CSV object) and an online disk also needs -Force, which takes it offline. Removed as unconfirmed: the report reading priorities, the run-as notes and the software update level remark.

Method: documentation only; no commands were run.
