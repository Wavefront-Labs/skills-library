---
id: computing-software.cloud-infrastructure-engineering.google-cloud.sole-tenant-nodes-and-licensing
name: sole-tenant-nodes-and-licensing
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, sole-tenant-nodes, sole-tenant, bring-your-own-license, byol, node-groups, node-templates, node-affinity, host-maintenance, cpu-overcommit, windows-server-byol, sql-server-licensing, dedicated-hosts, license-compliance, in-place-restart]
level: advanced
status: docs-checked
description: "Run licence-bound or isolated workloads on sole-tenant nodes: node templates and groups, affinity labels, maintenance policies, CPU overcommit, and BYOL image import and tracking."
sources: ["https://docs.cloud.google.com/compute/docs/nodes/sole-tenant-nodes", "https://docs.cloud.google.com/compute/docs/nodes/provisioning-sole-tenant-vms", "https://docs.cloud.google.com/compute/docs/nodes/bringing-your-own-licenses", "https://docs.cloud.google.com/compute/docs/nodes/overcommitting-cpus-sole-tenant-vms", "https://docs.cloud.google.com/compute/docs/nodes/manually-live-migrate", "https://docs.cloud.google.com/sdk/gcloud/reference/compute/sole-tenancy/node-groups/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sole-tenant nodes and licensing

**Goal:** physical-host isolation (compliance, noisy-neighbour, or per-core/per-socket licences)
with maintenance handled the way the licence terms require.

## 1. When you need it
- **BYOL** for software licensed per physical core or processor with a dedicated-hardware requirement: bring your own media and run it on compliant hardware such as sole-tenant nodes. Per-user or per-device licences do not need server limits. BYOS Linux (RHEL, SLES) and Microsoft applications under License Mobility (for example SQL Server) do not require sole-tenant nodes.
- Physical isolation from other projects for security or compliance (workloads may still be shared inside your organisation if you share the group).
- Grouping VMs on the same host hardware.
Otherwise it costs more: a sole-tenant node bills the whole host plus a sole-tenancy premium whether you fill it or not (see the pricing page for rates).

## 2. Create
```bash
gcloud compute sole-tenancy node-templates create n2-tpl --region=europe-west1 \
  --node-type=n2-node-80-640 --node-affinity-labels=workload=sqlserver \
  --cpu-overcommit-type=enabled          # optional, only N1, N2, N2D, N4 nodes
gcloud compute sole-tenancy node-groups create sql-nodes --zone=europe-west1-b \
  --node-template=n2-tpl --target-size=2 \
  --maintenance-policy=restart-in-place  # default | restart-in-place | migrate-within-node-group
gcloud compute instances create sql-1 --zone=europe-west1-b --machine-type=n2-standard-16 \
  --node-group=sql-nodes   # or --node-affinity-file for label-based placement
```
- Affinity labels exist only on the node template; you cannot add them to a group later. `--node-affinity-file` takes a list of `key`, `operator` (`IN`/`NOT_IN`) and `values`, so instance templates can target labelled nodes.
- `NOT_IN` (anti-affinity) keeps VMs off chosen nodes, for example two replicas on different hosts.
- Autoscaling: `--autoscaler-mode` with `--min-nodes`/`--max-nodes` (maximum 100) on `node-groups create`; see the sole-tenant-node-group-autoscaling skill.

## 3. Maintenance policy = licence policy
| Policy | Behaviour | Licence fit (per Google docs) |
|---|---|---|
| `default` | live-migrate to a new physical server | per-user or per-device licences; general workloads |
| `restart-in-place` | VMs stopped, then restarted on the same physical server; the VM's on-host-maintenance must be `TERMINATE`; roughly an hour of downtime | per physical core/processor licences, fault-tolerant workloads |
| `migrate-within-node-group` | live-migrate within a fixed group of physical servers, using reserved holdback nodes | high-availability workloads with per-core/processor licences |
- Host events occur about every 4 to 6 weeks. On `node-groups create`, `--maintenance-interval=recurrent` limits planned updates to no more often than every 28 days (`as-needed` is the alternative), and `--maintenance-window-start-time` takes `00:00`, `04:00`, `08:00`, `12:00`, `16:00` or `20:00` (GMT) for a 4-hour window. Windows are fixed at creation and not supported with `migrate-within-node-group`.
- Test with `gcloud compute instances simulate-maintenance-event` or `gcloud compute sole-tenancy node-groups perform-maintenance`.
- You cannot change the policy of a live node group.

## 4. BYOL mechanics
- Import your own media: `gcloud compute images import IMAGE --source-file=<VMDK or gs:// path> --byol`. Images based on Google premium images are not eligible. Run the precheck tool in the source VM first and enable the Cloud Build API.
- Activate with a MAK via startup scripts or your own KMS; BYOL images cannot activate against Compute Engine's license server.
- Provision on a node group built with `restart-in-place` or `migrate-within-node-group` when licences are per physical core. For `migrate-within-node-group`, target a single group by group name, not a single node.
- Enable Cloud Logging and export to BigQuery to track physical server usage; Compute Engine reports the physical server ID for each VM, so you can reconstruct host history. Report consumption to your vendor yourself.
- Check your own licence agreement for rules on counting cores or relocating licences; this skill does not state vendor terms.

## 5. CPU overcommit
Node template `--cpu-overcommit-type=enabled` (set at template creation) and a per-VM minimum CPUs `--min-node-cpu`. Maximum overcommit ratio 2.0, only for N1, N2, N2D and N4 nodes. Suited to bursty, uncorrelated, non-critical workloads. It carries an extra premium; read the overcommit page before enabling.

## Gotchas
- Node groups are zonal; for HA, put node groups in different zones.
- Quota: new projects start with a CPU quota; node groups count whole-node vCPUs, so request quota for the node group size (two 96-vCPU nodes need 192).
- Sole-tenant VMs cannot use some machine series (T2D, T2A, E2, C2D, A3 Ultra, A3 Edge, A4, A4X, bare metal), cannot be preemptible and cannot set a minimum CPU platform.
- Consult the pricing page for committed use discount behaviour: resource-based CUDs do not cover the sole-tenancy premium.

## Verify
- [ ] `node-groups describe` shows `maintenancePolicy` matching the licence requirement and VMs placed on expected nodes.
- [ ] Cloud Logging shows the physical server ID for each BYOL VM.

## Checked
2026-10-28. Confirmed against the Sole-tenancy overview, the BYOL page, the provisioning page, the CPU overcommit page and the gcloud `node-groups create` and `node-templates create` references: policies and their suitability, restart-in-place TERMINATE requirement, holdback nodes, 28-day interval and window start times, `images import --byol`, MAK/KMS activation, logging of server IDs, overcommit limits, quota example, restrictions. Corrected: maintenance interval and window are flags of `node-groups create`, not the template; overcommit flag is `--min-node-cpu`; BYOL is done by `images import --byol`, not a licences URL. Removed: the 10 percent premium figure, Oracle and Windows 90-day rules, SQL Server Software Assurance claim, unconfirmed error strings and delete behaviour, the node-group CUD SKU claim.
Method: documentation only; no commands were run.
