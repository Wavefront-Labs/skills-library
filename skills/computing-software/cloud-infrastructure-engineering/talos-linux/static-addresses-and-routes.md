---
id: computing-software.cloud-infrastructure-engineering.talos-linux.static-addresses-and-routes
name: static-addresses-and-routes
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [static-ip, routes, linkconfig, gateway, networking, addressspec]
level: practitioner
status: docs-checked
description: "Assign static addresses and routes to Talos links: addresses and routes fields, routePriority, three gateway layouts, a LinkConfig example and talosctl status commands."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/networking/configuration/static.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Static addressing works on physical links (through a `LinkConfig` document) and on logical links (bond, bridge, VLAN), where the fields sit directly in the logical link document.

Addresses are CIDR strings, with an optional `routePriority` for the implicit route:

```yaml
addresses:
    - address: 192.168.1.100/24
    - address: 2001:db8::1/64
      routePriority: 100
```

Routes: `destination` (omit for a default route), `gateway` (omit for a directly connected route), plus advanced fields such as `metric` and `mtu`.

Typical layouts:

```yaml
# subnet address with a gateway in the same subnet
addresses:
    - address: 192.168.1.100/24
routes:
    - gateway: 192.168.1.1
```

```yaml
# /32 address, gateway outside the subnet: add a host route to the gateway first
addresses:
    - address: 192.168.1.100/32
routes:
    - destination: 192.168.1.1
    - gateway: 192.168.1.1
```

```yaml
# private network with no default gateway, specific routes only
addresses:
    - address: 10.0.0.3/24
routes:
    - destination: 10.1.0.0/24
      gateway: 10.0.0.1
```

Complete physical-link example:

```yaml
apiVersion: v1alpha1
kind: LinkConfig
name: enp0s3
addresses:
    - address: 192.168.1.100/24
routes:
    - gateway: 192.168.1.1
```

Observe with `talosctl get addresses` and `talosctl get routes` (everything on the node), `talosctl get addressspecs` and `talosctl get routespecs` (what Talos manages), and add `--namespace network-config` to see which source (static, DHCP, operator) each came from. The page's prose spells the flag `--namespace=networkconfig` but its example output uses `--namespace network-config`; use the hyphenated form.

## Checked

2026-11-04. Address and route fields, three layouts, LinkConfig example and observation commands confirmed on the Static Addressing page.

Method: documentation only; no commands were run.
