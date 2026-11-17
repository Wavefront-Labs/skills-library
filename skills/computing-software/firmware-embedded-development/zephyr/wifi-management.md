---
id: computing-software.firmware-embedded-development.zephyr.wifi-management
name: wifi-management
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-wifi, net-request-wifi-connect, wifi-mgmt, wifi-scan, wifi-credentials, wpa-supplicant, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Connect Zephyr devices to Wi-Fi with the wifi_mgmt API: scan, connect with security params, connection events, stored credentials, power save, and the wifi shell."
sources:
  - https://docs.zephyrproject.org/latest/connectivity/networking/api/wifi.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/net/wifi_mgmt.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/net/wifi_credentials.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/net/net_mgmt.h
  - https://docs.zephyrproject.org/latest/releases/migration-guide-4.2.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wi-Fi management

```
CONFIG_WIFI=y
CONFIG_NET_L2_WIFI_MGMT=y
CONFIG_NET_MGMT_EVENT=y
CONFIG_NET_DHCPV4=y
CONFIG_WIFI_NM_WPA_SUPPLICANT=y   # hostap-based supplicant (modules/hostap), for drivers that use it
CONFIG_NET_L2_WIFI_SHELL=y
```

## Connect
```c
#include <zephyr/net/wifi_mgmt.h>
#include <zephyr/net/net_event.h>

static struct net_mgmt_event_callback wifi_cb, ip_cb;
static K_SEM_DEFINE(ip_ready, 0, 1);

static void wifi_evt(struct net_mgmt_event_callback *cb, uint64_t ev, struct net_if *iface)
{
    const struct wifi_status *st = cb->info;
    if (ev == NET_EVENT_WIFI_CONNECT_RESULT)    printk("connect: %d\n", st->status);
    if (ev == NET_EVENT_WIFI_DISCONNECT_RESULT) printk("disconnected: %d\n", st->status);
}
static void ip_evt(struct net_mgmt_event_callback *cb, uint64_t ev, struct net_if *iface)
{
    if (ev == NET_EVENT_IPV4_ADDR_ADD) k_sem_give(&ip_ready);
}

int wifi_up(const char *ssid, const char *psk)
{
    struct net_if *iface = net_if_get_first_wifi();   /* or net_if_get_default() */
    net_mgmt_init_event_callback(&wifi_cb, wifi_evt,
        NET_EVENT_WIFI_CONNECT_RESULT | NET_EVENT_WIFI_DISCONNECT_RESULT);
    net_mgmt_add_event_callback(&wifi_cb);
    net_mgmt_init_event_callback(&ip_cb, ip_evt, NET_EVENT_IPV4_ADDR_ADD);
    net_mgmt_add_event_callback(&ip_cb);

    struct wifi_connect_req_params p = {
        .ssid = (const uint8_t *)ssid, .ssid_length = strlen(ssid),
        .psk  = (const uint8_t *)psk,  .psk_length  = strlen(psk),
        .security = WIFI_SECURITY_TYPE_PSK,          /* SAE for WPA3, NONE for open */
        .band = WIFI_FREQ_BAND_UNKNOWN,              /* any */
        .channel = WIFI_CHANNEL_ANY,
        .mfp = WIFI_MFP_OPTIONAL,
        .timeout = SYS_FOREVER_MS,
    };
    int rc = net_mgmt(NET_REQUEST_WIFI_CONNECT, iface, &p, sizeof p);
    if (rc) return rc;                                /* request rejected; result comes as event */
    return k_sem_take(&ip_ready, K_SECONDS(30));
}
```
The request returning 0 only means "started"; success is the `CONNECT_RESULT` event with status 0,
then DHCP gives an address.

## Scan
`net_mgmt(NET_REQUEST_WIFI_SCAN, iface, NULL, 0)` with `NET_EVENT_WIFI_SCAN_RESULT` (one per AP,
`struct wifi_scan_result`: ssid, rssi, channel, security) and `NET_EVENT_WIFI_SCAN_DONE`.

## Stored credentials and auto-connect
```
CONFIG_WIFI_CREDENTIALS=y
CONFIG_WIFI_CREDENTIALS_BACKEND_SETTINGS=y
CONFIG_WIFI_CREDENTIALS_CONNECT_STORED=y   # newer releases: connect to stored networks at boot
```
`wifi_credentials_set_personal(ssid, len, WIFI_SECURITY_TYPE_PSK, NULL, 0, psk, psk_len, 0, 0, 0)`.
Or use `conn_mgr` connectivity bindings (`conn_mgr_all_if_connect`) for a generic flow.

## Power save
`NET_REQUEST_WIFI_PS` with `struct wifi_ps_params` (`enabled`, `listen_interval`, `wakeup_mode`,
`mode`, `timeout_ms`, `exit_strategy`); TWT has its own request and parameter structs. Check `NET_REQUEST_WIFI_IFACE_STATUS` for RSSI and link info.

## Shell
```
uart:~$ wifi scan
uart:~$ wifi connect -s MySSID -p secret -k 1
uart:~$ wifi status
```
(Argument syntax changed across releases; `wifi connect --help`.)

## Verify
- [ ] App waits for IP-address event, not just the connect request return.
- [ ] Reconnects after AP reboot (handle `DISCONNECT_RESULT` with backoff).
- [ ] Credentials never logged.

## Checked

Zephyr v4.4.2 documentation and source (latest release on 2026-10-27), read from the zephyr repository.
Confirmed in the headers, Kconfig files and shell source: NET_REQUEST_WIFI_CONNECT/SCAN/PS/IFACE_STATUS; events CONNECT_RESULT, DISCONNECT_RESULT, SCAN_RESULT, SCAN_DONE; `struct wifi_connect_req_params` fields (ssid, ssid_length, psk, psk_length, sae_password, band, channel, security, mfp, timeout); WIFI_SECURITY_TYPE_NONE/PSK/SAE, WIFI_FREQ_BAND_UNKNOWN, WIFI_CHANNEL_ANY, WIFI_MFP_OPTIONAL; `net_if_get_first_wifi()`; `wifi_credentials_set_personal()` signature (10 arguments); CONFIG_NET_L2_WIFI_MGMT, CONFIG_NET_L2_WIFI_SHELL, CONFIG_WIFI_NM_WPA_SUPPLICANT, CONFIG_WIFI_CREDENTIALS, ..._BACKEND_SETTINGS and ..._CONNECT_STORED; `conn_mgr_all_if_connect()`; the shell `wifi connect` options -s, -p and -k.
Stale claims fixed: `net_mgmt` event handlers take a `uint64_t` event argument in current releases (migration guide 4.2); `wifi_ps_params` has `enabled`, not `enable`. Removed the unconfirmed list of drivers that need the supplicant.

Method: documentation only; no commands were run.
