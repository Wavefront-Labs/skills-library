---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.cloud-service-discovery-ec2-azure-gce
name: cloud-service-discovery-ec2-azure-gce
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, service-discovery, ec2-sd-configs, azure-sd-configs, gce-sd-configs, ec2-sd, azure-sd, gce-sd, cloud-sd, instance-tags, iam-permissions, refresh-interval, private-ip, lightsail-sd, scaleway-sd, hetzner-sd, pca]
level: practitioner
status: docs-checked
description: "Discover VMs with ec2_sd, azure_sd and gce_sd: credentials and permissions, filters, __meta tag/label names, refresh intervals, and relabeling to set the scrape port."
sources: ["https://prometheus.io/docs/prometheus/latest/configuration/configuration/#ec2_sd_config", "https://prometheus.io/docs/prometheus/latest/configuration/configuration/#azure_sd_config", "https://prometheus.io/docs/prometheus/latest/configuration/configuration/#gce_sd_config"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud VM service discovery

**Goal:** scrape node_exporter (or any agent) on every VM in an account without maintaining
a target file, using tags to select and label.

## 1. AWS EC2
```yaml
  - job_name: ec2-node
    ec2_sd_configs:
      - region: eu-west-1
        # credentials: env / shared file / instance role; or access_key + secret_key(_file)
        role_arn: arn:aws:iam::123456789012:role/prometheus-sd     # cross-account
        port: 9100
        refresh_interval: 60s
        filters:                                  # server-side, saves API calls
          - name: tag:monitoring
            values: [enabled]
          - name: instance-state-name
            values: [running]
    relabel_configs:
      - source_labels: [__meta_ec2_private_ip]
        regex: (.+)
        replacement: ${1}:9100
        target_label: __address__            # default __address__ is private IP:port already; set explicitly when mixing ports
      - source_labels: [__meta_ec2_tag_Name]
        target_label: instance
      - source_labels: [__meta_ec2_availability_zone]
        target_label: az
```
IAM: `ec2:DescribeInstances` is required; `ec2:DescribeAvailabilityZones` is optional and only needed for
`__meta_ec2_availability_zone_id`. The `region` falls back to the instance metadata when blank, and `port`
defaults to 80. Useful meta labels: `__meta_ec2_tag_<tagkey>`, `__meta_ec2_instance_id`,
`__meta_ec2_instance_type`, `__meta_ec2_instance_state`, `__meta_ec2_private_dns_name`, `__meta_ec2_public_ip`,
`__meta_ec2_vpc_id`, `__meta_ec2_subnet_id`, `__meta_ec2_instance_lifecycle` (set only for spot or scheduled
instances), `__meta_ec2_platform` (set to windows on Windows servers).

## 2. Azure
```yaml
  - job_name: azure-node
    azure_sd_configs:
      - subscription_id: <SUBSCRIPTION_ID>
        authentication_method: ManagedIdentity     # or OAuth with tenant_id/client_id/client_secret
        resource_group: prod-rg                    # optional
        port: 9100
        refresh_interval: 300s
    relabel_configs:
      - source_labels: [__meta_azure_machine_tag_monitoring]
        regex: enabled
        action: keep
      - source_labels: [__meta_azure_machine_name]
        target_label: instance
```
Needs `Microsoft.Compute/virtualMachines/read` and `Microsoft.Network/networkInterfaces/read` for VMs, plus
`Microsoft.Compute/virtualMachineScaleSets/virtualMachines/read` and
`.../virtualMachineScaleSets/virtualMachines/networkInterfaces/read` for scale sets. `authentication_method`
is one of OAuth (default), ManagedIdentity, SDK or WorkloadIdentity; `refresh_interval` defaults to 300s and
`port` to 80. Meta: `__meta_azure_machine_tag_<tagname>`, `__meta_azure_machine_location`,
`__meta_azure_machine_scale_set`, `__meta_azure_machine_private_ip`, `__meta_azure_machine_size`.

## 3. GCE
```yaml
  - job_name: gce-node
    gce_sd_configs:
      - project: my-project
        zone: europe-west1-b          # one zone per block; list several blocks for several zones
        filter: 'labels.monitoring = "enabled" AND status = "RUNNING"'
        port: 9100
        refresh_interval: 60s
    relabel_configs:
      - source_labels: [__meta_gce_instance_name]
        target_label: instance
      - source_labels: [__meta_gce_label_team]
        target_label: team
```
Credentials come from the Google Cloud SDK default client: the file named by `GOOGLE_APPLICATION_CREDENTIALS`,
the well-known application default credentials file, or the GCE metadata server. The service account needs at
least read-only access to compute resources. Meta: `__meta_gce_label_<labelname>`, `__meta_gce_metadata_<name>`,
`__meta_gce_private_ip`, `__meta_gce_public_ip`, `__meta_gce_machine_type`, `__meta_gce_tags` (a list joined
with `tag_separator`, default `,`).

## 4. Common practice
- Filter server-side (`filters`/`filter`) **and** keep a relabel `keep` on a tag so an
  unfiltered account is still safe.
- `refresh_interval` defaults: 60s for EC2 and GCE, 300s for Azure; every refresh calls the cloud API, and each
  Prometheus replica does so independently.
- Set `instance` to the VM name; the default `ip:port` changes when a VM is replaced and
  makes dashboards ugly.
- Metadata labels (`__meta_*`) are dropped after relabeling; copy what you need.

## Gotchas
- EC2 `filters` on `tag:` are exact match; use relabel regex for prefixes.
- Filter on `instance-state-name` (or keep on `__meta_ec2_instance_state`) so stopped instances do not show as down.
- Azure `WorkloadIdentity` uses the environment variables injected by the Azure Workload Identity webhook
  (`AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_FEDERATED_TOKEN_FILE`).
- GCE `zone` is required per block; for several zones use several `gce_sd_configs`.

## Checked
2026-10-28. Confirmed on the Prometheus configuration page (`ec2_sd_config`, `azure_sd_config`, `gce_sd_config`: required
permissions, meta labels, `authentication_method` values, refresh defaults, `port` default 80, `filters`/`filter`, per-zone blocks,
default credential lookup for GCE) and the HTTP API page (`/api/v1/targets`). Removed: `__meta_azure_machine_power_state` (not
documented), 429 throttling and list-all-VMs claims, tag-key sanitising rule, `compute.instances.list` permission name, leading and
trailing commas in `__meta_gce_tags`, `_file` credential suffix claim, and the `/service-discovery` page.
Method: documentation only; no commands were run.

## Verify
- [ ] `/api/v1/targets` lists the expected `activeTargets` and the filtered-out VMs under `droppedTargets` (with `discoveredLabels`).
- [ ] Cloud API throttling errors stay at zero in the Prometheus logs.
- [ ] Replacing a VM (new IP, same name) keeps the same `instance` label.
