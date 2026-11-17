---
id: computing-software.cloud-infrastructure-engineering.google-cloud.deploying-slurm-clusters-with-cluster-toolkit
name: deploying-slurm-clusters-with-cluster-toolkit
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, hpc, slurm-cluster-deploy, slurm-gcp, cluster-toolkit, hpc-toolkit, filestore, autoscaling-partitions]
level: advanced
status: docs-checked
description: "Deploy an autoscaling Slurm cluster on Google Cloud with Cluster Toolkit blueprints: VPC, shared Filestore, nodesets and partitions, controller and login nodes, then operate it."
sources: ["https://docs.cloud.google.com/cluster-toolkit/docs/overview", "https://docs.cloud.google.com/cluster-toolkit/docs/quickstarts/slurm-cluster", "https://github.com/GoogleCloudPlatform/cluster-toolkit", "https://raw.githubusercontent.com/GoogleCloudPlatform/cluster-toolkit/main/examples/hpc-slurm.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deploying Slurm clusters with Cluster Toolkit

Cluster Toolkit's `gcluster` engine turns a YAML **blueprint** into a Terraform/Packer deployment directory. The Slurm-GCP v6 modules give a controller that creates compute VMs on demand.

## 1. Blueprint (trimmed from `examples/hpc-slurm.yaml`)
```yaml
blueprint_name: hpc-slurm
vars: {project_id: <P>, deployment_name: hpc-slurm, region: us-central1, zone: us-central1-a}
deployment_groups:
- group: primary
  modules:
  - {id: network, source: modules/network/vpc}
  - {id: private_service_access, source: modules/network/private-service-access, use: [network]}
  - id: homefs
    source: modules/file-system/filestore
    use: [network, private_service_access]
    settings: {local_mount: /home}
  - id: compute_nodeset
    source: community/modules/compute/schedmd-slurm-gcp-v6-nodeset
    use: [network]
    settings: {node_count_dynamic_max: 20, machine_type: <MACHINE_TYPE>, bandwidth_tier: gvnic_enabled}
  - id: compute_partition
    source: community/modules/compute/schedmd-slurm-gcp-v6-partition
    use: [compute_nodeset]
    settings: {partition_name: compute, is_default: true}
  - id: slurm_login
    source: community/modules/scheduler/schedmd-slurm-gcp-v6-login
    use: [network]
  - id: slurm_controller
    source: community/modules/scheduler/schedmd-slurm-gcp-v6-controller
    use: [network, compute_partition, homefs, slurm_login]
```
`use:` wires modules together. Private Service Access is the example's recommended setup for Filestore and needs the `compute.networkAdmin` role (in Owner, not Editor).

## 2. Build and deploy
```bash
git clone https://github.com/GoogleCloudPlatform/cluster-toolkit && cd cluster-toolkit && make
./gcluster deploy examples/hpc-slurm.yaml --vars project_id=<P>
```
`make` needs Go and Terraform (and Packer) installed first; the README also offers pre-built release bundles. `gcluster expand` validates a blueprint without writing a deployment directory. Then log in to the login node as the quickstart describes and run `sinfo` and `srun -N 2 hostname`. Tear down with:
```bash
./gcluster destroy hpc-slurm --auto-approve
```
Dynamic nodes are created when jobs queue and deleted after inactivity (the quickstart shows autoscaled nodes removed automatically after a period of inactivity), so you pay for compute nodes while they exist.

## 3. Operate
- Images: build a custom Slurm image (Packer group in the blueprint) with your apps and MPI so nodes boot fast.
- Check regional quota for the machine family (the example notes H3 is available only in specific zones and does not support pd-ssd or pd-standard disks).
- Partition setting `exclusive: false` lets nodes stay up after jobs finish.
- Spot: nodesets have `enable_spot_vm`; keep a separate on-demand partition for long tightly coupled jobs.

## Gotchas
- `node_count_dynamic_max` times machine vCPUs must fit regional CPU quota or jobs pend with resume failures.
- Changing partitions means re-running `gcluster deploy`; jobs on removed partitions fail.
- Home filesystem sizing and a separate scratch filesystem (the README lists Managed Lustre, Filestore and GCS FUSE as storage options) matter for I/O-heavy jobs.

## Verify
- [ ] `sinfo` shows the partition with powered-down nodes; a test `sbatch` spins nodes up and they are removed after the idle period.
- [ ] `gcloud compute instances list` shows only the controller and login nodes when idle.

## Checked
2026-10-31. Confirmed in the Cluster Toolkit README and quickstart page and in `examples/hpc-slurm.yaml`: module sources, `use:`, `local_mount`, `node_count_dynamic_max`, `partition_name`, `is_default`, `exclusive`, `enable_spot_vm`, `bandwidth_tier: gvnic_enabled`, `gcluster deploy`/`expand`/`destroy`, `--vars`, `--auto-approve` on destroy, autoscaled nodes removed when idle, H3 zone and disk notes, PSA role note. Removed: `size_gb`, `enable_placement`, `tier_1_enabled`, `suspend_time`, the login host name and IAP ssh command, `/var/log/slurm/`, the c2d/H3 sizing, "Filestore size sets throughput" and the claim that compute is billed only while jobs run (replaced by the page's wording).
Method: documentation only; no commands were run.
