---
id: computing-software.firmware-embedded-development.esp-idf.esp-netif-static-ip
name: esp-netif-static-ip
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-wifi, esp-netif, static-ip, dns-server, dhcp-client, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Configure ESP-IDF network interfaces with esp_netif: default STA/AP netifs, static IPv4 with DNS, hostname, DHCP control and IPv6 addresses."
sources:
  - https://github.com/espressif/esp-idf/blob/master/components/esp_netif/include/esp_netif.h
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/network/esp_netif_programming.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/network/esp_netif.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# esp_netif and static IP

`esp_netif` is the glue between drivers (Wi-Fi, Ethernet, PPP) and lwIP. Every networking call
on an interface goes through an `esp_netif_t *`.

## Default setup
```c
ESP_ERROR_CHECK(esp_netif_init());
ESP_ERROR_CHECK(esp_event_loop_create_default());
esp_netif_t *sta = esp_netif_create_default_wifi_sta();
esp_netif_set_hostname(sta, "sensor-12");     /* before the interface comes up */
```

## Static IPv4
```c
ESP_ERROR_CHECK(esp_netif_dhcpc_stop(sta));    /* ESP_ERR_ESP_NETIF_DHCP_ALREADY_STOPPED is fine */
esp_netif_ip_info_t ip = {0};
ip.ip.addr      = ESP_IP4TOADDR(192, 168, 1, 50);
ip.gw.addr      = ESP_IP4TOADDR(192, 168, 1, 1);
ip.netmask.addr = ESP_IP4TOADDR(255, 255, 255, 0);
ESP_ERROR_CHECK(esp_netif_set_ip_info(sta, &ip));

esp_netif_dns_info_t dns = { .ip.u_addr.ip4.addr = ESP_IP4TOADDR(1, 1, 1, 1), .ip.type = ESP_IPADDR_TYPE_V4 };
ESP_ERROR_CHECK(esp_netif_set_dns_info(sta, ESP_NETIF_DNS_MAIN, &dns));
```
Set the address while the DHCP client is stopped: `esp_netif_set_ip_info` returns
`ESP_ERR_ESP_NETIF_DHCP_NOT_STOPPED` if DHCP is still running. With DHCP stopped nothing
supplies DNS servers, so call `esp_netif_set_dns_info`.

## Reading the address
```c
static void on_ip(void *a, esp_event_base_t b, int32_t id, void *data) {
    ip_event_got_ip_t *e = data;
    ESP_LOGI(TAG, "IP " IPSTR " gw " IPSTR, IP2STR(&e->ip_info.ip), IP2STR(&e->ip_info.gw));
}
esp_event_handler_register(IP_EVENT, IP_EVENT_STA_GOT_IP, on_ip, NULL);
```

## IPv6
Call `esp_netif_create_ip6_linklocal(sta)` in `WIFI_EVENT_STA_CONNECTED`, then handle
`IP_EVENT_GOT_IP6`. Requires `CONFIG_LWIP_IPV6`.

## Several interfaces
With STA + Ethernet, lwIP routes by the default netif: set priority via
`esp_netif_inherent_config_t.route_prio` or `esp_netif_set_default_netif()`.

## Pitfalls
- Static IP chosen inside the DHCP pool causes ARP conflicts; reserve it on the router.

## Verify
- [ ] `ping` from LAN works and DNS lookup (`getaddrinfo`) succeeds with static config.
- [ ] Hostname visible in the router's DHCP client list (DHCP mode).

## Checked
2026-10-26. ESP-IDF master docs, latest release v6.1 (repository head 2026-10-23). Confirmed in esp_netif.h: esp_netif_dhcpc_stop and its ESP_ERR_ESP_NETIF_DHCP_ALREADY_STOPPED error, esp_netif_set_ip_info (DHCP must be stopped), esp_netif_set_dns_info, ESP_NETIF_DNS_MAIN, esp_netif_set_hostname, esp_netif_create_ip6_linklocal, route_prio, esp_netif_set_default_netif; the programming guide points to the static_ip example. Removed unconfirmed claims about double init asserting, ISR use, call-timing and GOT_IP with static addresses.
Method: documentation only; no commands were run.
