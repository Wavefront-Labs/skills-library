---
id: computing-software.systems-network-administration.netbird.networks-resources
name: networks-resources
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, networks, network-resources, least-privilege, clientless-devices]
level: practitioner
status: docs-checked
description: "Model private infrastructure as NetBird Networks: resources (IP, CIDR, domain, wildcard), routing peers, default-deny policies and the setup sequence."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/networks/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Network maps part of your infrastructure (office LAN, cloud VPC, data center) onto the overlay and reaches devices that cannot run the client, such as printers and appliances. Use one Network per environment.

Resources: a single IP (`/32`), a CIDR range, a domain, or a wildcard domain. Prefer `/32` for least privilege. Resources can be grouped so one policy covers several apps. A wildcard matches subdomains only; the base domain needs its own resource.

Access: resources are not in the `All` group, so a resource with no policy is unreachable. A policy grants a source group access to a destination group or resource on set protocols and ports.

Traffic flow: client encrypts to the routing peer, which decrypts and forwards; by default it masquerades the source to its LAN IP, so return traffic needs no extra policy. A resource policy covers traffic through the routing peer; services on the routing peer itself need a separate peer-to-peer policy.

Setup:
1. Install the client on a host inside the network and register with a setup key.
2. Create the Network and add resources into a resource group.
3. Create a policy from the user group to the resource group.
4. Assign the host as the routing peer.
5. Verify from a client with `netbird networks ls`.

Routing peer must resolve internal names for domain resources.

## Checked

2026-11-04. Confirmed against the NetBird Networks page: resource types, /32 preference, resource groups, wildcard behaviour, All group warning, packet flow and masquerade, forward versus input chain, walkthrough order, `netbird networks ls`, DNS requirement. Nothing removed.
Method: documentation only; no commands were run.
