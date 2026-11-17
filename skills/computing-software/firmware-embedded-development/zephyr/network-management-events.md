---
id: computing-software.firmware-embedded-development.zephyr.network-management-events
name: network-management-events
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-networking, net-mgmt, net-mgmt-event-callback, conn-mgr, l4-connected, network-state-machine, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "React to Zephyr network state with net_mgmt event callbacks and the connection manager: L4 up/down, address events, Wi-Fi requests, and callback rules."
sources:
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/net/net_mgmt.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/net/net_event.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/net/conn_mgr_monitor.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/net/ip/Kconfig.mgmt
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/net/conn_mgr/Kconfig
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/net/wifi_mgmt.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network management events

net_mgmt is Zephyr's event bus for network state (interface up/down, address added, DHCP
bound, Wi-Fi connected) and its request API (connect to Wi-Fi, scan).

## Wait for "internet is usable"
The connection manager aggregates per-interface states into L4 events, which is what an
application usually wants.
```
CONFIG_NET_MGMT=y
CONFIG_NET_MGMT_EVENT=y
CONFIG_NET_CONNECTION_MANAGER=y
```
```c
#include <zephyr/net/net_mgmt.h>
#include <zephyr/net/net_event.h>

#define L4_EVENTS (NET_EVENT_L4_CONNECTED | NET_EVENT_L4_DISCONNECTED)
static struct net_mgmt_event_callback l4_cb;
static K_SEM_DEFINE(net_up, 0, 1);

/* mgmt_event is uint64_t in current releases */
static void l4_handler(struct net_mgmt_event_callback *cb, uint64_t mgmt_event,
                       struct net_if *iface)
{
    if (mgmt_event == NET_EVENT_L4_CONNECTED)    { k_sem_give(&net_up); }
    if (mgmt_event == NET_EVENT_L4_DISCONNECTED) { k_sem_reset(&net_up); app_offline(); }
}

void net_wait_init(void)
{
    net_mgmt_init_event_callback(&l4_cb, l4_handler, L4_EVENTS);
    net_mgmt_add_event_callback(&l4_cb);
    conn_mgr_mon_resend_status();     /* get current state if already connected */
}
/* app thread: k_sem_take(&net_up, K_FOREVER); then open sockets */
```
Register the callback **before** bringing interfaces up, or call `conn_mgr_mon_resend_status()`, which resends
`NET_EVENT_L4_CONNECTED` or `NET_EVENT_L4_DISCONNECTED` depending on current connectivity; otherwise you miss an event that
already happened. `NET_EVENT_L4_CONNECTED` means an interface is up and has an IPv4 or IPv6 address.

## Other useful events
- `NET_EVENT_IPV4_ADDR_ADD` / `NET_EVENT_IPV4_DHCP_BOUND`: got an address.
- `NET_EVENT_IF_UP` / `NET_EVENT_IF_DOWN`: link state.
- `NET_EVENT_WIFI_CONNECT_RESULT`, `NET_EVENT_WIFI_DISCONNECT_RESULT`, `NET_EVENT_WIFI_SCAN_RESULT`.

Only the command part of a callback's mask is a bit mask; the layer and layer code must match exactly, so to
receive events from several layers register one callback struct per layer (L4, IPv4, Wi-Fi...). Event info
(for example the address) is in `cb->info` (with `info_length`) when `CONFIG_NET_MGMT_EVENT_INFO=y`, which
`CONFIG_NET_CONNECTION_MANAGER` selects.

## Requests
```c
struct wifi_connect_req_params p = { .ssid = ssid, .ssid_length = strlen(ssid),
    .psk = psk, .psk_length = strlen(psk), .security = WIFI_SECURITY_TYPE_PSK,
    .channel = WIFI_CHANNEL_ANY, .band = WIFI_FREQ_BAND_2_4_GHZ };
net_mgmt(NET_REQUEST_WIFI_CONNECT, net_if_get_default(), &p, sizeof(p));
```
The return only means "request accepted"; the result arrives as an event.

## Callback rules
Where handlers run depends on the `NET_MGMT_EVENT_WORKER` choice: a dedicated net_mgmt thread
(`CONFIG_NET_MGMT_EVENT_THREAD`, the default, stack size `CONFIG_NET_MGMT_EVENT_STACK_SIZE`), the system work
queue (`CONFIG_NET_MGMT_EVENT_SYSTEM_WORKQUEUE`) or directly in the emitter's context
(`CONFIG_NET_MGMT_EVENT_DIRECT`). In every case keep handlers short: signal a semaphore or submit work, and
avoid blocking network calls inside a handler.

## Verify
- [ ] Pull the cable / turn off the AP: app sees DISCONNECTED, stops sending, reconnects after CONNECTED.
- [ ] Callback registered before interface up, or resend-status called.
- [ ] No sockets opened before the first L4_CONNECTED.

## Checked

Checked 2026-10-26 against Zephyr main on GitHub (`net_mgmt.h`, `net_event.h`, `conn_mgr_monitor.h`, `Kconfig.mgmt`, conn_mgr Kconfig,
`wifi_mgmt.h`/`wifi.h`): `uint64_t` event type, `net_mgmt_init_event_callback()`/`net_mgmt_add_event_callback()`,
`conn_mgr_mon_resend_status()` semantics, `NET_EVENT_L4_*`, `NET_EVENT_IPV4_ADDR_ADD`, `NET_EVENT_IPV4_DHCP_BOUND`, `NET_EVENT_IF_UP/DOWN`,
Wi-Fi events and `NET_REQUEST_WIFI_CONNECT`, `struct wifi_connect_req_params` fields, the one-callback-per-layer rule, the info
fields, `CONFIG_NET_CONNECTION_MANAGER` selecting `NET_MGMT_EVENT_INFO`, and the event-handler execution choice. Fixed: handlers
do not always run in a dedicated thread. Removed the "can deadlock" remark and the reference to older uint32_t event types.

Method: documentation only; no commands were run.
