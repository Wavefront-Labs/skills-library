---
id: computing-software.firmware-embedded-development.bootloader-development.lwm2m-firmware-update-object
name: lwm2m-firmware-update-object
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [lwm2m-firmware, firmware-transport, object-5, fota-state-machine, push-pull-update, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Implement OMA LwM2M Firmware Update (Object 5): resources, the State/Update Result state machine, push vs pull delivery, and integrating with the bootloader swap and confirm."
sources:
  - https://raw.githubusercontent.com/OpenMobileAlliance/lwm2m-registry/prod/5.xml
  - https://raw.githubusercontent.com/zephyrproject-rtos/zephyr/main/include/zephyr/net/lwm2m.h
  - https://raw.githubusercontent.com/zephyrproject-rtos/zephyr/main/include/zephyr/dfu/mcuboot.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LwM2M firmware update object

LwM2M device management servers update devices via **Object 5 (Firmware Update)**; the OMA
registry lists object version 1.2 (single instance, optional).

## Resources
| ID | Name | Use |
|---|---|---|
| 5/0/0 | Package | server **writes** the image (push); clients must support CoAP block-wise transfer |
| 5/0/1 | Package URI | server writes a URI (RFC 3986); device downloads itself (pull) at the next practical opportunity |
| 5/0/2 | Update | server **executes** to start installing; only executable when State is Downloaded |
| 5/0/3 | State | 0 Idle, 1 Downloading, 2 Downloaded, 3 Updating |
| 5/0/5 | Update Result | 0 initial, 1 success, 2 not enough flash, 3 out of RAM, 4 connection lost, 5 integrity check failed, 6 unsupported package type, 7 invalid URI, 8 update failed, 9 unsupported protocol, 10 cancelled, 11 deferred |
| 5/0/6, 5/0/7 | PkgName, PkgVersion | reported after install |
| 5/0/8 | Firmware Update Protocol Support | 0 CoAP (default), 1 CoAPS, 2 HTTP 1.1, 3 HTTPS 1.1, 4 CoAP over TCP, 5 CoAP over TLS |
| 5/0/9 | Firmware Update Delivery Method | 0 pull only, 1 push only, 2 both |
| 5/0/10 | Cancel | optional; execute before installation starts, sets Update Result 10 and State 0 |

## State machine (device side)
```
Idle --(write Package / Package URI)--> Downloading --(complete + verified)--> Downloaded
Downloaded --(execute Update)--> Updating --(reboot into new image, self-test, confirm)--> Idle, Result=1
error --> Idle with Result 2..9 (a failed Update may return to Downloaded or Idle, depending on the reason)
writing an empty string to Package URI (or NULL to Package) resets: State Idle, Update Result 0
```
Servers observe State and Update Result; set them accurately and at each transition, or the
server's campaign hangs.

## Integration with the bootloader
- During Downloading, write into the inactive slot (MCUboot secondary) and verify the signature
  before reporting Downloaded.
- On Update execute: mark the image for test (`boot_request_upgrade(BOOT_UPGRADE_TEST)`), reply to
  the server, then reboot.
- After reboot the new image re-registers, runs self-tests, confirms
  (`boot_write_img_confirmed()`), and sets Update Result = 1 with the new PkgVersion. If it can't
  confirm, the next reset reverts and the old image reports Result = 8.
- Persist State/Result across the reboot.

## Zephyr
`CONFIG_LWM2M_FIRMWARE_UPDATE_OBJ_SUPPORT`, `CONFIG_LWM2M_FIRMWARE_UPDATE_PULL_SUPPORT`; register
callbacks with `lwm2m_firmware_set_write_cb()` (receive blocks), `lwm2m_firmware_set_update_cb()`
(execute).

## Verify
- [ ] Against a test LwM2M server: push and pull updates complete; State/Result transitions match the spec.
- [ ] Corrupted package gives Update Result 5; unconfirmed image after reboot gives Result 8 and the old version.

## Checked
2026-10-31. Confirmed against the OMA LwM2M registry definition of Object 5 (resource IDs, operations, State 0..3, Update Result 0..11, protocol support 0..5, delivery method 0..2, Cancel, reset by empty Package URI) and the Zephyr headers (`lwm2m_firmware_set_write_cb`, `lwm2m_firmware_set_update_cb`, `boot_request_upgrade`, `boot_write_img_confirmed`, `BOOT_UPGRADE_TEST`) and Kconfig (`CONFIG_LWM2M_FIRMWARE_UPDATE_OBJ_SUPPORT`, `..._PULL_SUPPORT`). Corrected Update Result range, the error/cancel behaviour and the delivery method wording; removed server product names and the nRF Connect SDK remark. Using Update Result 8 for an unconfirmed image is a design choice, not a spec statement.
Method: documentation only; no commands were run.
