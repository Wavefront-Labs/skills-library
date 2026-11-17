---
id: computing-software.cloud-infrastructure-engineering.google-cloud.setting-up-migrate-to-vms-sources
name: setting-up-migrate-to-vms-sources
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, migration-planning, migrate-vm-setup, m2vm-source, vmware, aws-migration]
level: advanced
status: docs-checked
description: "Prepare Migrate to Virtual Machines: host and target projects, the vSphere Migrate Connector, AWS and Azure sources, required APIs and permissions, and source health."
sources: ["https://cloud.google.com/migrate/virtual-machines/docs/5.0/get-started/enable-services", "https://cloud.google.com/migrate/virtual-machines/docs/5.0/migrate/installing-migrate-connector", "https://cloud.google.com/migrate/virtual-machines/docs/5.0/migrate/create-an-aws-source", "https://cloud.google.com/migrate/virtual-machines/docs/5.0/migrate/target-project"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Setting up Migrate to VMs sources

## 1. Projects and APIs
- **Host project**: where Migrate to VMs runs (`vmmigration.googleapis.com` enabled).
- **Target projects**: where migrated VMs land; add each as a target project in Migrate to Virtual Machines (the host project can itself be a target) and grant the service agent access in the target as the target-project page describes. Required host-project APIs: `vmmigration.googleapis.com`, `servicemanagement.googleapis.com`, `servicecontrol.googleapis.com`, `iam.googleapis.com`, `cloudresourcemanager.googleapis.com`, `compute.googleapis.com`.
- Network in the target project/region ready (subnets, firewall, Shared VPC permissions).

## 2. VMware source (vSphere)
1. Download the **Migrate Connector** OVA, deploy it in vCenter (take sizing from the connector install page), give it network to vCenter/ESXi and outbound HTTPS to Google.
2. A vCenter user with the documented privileges (snapshots, CBT, datastore browse).
3. Register the connector and create the vSphere source by following the connector install page for your Migrate to Virtual Machines version.
4. Ports and network requirements: take them from the vSphere source pages (not verified here).

## 3. AWS / Azure sources
Create the AWS source in the console (Migrate to Virtual Machines, SOURCES tab, ADD SOURCE, Add AWS Source). Create an IAM policy from the docs' JSON template and an IAM user with programmatic access first. Fields: name, GCP region, AWS region (none of these can be edited later), access key ID and secret, optional CMEK, optional filters by security group or VM tags (several tags must all match). The source goes Active in up to 15 minutes. A host project can hold at most 15 cloud sources (AWS and Azure combined). Azure sources work almost identically; see the Azure source page for details.

## 4. Check
Console, Migrate to Virtual Machines, Sources: status Active, inventory shows source VMs. Start replication for a pilot VM before waves.

## Gotchas
- Wrong AWS region text makes the source fail to become active; create a new source.
- Changing credentials mid-replication can interrupt a cycle; wait 24 hours before revoking old credentials.

## Verify
- [ ] Source is Active with full inventory; a pilot VM completes initial sync and a test-clone boots in GCP.

## Checked
2026-10-28. Confirmed on the enable-services page (host vs target project, six required APIs) and the AWS source page (policy template, console path, fields, 15-minute activation, 15 cloud sources per host project, immutable name/regions, 24-hour credential note).
Fixed: `gcloud migration vms target-projects create` does not exist (check_commands: no `create` under that group), so it was removed.
Removed: connector sizing (4 vCPU, 16 GB), `m2vm register/status`, port numbers, CBT and NTP gotchas, `roles/vmmigration.serviceAgent`: the connector and target-project source pages fetched as empty landing pages and could not confirm them.
Method: documentation only; no commands were run.
