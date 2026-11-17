---
id: computing-software.firmware-embedded-development.esp-idf.mdns-service-discovery
name: mdns-service-discovery
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-networking, mdns, dns-sd, local-hostname, service-advertisement, espressif-mdns, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Make an ESP32 reachable as name.local and advertise services with the espressif/mdns component: hostname, DNS-SD services with TXT records, queries, and Wi-Fi power-save caveats."
sources:
  - https://github.com/espressif/esp-protocols/blob/master/components/mdns/include/mdns.h
  - https://github.com/espressif/esp-protocols/tree/master/components/mdns
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/protocols/mdns.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/wifi-driver/wifi-performance-and-power-save.rst
  - https://www.rfc-editor.org/rfc/rfc6763
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mDNS and service discovery

mDNS lets clients on the LAN find `acme-1a2b.local` without DNS servers, and DNS-SD lets apps
browse for `_http._tcp` services. Since ESP-IDF 5.0 it lives in the `espressif/mdns` component.

## Add and advertise
```bash
idf.py add-dependency "espressif/mdns"
```
```c
#include "mdns.h"

void mdns_start(const char *id)
{
    ESP_ERROR_CHECK(mdns_init());
    char host[32];
    snprintf(host, sizeof host, "acme-%s", id);          /* unique per device */
    mdns_hostname_set(host);                              /* -> acme-1a2b.local */
    mdns_instance_name_set("ACME Sensor");

    mdns_txt_item_t txt[] = {
        { "fw", FW_VERSION },
        { "model", "TS-100" },
        { "path", "/" },
    };
    mdns_service_add("ACME Sensor Web", "_http", "_tcp", 80, txt, 3);
    mdns_service_add(NULL, "_acme", "_tcp", 5000, NULL, 0);   /* custom app service */
}
```
`mdns_init()` registers an event handler (it returns `ESP_ERR_INVALID_STATE` if that fails).
Update TXT data at run time with `mdns_service_txt_item_set("_http", "_tcp", "fw", ver)`.

## Query (device as client)
```c
mdns_result_t *res = NULL;
if (mdns_query_ptr("_acme", "_tcp", 3000, 20, &res) == ESP_OK) {
    for (mdns_result_t *r = res; r; r = r->next) {
        /* r->instance_name, r->hostname, r->port, r->addr list, r->txt */
    }
    mdns_query_results_free(res);
}
esp_ip4_addr_t ip;
mdns_query_a("printer", 2000, &ip);           /* resolve printer.local */
```
Queries take a timeout in milliseconds and return when they complete; run them in a worker task, not the event loop.

## Naming
- Hostnames must be unique on the LAN. Derive from the MAC or serial; a fixed name for every
  device leads to conflicts.
- Service type and protocol are passed as separate arguments (`"_http"`, `"_tcp"`); host names
  passed to the API must not include the domain, because mDNS uses `.local`.

## Reliability caveats
- Wi-Fi power save: with `WIFI_PS_MIN_MODEM` (default) broadcast data is not lost because the
  station wakes at every DTIM; with `WIFI_PS_MAX_MODEM` broadcast data may be lost, so
  multicast queries can be missed. Test discovery in the chosen power-save mode.
- mDNS is unauthenticated. Don't trust discovery results for security decisions.

## Verify
- [ ] `ping acme-1a2b.local` works from a client that supports mDNS, and a service browser lists the service with its TXT records.
- [ ] Two devices on the same LAN have different hostnames.
- [ ] Discovery tested on the customer-typical router with the chosen power-save mode.

## Checked
2026-10-26. ESP-IDF master docs, latest release v6.1 (repository head 2026-10-23). Checked against esp-protocols mdns.h (repository head 2026-10-23): mdns_init, mdns_hostname_set, mdns_instance_name_set, mdns_service_add(instance, type, proto, port, txt[], n), mdns_service_txt_item_set(type, proto, key, value), mdns_query_ptr(type, proto, timeout, max_results, &results), mdns_query_a(host, timeout, &addr), mdns_query_results_free, mdns_txt_item_t; the IDF docs page confirms the component moved out of ESP-IDF in v5.0 and is added with `idf.py add-dependency espressif/mdns`. Wrong: the power-save note (MIN_MODEM does not lose broadcast; MAX_MODEM can). Removed unconfirmed claims: service-name length limit, client-OS resolver support, router multicast behaviour and automatic hostname renaming.
Method: documentation only; no commands were run.
