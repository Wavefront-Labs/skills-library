---
id: computing-software.systems-network-administration.netbox.wireless-lans-and-links
name: wireless-lans-and-links
category: computing-software
field: systems-network-administration
product: netbox
tags: [wireless, wireless-lan, wireless-link]
level: practitioner
status: docs-checked
description: "Record SSIDs, authentication and point-to-point wireless links."
sources: ["https://netboxlabs.com/docs/netbox/features/wireless/", "https://netboxlabs.com/docs/netbox/features/tenancy/", "https://netboxlabs.com/docs/netbox/administration/permissions/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Wireless

Goal: model wireless alongside cabled plant.

**Wireless LAN.** A multi-access network shared by many wireless clients, identified by a common SSID and authentication parameters. LANs can be organised into self-nesting groups.

Authentication attributes (all optional):

- **Type**: Open, WEP, WPA, and others
- **Cipher**: Auto, TKIP or AES
- **Pre-shared key (PSK)**: the secret configured on all participating clients

**Wireless link.** A point-to-point connection between exactly two stations. It behaves much like a cable but models the wireless medium more accurately. Like a LAN it has an SSID and optional authentication attributes.

**When to use which**

- Many clients on one SSID: wireless LAN.
- Backhaul bridge between two radios: wireless link.
- Physical copper or fibre: cable.

**Related.** Wireless LANs and wireless links can be assigned to tenants. Object-based permissions can limit viewing to a subset of objects, which is one way to restrict who sees a PSK.

**Checklist**

1. Group LANs by site or purpose.
2. Use links for two-station bridges.
3. Limit who can view PSKs.

## Checked

Method: docs-checked 2026-11-09 against the NetBox Wireless and Tenancy feature pages and the Object-Based Permissions page (all read in full).
