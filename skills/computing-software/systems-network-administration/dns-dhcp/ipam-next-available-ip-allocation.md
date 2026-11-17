---
id: computing-software.systems-network-administration.dns-dhcp.ipam-next-available-ip-allocation
name: ipam-next-available-ip-allocation
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [ipam, next-available-ip, netbox, infoblox-nios, automation, race-conditions]
level: practitioner
status: verified
description: "Allocate IP addresses through IPAM APIs (NetBox available-ips, Infoblox func:nextavailableip, phpIPAM first_free) safely in automation without collisions."
sources:
  - https://netboxlabs.com/docs/netbox/en/stable/integrations/rest-api/
  - https://docs.infoblox.com/space/niosapi/
  - https://phpipam.net/api/api_documentation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API-driven next-available allocation

Provisioning pipelines (Terraform, Ansible, VM orchestration) should ask the IPAM for the next free
address and record it atomically, not ping-sweep or pick from spreadsheets.

## NetBox
```
curl -s -X POST -H "Authorization: Token $T" -H "Content-Type: application/json" \
  https://netbox.example.com/api/ipam/prefixes/42/available-ips/ \
  -d '{"description":"vm-app-07","dns_name":"app07.corp.example.com","status":"active"}'
```
The POST allocates and creates the IP object in one request: the view takes a PostgreSQL advisory lock (key
`available-ips`) around the allocation (NetBox `ipam/api/views.py`; the lock is global to available-ips requests, not
per prefix). GET on the same endpoint only lists, which races if you allocate later. The address is created with the
prefix's mask length unless the body gives `prefix_length`, in the prefix's VRF. Terraform: `netbox_available_ip_address`
(resource in the e-breuninger provider).

## Infoblox
Infoblox's WAPI can allocate the next free address inside the same create call (a server-side function in the
`ipv4addr` field of a `record:host` object) rather than a separate query. The exact function syntax and WAPI version
segment differ by appliance release, so copy them from the WAPI documentation served by your own grid master
(`https://<gm>/wapidoc/`) instead of from memory. Exclude ranges (gateways, DHCP ranges) in the network.

## phpIPAM
`POST /api/<app>/addresses/first_free/<subnetId>/` searches for the first free address in the subnet and creates it
(phpIPAM `Addresses` API controller comments).

## Safe patterns
- Allocate and create in the same API call; never "get next free" then "create" in two calls without a lock.
- Tag allocations with owner/automation run IDs so failed pipelines can clean up.
- Reserve gateway and infrastructure addresses in the IPAM so they are never returned.
- Release on destroy (Terraform destroy deletes the IP object; ensure the provider does).
- Verify uniqueness: optional ARP/ping check before use, but trust the IPAM as source of truth.

## Verify
- [ ] Parallel test allocations (e.g. 10 concurrent API calls) return 10 distinct addresses, all recorded in the IPAM.
