---
id: computing-software.firmware-embedded-development.bootloader-development.entering-bootloader-from-application
name: entering-bootloader-from-application
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [enter-bootloader, bootloader-architecture, magic-word, noinit-flag, rom-bootloader-jump, firmware-embedded-development]
level: practitioner
status: draft
description: "Let a running application request update mode: magic value in no-init RAM or backup register plus reset, jumping to the ROM system bootloader, and protecting against stuck flags."
sources:
  - https://www.st.com/resource/en/application_note/an2606-stm32-microcontroller-system-memory-boot-mode-stmicroelectronics.pdf
  - https://docs.mcuboot.com/serial_recovery.html
  - https://developer.arm.com/documentation/dui0553/latest/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Entering the bootloader from the application

Triggers: a "start update" command over the app's protocol, a USB DFU detach request, a button
combination, or the cloud pushing an update.

## Pattern: flag + reset
```c
/* shared between bootloader and app: same address in both link scripts */
__attribute__((section(".noinit_shared"))) volatile uint32_t g_boot_req;
#define BOOT_REQ_UPDATE 0xB007D0F1u     /* not a plausible random value; avoid 0 and 0xFFFFFFFF */

void app_request_update(void) {
    g_boot_req = BOOT_REQ_UPDATE;
    __DSB();
    NVIC_SystemReset();
}

/* bootloader, very early */
bool update_requested = (g_boot_req == BOOT_REQ_UPDATE);
g_boot_req = 0;                         /* consume it: never loop in update mode */
if (!update_requested && app_valid()) jump_to_app();
run_update_mode();
```
Storage choices:
- **No-init SRAM**: survives software and watchdog resets on most MCUs; lost on power loss; some
  parts with ECC SRAM or SRAM erase-on-reset options (STM32 `SRAM2_RST` option, RDP regression)
  clear it.
- **RTC backup registers**: survive resets and (with VBAT) power loss; need backup domain write
  access (`PWR_CR1.DBP`). Common for this purpose on STM32.
- **Flash flag**: survives everything but wears flash; use for "update pending" that must
  survive power cycles.

## Jumping to the ROM system bootloader (STM32)
Each family documents the system memory address (AN2606), e.g. 0x1FFF0000 for STM32L4:
```c
void jump_to_system_bootloader(void) {
    deinit_before_jump();               /* clocks to reset state, IRQs off, peripherals reset */
    __HAL_SYSCFG_REMAPMEMORY_SYSTEMFLASH();   /* some families need memory remap */
    const uint32_t *vt = (const uint32_t *)0x1FFF0000u;
    __set_MSP(vt[0]);
    ((void (*)(void))vt[1])();
}
```
Do it via the flag + reset path so the jump happens from a clean reset state. Some families
check `BOOT0`/option bytes and won't stay in the ROM bootloader if a valid app exists unless the
jump is done this way; newer parts (with `nBOOT_SEL`, `nSWBOOT0`) can be controlled via option
bytes instead.

## Safety
- Timeout in update mode: if no update arrives within N minutes, boot the app again.
- Authenticate remote "enter bootloader" commands, or an attacker can keep devices offline.
- A physical override (button held at power-on) for when the app is broken and can't send the
  request.

## Verify
- [ ] App command enters update mode once; the next reset boots the app (flag consumed).
- [ ] Random no-init RAM content after power-on never triggers update mode.
