---
id: computing-software.cloud-infrastructure-engineering.azure.subnet-delegation-for-paas-services
name: subnet-delegation-for-paas-services
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vnet, subnet-delegation, delegated-subnets, delegation, network-intent-policies, subnets]
level: practitioner
status: docs-checked
description: "Plan and configure subnet delegation for PaaS services: list available delegations, delegate or remove a subnet, and what a delegated subnet restricts."
sources: ["https://learn.microsoft.com/azure/virtual-network/subnet-delegation-overview", "https://learn.microsoft.com/azure/virtual-network/manage-subnet-delegation", "https://learn.microsoft.com/azure/virtual-network/virtual-network-for-azure-services", "https://learn.microsoft.com/en-us/cli/azure/network/vnet/subnet"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Subnet delegation for PaaS

**Goal:** each VNet-injected PaaS service gets a correctly delegated subnet that suits that
service's rules, and delegation can be removed cleanly later.

## What delegation is
Delegating a subnet gives a service explicit permission to create service-specific resources in it
(through a unique identifier when the service is deployed). The virtual network owner does the
delegating. The delegated service can then add pre- or post-deployment conditions such as
Network Intent Policies, which can block actions that would break the injected service. You still
control NSGs, route tables and service endpoints on the subnet, within what that service allows.

Each service defines its own deployment model. Check the service's own article for: shared versus
dedicated subnet, NSG and route table support (and whether they may be shared with other subnets),
the minimum number of IP addresses, whether the range must be from private address space, and
custom DNS requirements. A delegated subnet cannot be used with a private endpoint, so private
endpoint network policies should not be configured on it.

The "Services that can be deployed into a virtual network" table says whether each service needs a
dedicated subnet (only that service's resources, no customer VMs or scale sets): for example Azure
SQL Managed Instance, Container Apps environments and VPN Gateway are listed as dedicated, virtual
machines as not, and AKS as "not mandatory but recommended". Re-read the table; it changes.

## Find the delegation name
```bash
az network vnet subnet list-available-delegations -l westus --query [].serviceName
```
This lists the services available for delegation in a region (the CLI reference example). Names
look like `Microsoft.Sql/managedInstances`.

## Configure
Needed permission if you did not create the subnet: `Microsoft.Network/virtualNetworks/subnets/write` (the built-in Network Contributor role includes it).
```bash
az network vnet subnet update -g rg-net --vnet-name vnet-spoke -n snet-delegated --delegations Microsoft.Sql/managedInstances
az network vnet subnet update -g rg-net --vnet-name vnet-spoke -n snet-delegated --remove delegations   # to remove
```
The how-to page uses `update` to add and remove; `az network vnet subnet create` also has a `--delegations` flag per the CLI reference. In the portal use Subnets, select the subnet, then "Delegate subnet to a service" (select None to remove).

## Cleaning up
Some services require the delegation to be removed before the subnet or virtual network can be deleted. Remove the service's resources from the subnet, then remove the delegation as above.

## Verify
- [ ] `az network vnet subnet show -g rg-net --vnet-name vnet-spoke -n snet-delegated --query delegations` shows the service in `serviceName`; after removal the output is `[]`.

## Checked

2026-11-07. Read in full: What is subnet delegation, Add or remove subnet delegation (portal, PowerShell and CLI tabs, including the verify output), and Integrate Azure services with virtual networks (including the services table and its two footnotes). The `az network vnet subnet` CLI reference is large: I searched it for `--delegations`, `--remove`, `list-available-delegations` and its `-l`/`--query` example, not read end to end.
Trimmed: the SQL MI /26 subnet example and per-service size table, the Bicep snippet, "network intent policies you can't remove", service association link (SAL) cleanup order and timing, App Service and Container Apps IP consumption, "can't resize a subnet", the NSG policy conflict claim and the IP plan document step (none stated on these pages). Added: the required permission, the private endpoint restriction and the dedicated-subnet table pointer.

Method: documentation only; no commands were run.
