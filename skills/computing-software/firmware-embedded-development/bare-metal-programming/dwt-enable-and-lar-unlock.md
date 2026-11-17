---
id: computing-software.firmware-embedded-development.bare-metal-programming.dwt-enable-and-lar-unlock
name: dwt-enable-and-lar-unlock
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [dwt-lar-unlock, dwt-cyccnt, demcr-trcena, coresight-lock, cortex-m7, firmware-embedded-development]
level: advanced
status: draft
description: "Enable the DWT cycle counter without a debugger: DEMCR.TRCENA, the Cortex-M7 software lock (LAR 0xC5ACCE55), and checking NOCYCCNT on parts that lack it."
sources:
  - https://developer.arm.com/documentation/ddi0403/latest/
  - https://developer.arm.com/documentation/ddi0489/latest/
  - https://developer.arm.com/documentation/ihi0029/latest/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Unlocking DWT on Cortex-M7 (LAR)

**Symptom:** `DWT->CYCCNT` stays 0 when running standalone but works under the debugger.
Two reasons: the trace block is not enabled (the debugger enables it for you), or on Cortex-M7
the DWT has a CoreSight software lock that ignores writes until unlocked.

## Enable sequence
```c
static bool cyccnt_init(void) {
    CoreDebug->DEMCR |= CoreDebug_DEMCR_TRCENA_Msk;     /* DCB->DEMCR on CMSIS 6 */
#if (__CORTEX_M == 7)
    DWT->LAR = 0xC5ACCE55;                              /* CoreSight key; ignored on cores without a lock */
#endif
    if (DWT->CTRL & DWT_CTRL_NOCYCCNT_Msk) return false;  /* no cycle counter implemented */
    DWT->CYCCNT = 0;
    DWT->CTRL |= DWT_CTRL_CYCCNTENA_Msk;
    return DWT->CYCCNT != 0 || (__NOP(), __NOP(), DWT->CYCCNT != 0);
}
```
- `LAR` is at `0xE0001FB0`; `LSR` (`0xE0001FB4`) reads bit 1 = locked, bit 0 = lock implemented.
  Older CMSIS headers lack `DWT->LAR`; write `*(volatile uint32_t *)0xE0001FB0 = 0xC5ACCE55`.
- The same lock exists on ITM (`ITM->LAR`) for software-driven SWO output on M7.

## Availability
- Not on ARMv6-M (Cortex-M0/M0+) or ARMv8-M Baseline (M23): no DWT cycle counter. Use SysTick or
  a timer.
- ARMv8-M Mainline (M33/M55): CYCCNT is optional; check `NOCYCCNT`. With TrustZone, non-secure
  access depends on `DEMCR.SDME` / secure debug configuration and `DAUTHCTRL`.
- Some vendor parts gate the trace clock: STM32H7 needs `DBGMCU->CR |= DBGMCU_CR_DBG_TRACECKEN`
  for some trace features (not usually for CYCCNT).

## Gotchas
- CYCCNT stops in sleep (WFI) since the core clock stops: cycle counts across sleep are wrong.
- It is 32-bit: wraps every `2^32 / f_cpu` seconds (8.9 s at 480 MHz).
- A debugger session (attach/detach) may reset TRCENA; re-run the init after debugger reset.
- Writing TRCENA also enables ITM/DWT power: small current increase in low-power builds.

## Verify
- [ ] Standalone boot (no debugger): two CYCCNT reads around `delay_us(1000)` differ by about `f_cpu/1000`.
- [ ] `DWT->LSR` reads 0 (unlocked) after the key write on M7.
