---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-coredns-and-cloud-controller
name: k3s-coredns-and-cloud-controller
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, coredns, cloud-controller, disable-cloud-controller]
level: practitioner
status: docs-checked
description: "Disable CoreDNS or the embedded cloud controller manager and deploy replacements without leaving nodes tainted."
sources:
  - https://docs.k3s.io/networking/networking-services
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
CoreDNS is deployed on server startup. Disable it by starting all servers with `--disable=coredns`; you must then provide your own cluster DNS. `--cluster-dns` and `--cluster-domain` must be identical on all servers in an HA cluster; look up their defaults in the K3s server flag reference.

Embedded cloud controller manager (CCM) duties:

- hosts the ServiceLB controller
- clears the node.cloudprovider.kubernetes.io/uninitialized taint
- sets node address fields from --node-ip, --node-external-ip, --node-internal-dns and --node-external-dns

To deploy an external CCM, first start all servers with `--disable-cloud-controller`. Node addresses then come from the cloud provider metadata APIs rather than the K3s flags.

Failure mode: if you disable the built-in CCM and set `--kubelet-arg=cloud-provider=external` without deploying and configuring a working replacement, nodes stay tainted and unschedulable. By default, disabling the built-in CCM keeps K3s from setting the kubelet cloud-provider arg, meaning no cloud provider is in use; Node Provider-IDs and External Addresses are then not set.

Hostnames: providers like Linode may create machines named localhost or with no hostname, breaking name resolution. Pass `--node-name` or K3S_NODE_NAME.

## Checked

2026-11-03: read docs.k3s.io networking/networking-services (and basic-network-options for the Linode hostname note). Confirmed: --disable=coredns, the embedded CCM duties, --disable-cloud-controller, the cloud-provider=external failure mode and the Linode localhost hostname note. Removed: the default values of --cluster-dns (10.43.0.10) and --cluster-domain, which no fetched page states.

Method: documentation only; no commands were run.
