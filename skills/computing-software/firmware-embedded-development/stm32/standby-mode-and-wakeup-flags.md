---
id: computing-software.firmware-embedded-development.stm32.standby-mode-and-wakeup-flags
name: standby-mode-and-wakeup-flags
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-low-power, standby-wakeup, pwr-flag-sb, wakeup-pins, sram2-retention, backup-registers, stm32, firmware-embedded-development]
level: practitioner
status: gated
description: "Use STM32 Standby mode: what survives, enabling wake-up pins and RTC wake, detecting a standby wake via the SB flag at boot, and clearing wake flags so it actually sleeps."
sources:
  - https://www.st.com/resource/en/application_note/an4621-stm32l4-and-stm32l4-ultralowpower-features-overview-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0090-stm32f405415-stm32f407417-stm32f427437-and-stm32f429439-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Standby mode and wake-up flags

Standby turns off the core domain: SRAM and registers are lost (except what's listed below),
and wake-up is a **reset**. Current drops to hundreds of nA (L4, with RTC around 0.3-0.5 uA;
check the datasheet). Use it for long sleeps where restart cost is acceptable.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## What survives
- Backup domain: RTC, LSE, backup registers (`RTC->BKPxR`, 32 x 32-bit on L4).
- Optionally SRAM2 on L4/L5/U5: `HAL_PWREx_EnableSRAM2ContentRetention()` (costs a few hundred nA).
- GPIO pull-ups/downs when "apply pull configuration" is enabled
  (`HAL_PWREx_EnablePullUpPullDownConfig()` + `HAL_PWREx_EnableGPIOPullUp/Down`); otherwise all
  pins float in standby, which can turn on external loads.
- IWDG keeps running (unless its standby-freeze option byte is set) and will reset you.

## Entering
```c
void enter_standby(uint32_t seconds)
{
    /* RTC wake-up timer as wake source */
    HAL_RTCEx_DeactivateWakeUpTimer(&hrtc);
    __HAL_RTC_WAKEUPTIMER_CLEAR_FLAG(&hrtc, RTC_FLAG_WUTF);
    HAL_RTCEx_SetWakeUpTimer_IT(&hrtc, seconds - 1, RTC_WAKEUPCLOCK_CK_SPRE_16BITS, 0);

    /* WKUP pin as second source (rising edge on PA0 = WKUP1) */
    HAL_PWR_DisableWakeUpPin(PWR_WAKEUP_PIN1);
    __HAL_PWR_CLEAR_FLAG(PWR_FLAG_WUF1);             /* L4 per-pin flags; F4: PWR_FLAG_WU */
    HAL_PWR_EnableWakeUpPin(PWR_WAKEUP_PIN1_HIGH);

    __HAL_PWR_CLEAR_FLAG(PWR_FLAG_WU);                /* any stale wake flag = instant wake */
    HAL_PWR_EnterSTANDBYMode();                       /* never returns */
}
```
If a wake-up flag is already set when entering, the device wakes immediately and appears to
reset in a loop. Clear flags **after** configuring sources and just before entry.

## Detecting a standby wake at boot
```c
int main(void) {
    HAL_Init();
    bool from_standby = __HAL_PWR_GET_FLAG(PWR_FLAG_SB);
    if (from_standby) {
        __HAL_PWR_CLEAR_FLAG(PWR_FLAG_SB);
        uint32_t why = 0;
        if (__HAL_PWR_GET_FLAG(PWR_FLAG_WUF1)) why |= WAKE_PIN;       /* which pin */
        if (__HAL_RTC_WAKEUPTIMER_GET_FLAG(&hrtc, RTC_FLAG_WUTF)) why |= WAKE_RTC;
        __HAL_PWR_CLEAR_FLAG(PWR_FLAG_WU);
        uint32_t state = HAL_RTCEx_BKUPRead(&hrtc, RTC_BKP_DR1);       /* restore app state */
        ...
    }
```
Read flags before anything clears them. The reset-cause flags in RCC_CSR show a normal reset
pattern for standby wakes; the PWR SB flag is what distinguishes them (see reset-cause-decoding).
Skip slow initialisation (LSE start, RTC init) when waking from standby: the backup domain is
already configured.

## Shutdown mode
L4/L5/U5/G4 also have Shutdown (lower still, tens of nA): no BOR, no SRAM2 retention, no
IWDG; wake via WKUP pins or RTC. Brown-out during shutdown isn't detected, so supply must be clean.

## Verify
- [ ] Current in standby measured with debugger detached (DBGMCU bits cleared by power cycle).
- [ ] Each wake source wakes the device; boot code identifies the source correctly.
- [ ] Pins that control external power stay in their safe state during standby (pull config applied).

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.
