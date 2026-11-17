---
id: computing-software.cloud-infrastructure-engineering.azure.private-link-service-behind-standard-load-balancer
name: private-link-service-behind-standard-load-balancer
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, private-link-service, private-link-service-setup, pls-nat, proxy-protocol, standard-load-balancer, visibility]
level: advanced
status: docs-checked
description: "Publish your own service privately to other VNets/tenants with Private Link Service on a Standard LB: NAT IPs, visibility and auto-approval, proxy protocol v2."
sources: ["https://learn.microsoft.com/azure/private-link/private-link-service-overview", "https://learn.microsoft.com/azure/private-link/create-private-link-service-cli", "https://learn.microsoft.com/en-us/cli/azure/network/private-link-service", "https://learn.microsoft.com/en-us/cli/azure/network/private-link-service/connection", "https://learn.microsoft.com/en-us/cli/azure/network/private-endpoint", "https://learn.microsoft.com/en-us/cli/azure/network/vnet/subnet"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Private Link Service behind a Standard load balancer

**Goal:** customers or other business units consume your service through a private endpoint in
*their* VNet, with no peering and no source-IP conflicts.

## Architecture
Consumer private endpoint (their VNet) -> Private Link service (your VNet, NAT IPs) -> Standard
Load Balancer frontend IP configuration -> backend pool. Traffic reaches your service sourced from
the Private Link service NAT IPs, so there is no IP conflict between consumer and provider address
space. The Private Link service must be deployed in the same region as the virtual network and the
Standard Load Balancer.

## Create
```bash
az network vnet subnet update -g rg-svc --vnet-name vnet-svc -n snet-pls --private-link-service-network-policies Disabled
az network private-link-service create -g rg-svc -n pls-orders-api \
  --vnet-name vnet-svc --subnet snet-pls \
  --lb-name ilb-orders --lb-frontend-ip-configs fe-orders \
  --private-ip-address-version IPv4 --private-ip-allocation-method Dynamic \
  --visibility "<consumer-sub-id-1>" "<consumer-sub-id-2>" \
  --auto-approval "<consumer-sub-id-1>" \
  --enable-proxy-protocol false
az network private-link-service show -g rg-svc -n pls-orders-api --query alias -o tsv   # share with consumers
```
- The `privateLinkServiceNetworkPolicies` setting must be disabled on the subnet before the service can be created (the CLI quickstart does this with `--private-link-service-network-policies Disabled`; the older `--disable-private-link-service-network-policies` is documented as being replaced by it).
- NAT IPs: at least eight addresses available in the NAT subnet is recommended; up to eight NAT IP addresses per Private Link service, and you cannot delete the last remaining one.
- **Visibility** options, most to least restrictive: role-based access control only, restricted by subscription, anyone with your alias.
- **Auto-approval** is a subset of the visibility list: subscriptions on it are approved automatically; other requests from visible subscriptions stay Pending until you approve them.
- The alias (`Prefix.GUID.region.azure.privatelinkservice`) or the resource URI can be shared; you choose the prefix and cannot change the alias afterwards.

## Consumer side
```bash
az network private-endpoint create -g rg-consumer -n pe-orders --vnet-name vnet-c --subnet snet-pe \
  --manual-request true --request-message "Contoso tenant 123" \
  --private-connection-resource-id <pls-alias-or-id> --connection-name orders
```
`--manual-request true` is for when the consumer has no access to the Private Link service subscription; the request message is limited to 140 characters.

## Client IP visibility
The backend sees the NAT IP. To get consumer connection information enable TCP proxy protocol v2
(`--enable-proxy-protocol true`). The header also carries the private endpoint LinkID (a custom TLV, type 0xEE, subtype 0x01, 4-byte little-endian value), which matches the `linkIdentifier` property of the private endpoint connection. You are responsible for parsing the header on the backend: requests fail if the setting is on and the service does not parse it, or the service expects the header while the setting is off. Once on, the header is also included in HTTP/TCP health probes from the host to the backend VMs. It applies to all load balancers and backend VMs behind that service, so set it consistently on every Private Link service sharing the same load balancer or backend pool, otherwise health probes fail.

## Limitations (from the overview)
- Standard Load Balancer only, not Basic; the backend pool must be configured by NIC, not by IP address.
- IPv4 only; TCP and UDP only.
- Idle timeout of about 5 minutes (300 seconds): client applications should use TCP keepalives lower than that.
- An inbound NAT rule of type backend pool needs a load balancing rule to work with Private Link service.

## Operate
- Approve, reject or delete requests: `az network private-link-service connection update --connection-status Rejected` (accepted values Approved, Rejected, Removed; add `--service-name` and the connection name). Requests are listed under the `privateEndpointConnections` property of the service.
- Before deleting a Private Link service, reject all connections so none remain.

## Verify
- [ ] `az network private-link-service show` reports `provisioningState` Succeeded and lists the consumer request under `privateEndpointConnections`.

## Checked

2026-11-07. Read in full: Private Link service overview (workflow, properties, details, alias, visibility, access, TCP proxy v2, limitations) and the Create a Private Link service with CLI quickstart (including the subnet policy step and the unused `--manual-request false` example). The CLI reference pages for `az network private-link-service`, `... connection`, `... private-endpoint` and `... vnet subnet` are very large: I searched them for the exact flags, accepted values and descriptions used (`--visibility`, `--auto-approval`, `--enable-proxy-protocol`, `--lb-frontend-ip-configs`, `--private-ip-*`, `--connection-status` values, `--manual-request`, `--request-message` 140 chars, `--private-link-service-network-policies`), not read end to end.
Corrected or trimmed: the subnet command now uses the documented replacement flag; removed `*` for anyone-visibility (the page names the "anyone with your alias" option, not a wildcard), the claim that frontends must be "internal" or may chain Gateway Load Balancers, the "no privatelink zone" DNS statement, NGINX/HAProxy examples, the health-probe-looks-connected claim and the invented Verify queries and curl step.

Method: documentation only; no commands were run.
