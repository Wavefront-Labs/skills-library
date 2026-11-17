---
id: computing-software.cloud-infrastructure-engineering.kubespray.openstack-external-cloud-provider-and-cinder-csi
name: openstack-external-cloud-provider-and-cinder-csi
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [openstack, cloud-provider, octavia, cinder-csi, lbaas, multi-nic]
level: advanced
status: docs-checked
description: "Set up the external OpenStack cloud provider with Octavia and Cinder CSI: cloud_provider external, cinder_csi_enabled, topology, multi-NIC networking and lbaas variables."
sources:
  - https://kubespray.io/docs/cloud_controllers/openstack.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The OpenStack provider in Kubespray uses Octavia by default (not Neutron LBaaS).

1. In `group_vars/all/all.yml`:

```yaml
cloud_provider: external
external_cloud_provider: openstack
```

2. In `group_vars/all/openstack.yml` enable Cinder CSI:

```yaml
cinder_csi_enabled: true
```

3. Optional topology support: `cinder_topology: true` (override the default "nova" zone with `cinder_topology_zones` if your cloud has custom zone names). `cinder_csi_ignore_volume_az: true` ignores the volume AZ and schedules on any node AZ.

4. If you used `openstack_lbaas_subnet_id`, replace it with `external_openstack_lbaas_subnet_id`.

5. For multi-NIC VMs, override the networking defaults:

```yaml
external_openstack_network_ipv6_disabled: false
external_openstack_network_internal_networks: []
external_openstack_network_public_networks: []
```

6. Metadata lookup can be changed: `external_openstack_metadata_search_order: "configDrive,metadataService"`.

7. Load balancer variables: `external_openstack_lbaas_enabled`, `_floating_network_id`, `_floating_subnet_id`, `_method` (ROUND_ROBIN), `_provider` (amphora), `_subnet_id`, `_member_subnet_id`, `_network_id`, `_manage_security_groups`, `_create_monitor` with `_monitor_delay`, `_monitor_max_retries`, `_monitor_timeout`, and `_internal_lb`.

8. Source your OpenStack rc file so `OS_AUTH_URL`, `OS_USERNAME`, `OS_PASSWORD` and the rest are available to the provider, then run `cluster.yml`.

For Open Telekom Cloud the page notes you must set `wait_for_floatingip = "true"` in `cluster.tfvars`.

## Checked

The numbered configuration steps and variable names were confirmed on the OpenStack page.

Method: docs-checked 2026-11-09 against the Kubespray docs/cloud_controllers/openstack.md page (full file read).
