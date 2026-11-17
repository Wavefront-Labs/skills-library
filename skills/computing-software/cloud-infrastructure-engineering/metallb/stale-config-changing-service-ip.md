---
id: computing-software.cloud-infrastructure-engineering.metallb.stale-config-changing-service-ip
name: stale-config-changing-service-ip
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, stale-config, reassign-ip, ipaddresspool, controller, service]
level: advanced
status: docs-checked
description: "Why removing a pool with IPs in use leaves MetalLB on a stale config, and the two ways to force reassignment: restart the controller pod or recreate the Service."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/configuration/_advanced_ipaddresspool_configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stale config and changing a service IP

MetalLB tries to preserve connectivity. If a configuration change would disrupt a service, such as removing an `IPAddressPool` containing IPs currently assigned, MetalLB does not reallocate; it marks the change stale and keeps running with the last valid configuration.

To give services new IPs, either:
1. restart the `controller` pod, or
2. delete and re-create the Service.

The docs note this behaviour may change in future so that MetalLB observes whatever state you request, even if disruptive.

Detect stale state: metric `metallb_k8s_client_config_stale_bool` equals 1 (`computing-software.cloud-infrastructure-engineering.metallb.alert-rules`), or config errors in logs (`computing-software.cloud-infrastructure-engineering.metallb.troubleshoot-config-validation`).

## Checked

2026-11-04. Confirmed against the MetalLB "Advanced AddressPool configuration" page (Changing the IP of a service: stale marking, the two re-assign options, behaviour-may-change note) and the Troubleshooting page (stale metric and `failed to parse the configuration` log). Removed the invented kubectl commands and the generic Verify line. Note that the Concepts page says MetalLB assigns another set of IPs when a pool is deleted or edited; the Advanced page describes the stale behaviour, so test which applies to your version.

Method: documentation only; no commands were run.
