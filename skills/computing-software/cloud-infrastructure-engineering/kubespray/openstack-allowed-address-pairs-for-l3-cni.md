---
id: computing-software.cloud-infrastructure-engineering.kubespray.openstack-allowed-address-pairs-for-l3-cni
name: openstack-allowed-address-pairs-for-l3-cni
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [openstack, calico, kube-router, neutron, allowed-address, spoofing]
level: sme
status: docs-checked
description: "Let Calico or kube-router pod traffic pass OpenStack anti-spoofing by adding allowed-address entries for the service and pod subnets to each instance's Neutron port."
sources:
  - https://kubespray.io/docs/cloud_controllers/openstack.md
  - https://kubespray.io/docs/CNI/calico.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Calico and kube-router are L3 CNIs: they route packets with pod IP addresses directly instead of encapsulating them in host addresses. OpenStack filters packets from IPs it does not know to prevent spoofing, so you must allow the pod networks.

1. Find the instance IDs:

```bash
openstack server list --project YOUR_PROJECT
```

2. Find the connected Neutron ports by device:

```bash
openstack port list -c id -c device_id --project YOUR_PROJECT
```

3. For each port ID, allow both `kube_service_addresses` (default `10.233.0.0/18`) and `kube_pods_subnet` (default `10.233.64.0/18`):

```bash
openstack port set 5662a4e0-e646-47f0-bf88-d80fbd2d99ef --allowed-address ip-address=10.233.0.0/18 --allowed-address ip-address=10.233.64.0/18
```

If every VM in the tenant belongs to the Kubespray deployment, sweep all ports at once:

```bash
openstack port list --device-owner=compute:nova -c ID -f value | xargs -tI@ openstack port set @ --allowed-address ip-address=10.233.0.0/18 --allowed-address ip-address=10.233.64.0/18
```

Then run the playbook.

The Calico page adds a related point: on OpenStack, `ipip` traffic must be allowed in security groups or you will see timeouts, and Calico is always set to `calico_ipip_mode: Always` when a cloud provider is defined.

## Checked

The port-listing and allowed-address commands were confirmed on the OpenStack page; the closing paragraph was confirmed on the Calico page. Port IDs in the example are the page's sample values.

Method: docs-checked 2026-11-09 against the Kubespray docs/cloud_controllers/openstack.md page (full file read) and the Calico page docs/CNI/calico.md (OpenStack and ipip passages read).
