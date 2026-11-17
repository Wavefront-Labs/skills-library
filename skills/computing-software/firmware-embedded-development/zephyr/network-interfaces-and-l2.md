---
id: computing-software.firmware-embedded-development.zephyr.network-interfaces-and-l2
name: network-interfaces-and-l2
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [net-if, net-if-get-default, net-l2, net-config, ipv4-address-config, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Work with Zephyr network interfaces: find and select net_if instances, L2 types (Ethernet, Wi-Fi, OpenThread, PPP), address configuration, DHCP, and default interface choice."
sources:
  - https://docs.zephyrproject.org/latest/connectivity/networking/api/net_if.html
  - https://docs.zephyrproject.org/latest/connectivity/networking/net-stack-architecture.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/net/net_if.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/net/ip/Kconfig
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/net/lib/config/Kconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network interfaces and L2 layers

Each network driver instance registers a `struct net_if` bound to an **L2** (link layer):
Ethernet, IEEE 802.15.4, OpenThread, Bluetooth IPSP, PPP, Wi-Fi (Ethernet-style L2 with
`wifi_mgmt`), CAN-ISO-TP, dummy/loopback.

## Finding interfaces
```c
#include <zephyr/net/net_if.h>

struct net_if *iface = net_if_get_default();               /* CONFIG_NET_DEFAULT_IF_* chooses */
struct net_if *eth   = net_if_get_first_by_type(&NET_L2_GET_NAME(ETHERNET));
struct net_if *wifi  = net_if_get_first_wifi();
int idx = net_if_get_by_iface(iface);                       /* 1-based index */

static void cb(struct net_if *iface, void *user) { /* ... */ }
net_if_foreach(cb, NULL);
```
Default interface selection: `CONFIG_NET_DEFAULT_IF_ETHERNET`, `_WIFI`, `_OFFLOAD`,
`_IEEE802154`, etc.; otherwise the first registered.

## Addresses
Static at boot via net_config:
```
CONFIG_NET_CONFIG_SETTINGS=y
CONFIG_NET_CONFIG_MY_IPV4_ADDR="192.0.2.10"
CONFIG_NET_CONFIG_MY_IPV4_NETMASK="255.255.255.0"
CONFIG_NET_CONFIG_MY_IPV4_GW="192.0.2.1"
CONFIG_NET_CONFIG_NEED_IPV4=y
```
Runtime:
```c
struct net_in_addr a, m;     /* 4.x names; the old ones need CONFIG_NET_NAMESPACE_COMPAT_MODE */
net_addr_pton(NET_AF_INET, "192.0.2.10", &a);
net_if_ipv4_addr_add(iface, &a, NET_ADDR_MANUAL, 0);
net_addr_pton(NET_AF_INET, "255.255.255.0", &m);
net_if_ipv4_set_netmask_by_addr(iface, &a, &m);       /* net_if_ipv4_set_netmask() is deprecated */

net_dhcpv4_start(iface);                               /* CONFIG_NET_DHCPV4=y */
```
Listen for `NET_EVENT_IPV4_ADDR_ADD` (net_mgmt) or use conn_mgr before opening sockets.

## Interface state
- `net_if_up(iface)` / `net_if_down(iface)`: administrative state.
- `net_if_is_up()` vs carrier (`net_if_is_carrier_ok`) vs dormant (Wi-Fi not associated):
  `enum net_if_oper_state` follows RFC 2863.
- `NET_EVENT_IF_UP/DOWN` events.

## Multiple interfaces
- Bind a socket to an interface with the `SO_BINDTODEVICE` socket option (`ZSOCK_SO_BINDTODEVICE`,
  value 25) and a `struct net_ifreq` carrying the interface name (`net_if_get_name`,
  `CONFIG_NET_INTERFACE_NAME`, default y).
- Routing chooses by destination subnet, then default interface.
- `CONFIG_NET_IF_MAX_IPV4_COUNT`/`_IPV6_COUNT` set the maximum number of IPv4/IPv6 network
  interfaces (default 1; 2 with loopback or dual virtual interfaces); raise them when adding
  interfaces.

## Shell
```
uart:~$ net iface        # list interfaces, L2, addresses, MTU
uart:~$ net ipv4 add 1 192.0.2.10 255.255.255.0
uart:~$ net ping 192.0.2.1
```

## Verify
- [ ] `net iface` shows the expected L2, address and state on each interface.
- [ ] App waits for an address/connectivity event before using the network.

## Checked

Zephyr v4.4.2 documentation and source (latest release on 2026-10-27), read from the zephyr repository.
Confirmed in headers and Kconfig: net_if_get_default, net_if_get_first_by_type with `NET_L2_GET_NAME` (net_l2.h), net_if_get_first_wifi, net_if_get_by_iface (index is 1-based, from net_if.c), net_if_foreach, net_if_ipv4_addr_add, net_if_ipv4_set_netmask_by_addr (and the deprecated net_if_ipv4_set_netmask), net_addr_pton, net_dhcpv4_start (CONFIG_NET_DHCPV4), net_if_up/down, net_if_is_carrier_ok, net_if_get_name, `enum net_if_oper_state` documented as RFC 2863, events NET_EVENT_IF_UP/DOWN and NET_EVENT_IPV4_ADDR_ADD; Kconfig NET_DEFAULT_IF_ETHERNET/WIFI/OFFLOAD/IEEE802154, NET_CONFIG_SETTINGS, NET_CONFIG_MY_IPV4_ADDR/NETMASK/GW, NET_CONFIG_NEED_IPV4, NET_INTERFACE_NAME, NET_IF_MAX_IPV4_COUNT and IPV6 counterpart; SO_BINDTODEVICE; shell commands `net iface` and `net ipv4`.
Stale claims fixed: networking types and constants are namespaced in 4.x (`net_in_addr`, `NET_AF_INET`, `net_ifreq`), with the old names kept only by CONFIG_NET_NAMESPACE_COMPAT_MODE; removed the unconfirmed "fails silently" remark and the "recent releases" hedges.

Method: documentation only; no commands were run.
