---
id: computing-software.firmware-embedded-development.zephyr.lwm2m-client
name: lwm2m-client
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-lwm2m, lwm2m-rd-client, lwm2m-engine, ipso-objects, dtls-psk, leshan, zephyr, firmware-embedded-development]
level: sme
status: docs-checked
description: "Connect a Zephyr device to an LwM2M server (Leshan, AVSystem): RD client start, security object with PSK/DTLS, resource paths, IPSO objects, observe, queue mode, and FOTA."
sources:
  - https://docs.zephyrproject.org/latest/connectivity/networking/api/lwm2m.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/net/lwm2m.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/net/lwm2m_path.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/net/lib/lwm2m/Kconfig
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/samples/net/lwm2m_client/src/lwm2m-client.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LwM2M client

LwM2M (OMA SpecWorks) is a CoAP-based device management protocol: objects/instances/resources
(e.g. `3303/0/5700` = temperature sensor value), bootstrap, registration, observe, firmware update.

```
CONFIG_LWM2M=y
CONFIG_LWM2M_DTLS_SUPPORT=y
CONFIG_LWM2M_IPSO_TEMP_SENSOR=y
CONFIG_LWM2M_FIRMWARE_UPDATE_OBJ_SUPPORT=y   # optional FOTA
CONFIG_LWM2M_QUEUE_MODE_ENABLED=y            # for sleepy devices
CONFIG_LWM2M_RD_CLIENT_SUPPORT_BOOTSTRAP=n
```

## Security object and start
```c
#include <zephyr/net/lwm2m.h>

static struct lwm2m_ctx ctx;

static int setup(void)
{
    lwm2m_set_string(&LWM2M_OBJ(0, 0, 0), "coaps://leshan.example.org:5684");   /* server URI */
    lwm2m_set_u8(&LWM2M_OBJ(0, 0, 2), 0);                                        /* mode: PSK */
    lwm2m_set_string(&LWM2M_OBJ(0, 0, 3), "dev-0001");                           /* PSK identity */
    lwm2m_set_opaque(&LWM2M_OBJ(0, 0, 5), psk, sizeof psk);                      /* PSK key */
    lwm2m_set_u16(&LWM2M_OBJ(1, 0, 0), 101);                                     /* short server id */
    lwm2m_set_u32(&LWM2M_OBJ(1, 0, 1), 300);                                     /* lifetime s */
    lwm2m_create_object_inst(&LWM2M_OBJ(3303, 0));
    return 0;
}

static void rd_cb(struct lwm2m_ctx *c, enum lwm2m_rd_client_event ev)
{
    if (ev == LWM2M_RD_CLIENT_EVENT_REGISTRATION_COMPLETE) { /* registered */ }
    if (ev == LWM2M_RD_CLIENT_EVENT_NETWORK_ERROR)         { /* back off, restart */ }
}

void lwm2m_start(void)
{
    setup();
    ctx.tls_tag = LWM2M_TAG;                   /* TLS credential tag where the library stores the DTLS keys */
    lwm2m_rd_client_start(&ctx, "dev-0001", 0 /*flags*/, rd_cb, NULL);
}
```
Current releases use `LWM2M_OBJ()` path structs (`lwm2m_path.h`) with `lwm2m_set_*` / `lwm2m_get_*`.
The security object (id 0) is also named `LWM2M_OBJECT_SECURITY_ID`, and mode 0 is `LWM2M_SECURITY_PSK`.

## Updating values and observe
```c
lwm2m_set_f64(&LWM2M_OBJ(3303, 0, 5700), 21.5);   /* notifies observers per pmin/pmax */
```
The server sets observation attributes (`pmin`, `pmax`, `gt`, `lt`, `st`). Writes from the server
trigger callbacks registered with `lwm2m_register_post_write_callback()`; executes (e.g. reboot
`3/0/4`) with `lwm2m_register_exec_callback()`.

## Queue mode and power
Queue mode lets the device sleep; the server holds requests until the device
sends an update. Tune `CONFIG_LWM2M_QUEUE_MODE_UPTIME` and the registration lifetime
(`CONFIG_LWM2M_ENGINE_DEFAULT_LIFETIME`, `CONFIG_LWM2M_UPDATE_PERIOD`,
`CONFIG_LWM2M_SECONDS_TO_UPDATE_EARLY` control when Update messages go out).
`lwm2m_engine_pause()` suspends the engine (for example when the network is down; it reports
`LWM2M_RD_CLIENT_EVENT_ENGINE_SUSPENDED`) and `lwm2m_engine_resume()` restarts it.

## Firmware update
Object 5 with push (`5/0/0` package write) or pull (`5/0/1` URI). Hook the transfer with the
firmware callbacks in `lwm2m.h` (`lwm2m_firmware_set_write_cb()` and the related update and cancel
callbacks) and write the image to your update slot from there.

## Test server
An Eclipse Leshan demo server for development; never use production PSKs on a public demo server.

## Verify
- [ ] Registration completes; server shows objects 0/1/3/3303.
- [ ] Observed resource notifications arrive respecting pmin/pmax.
- [ ] Recovery from network loss re-registers without reboot.

## Checked

Zephyr v4.4.2 documentation and source (latest release on 2026-10-27), read from the zephyr repository.
Confirmed in lwm2m.h, lwm2m_path.h, the LwM2M doc and the sample client: `LWM2M_OBJ()`, `lwm2m_set_string/u8/u16/u32/opaque/f64`, `lwm2m_create_object_inst`, `lwm2m_rd_client_start(ctx, ep_name, flags, event_cb, observe_cb)` and the event callback type, events REGISTRATION_COMPLETE and NETWORK_ERROR, `ctx.tls_tag`, PSK security object resources 0/2/3/5 with mode 0, short server id at 1/0/0 and lifetime at 1/0/1, `lwm2m_register_post_write_callback`/`exec_callback`, 3303/0/5700 and 3/0/4, pmin/pmax attributes, Kconfig LWM2M, LWM2M_DTLS_SUPPORT, LWM2M_FIRMWARE_UPDATE_OBJ_SUPPORT, LWM2M_QUEUE_MODE_ENABLED, LWM2M_QUEUE_MODE_UPTIME, LWM2M_RD_CLIENT_SUPPORT_BOOTSTRAP, LWM2M_IPSO_TEMP_SENSOR (Kconfig.ipso), the lifetime options.
Wrong claims fixed: there is no `lwm2m_rd_client_pause/resume`; the pause call is `lwm2m_engine_pause()`/`lwm2m_engine_resume()`. Removed the unconfirmed MCUboot/flash_img download claim, the demo-server hostname and the "older releases" string-path remark.

Method: documentation only; no commands were run.
