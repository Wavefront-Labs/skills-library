---
id: computing-software.firmware-embedded-development.esp-idf.sntp-time-sync
name: sntp-time-sync
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-networking, sntp, esp-netif-sntp, timezone-tz, wall-clock-time, dhcp-ntp-server, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Get correct wall-clock time on ESP32 with esp_netif_sntp: waiting for first sync, time zones with POSIX TZ strings, sync intervals, smooth adjustment and behaviour across sleep."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/system/system_time.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/network/esp_netif_programming.rst
  - https://github.com/espressif/esp-idf/blob/master/components/esp_netif/include/esp_netif_sntp.h
  - https://github.com/espressif/esp-idf/blob/master/components/lwip/Kconfig
  - https://github.com/espressif/esp-idf/blob/master/examples/protocols/sntp/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SNTP time sync

## Start and wait
```c
#include "esp_netif_sntp.h"
#include <time.h>

esp_err_t time_sync(void)
{
    esp_sntp_config_t cfg = ESP_NETIF_SNTP_DEFAULT_CONFIG("pool.ntp.org");
    /* cfg.server_from_dhcp = true; to accept NTP servers offered by DHCP */
    esp_netif_sntp_init(&cfg);
    esp_err_t r = esp_netif_sntp_sync_wait(pdMS_TO_TICKS(15000));   /* ESP_ERR_TIMEOUT if not yet */
    return r;
}
```
Call after the network has an IP. Multiple servers: `ESP_NETIF_SNTP_DEFAULT_CONFIG_MULTIPLE(2,
ESP_SNTP_SERVER_LIST("time.acme.example", "pool.ntp.org"))` (limit from
`CONFIG_LWIP_SNTP_MAX_SERVERS`). Notification of each sync: `cfg.sync_cb`.

(Older code uses `esp_sntp_setoperatingmode`/`esp_sntp_init` directly; the `esp_netif_sntp`
wrapper is the current API.)

## Time zone
The system clock is UTC. Local time comes from the POSIX `TZ` variable:
```c
setenv("TZ", "CET-1CEST,M3.5.0,M10.5.0/3", 1);     /* Central Europe with DST rules */
tzset();
time_t now; struct tm lt;
time(&now);
localtime_r(&now, &lt);
strftime(buf, sizeof buf, "%Y-%m-%d %H:%M:%S %Z", &lt);
```
Other examples: `"EST5EDT,M3.2.0,M11.1.0"` (US Eastern), `"AEST-10AEDT,M10.1.0,M4.1.0/3"`
(Sydney), `"UTC0"`. Store the user's POSIX TZ string, not an
Olson name, or map names to strings on your backend. Note the inverted sign: `CET-1` is UTC+1.

## Before sync
`time()` starts at 1970 (or the last value preserved across deep sleep). Don't timestamp
records, check certificate dates or schedule events until synced:
```c
bool time_valid(void) { return time(NULL) > 1700000000; }   /* after Nov 2023 */
```
Or track the sync callback.

## Ongoing sync
- Default resync interval: `CONFIG_LWIP_SNTP_UPDATE_DELAY` (default 3600000 ms, minimum 15000 ms).
- `cfg.smooth_sync = true` selects smooth updates instead of a jump (`esp_netif_sntp_sync_wait`
  returns `ESP_ERR_NOT_FINISHED` while a smooth update is in progress). Better: measure intervals
  with `esp_timer_get_time()` (monotonic) and use wall time only for display/timestamps.

## Sleep and power loss
- Sleep and resets: the RTC timer keeps time across sleep modes and resets, except power-on
  resets. Its accuracy depends on the RTC clock source (`CONFIG_RTC_CLK_SRC`): the internal RC
  oscillator is affected by temperature, an external 32 kHz crystal is more stable. Resync
  occasionally after wake.
- Power-on reset: time is lost. Products needing time at boot without network need an external RTC.

## Verify
- [ ] Local time correct across a DST transition (test by setting time manually around the switch).
- [ ] Records created before first sync are flagged or re-timestamped.
- [ ] Drift after 24 h of deep-sleep cycles measured and acceptable.

## Checked
2026-10-26. ESP-IDF master docs, latest release v6.1 (repository head 2026-10-23). Confirmed: esp_netif_sntp_init / sync_wait (ESP_ERR_TIMEOUT, ESP_ERR_NOT_FINISHED), ESP_NETIF_SNTP_DEFAULT_CONFIG(_MULTIPLE), ESP_SNTP_SERVER_LIST, server_from_dhcp, smooth_sync, sync_cb, CONFIG_LWIP_SNTP_UPDATE_DELAY default 3600000 (min 15000), CONFIG_LWIP_SNTP_MAX_SERVERS, RTC timer behaviour and clock sources (system time page). The epoch threshold 1700000000 is 2023-11-14 (computed). Removed unconfirmed ppm drift figure, DHCP option number and the no-tz-database claim.
Method: documentation only; no commands were run.
