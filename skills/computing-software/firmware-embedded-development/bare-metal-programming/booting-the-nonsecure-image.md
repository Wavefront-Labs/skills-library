---
id: computing-software.firmware-embedded-development.bare-metal-programming.booting-the-nonsecure-image
name: booting-the-nonsecure-image
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [ns-image-boot, trustzone-m, vtor-ns, msp-ns, blxns, secure-boot-handoff, firmware-embedded-development]
level: advanced
status: gated
description: "Hand over from the secure image to the non-secure application on ARMv8-M: set VTOR_NS and MSP_NS, configure SAU/NVIC targeting, then branch with BLXNS to the NS reset handler."
sources:
  - https://developer.arm.com/documentation/100690/latest/
  - https://arm-software.github.io/CMSIS_6/latest/Core/using_TrustZone_pg.html
  - https://github.com/ARM-software/CMSIS_6/blob/main/CMSIS/Core/Include/m-profile/cmsis_gcc_m.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Booting the non-secure image

The core always resets into the **secure** state. Secure firmware configures security
attribution, then starts the NS application.

## Sequence (secure main)
```c
#define NS_VTOR 0x08040000u                       /* NS alias of the NS image start */
typedef void (*ns_fn_t)(void) __attribute__((cmse_nonsecure_call));

int main(void) {
    SystemInit();                                  /* secure clocks */
    TZ_SAU_Setup();                                /* partition_<device>.h: SAU regions, NSC, NVIC ITNS, SCB->NSACR */
    vendor_security_config();                      /* vendor: peripherals and SRAM blocks for NS */
    gpio_secure_config();                          /* release pins the NS app uses */

    SCB_NS->VTOR = NS_VTOR;                        /* NS vector table */
    __TZ_set_MSP_NS(*(uint32_t *)NS_VTOR);         /* NS initial stack pointer */
    ns_fn_t ns_reset = (ns_fn_t)cmse_nsfptr_create(*(uint32_t *)(NS_VTOR + 4));
    ns_reset();                                    /* BLXNS; does not return */
    for (;;) {}
}
```

## Things the secure side must set first
- **SAU**: NS flash and RAM regions plus the NSC region for veneers; `SAU->CTRL = ENABLE`. With
  the SAU disabled and `ALLNS=0`, everything is Secure and the NS jump faults immediately.
  (gated: unconfirmed, source is paywalled or blocked)
- **NVIC_ITNS**: route the interrupts the NS app uses to the NS world (bit = 1; CMSIS `NVIC_SetTargetState`).
  Otherwise the IRQ stays with the Secure world.
- **SCB->NSACR**: grant NS access to coprocessors, at least CP10/CP11 for the FPU
  (`SCB->NSACR |= (3U << 10)`), or NS float code raises NOCP UsageFault.
- **AIRCR.PRIS / BFHFNMINS**: PRIS makes Secure interrupts always rank higher than Non-secure ones;
  BFHFNMINS selects the security state that handles BusFault, HardFault and NMI.
- **Secure fault handlers** and SecureFault enabled before the jump.

## NS image layout
The NS image is a normal Cortex-M image with its vector table at the NS start; its startup code
sets nothing security-related. It calls secure services through veneers in the NSC region, linked
with the secure build's CMSE import library (`--out-implib`/`--cmse-implib`).

## Debugging
- Debuggers need secure debug enabled to step the handover; debug authentication (`DCB->DAUTHCTRL`, vendor
  settings) can restrict a probe to Non-secure state.
- Typical first-boot faults: SecureFault AUVIOL at NS reset handler address (SAU region missing), an NS
  interrupt not delivered (ITNS not set), NOCP (NSACR).

## Verify
- [ ] NS app's first instruction executes in NS state (`__TZ_get_CONTROL_NS` readable; IPSR/state in debugger shows Non-secure).
- [ ] NS interrupts and FPU work; secure services callable through veneers.

## Checked
2026-11-01. Confirmed in the CMSIS-Core TrustZone page and CMSIS headers `core_cm33.h` and `cmsis_gcc_m.h`: reset
into Secure state, `TZ_SAU_Setup` from `partition_<device>.h`, `SCB_NS`, `__TZ_set_MSP_NS`, `NVIC->ITNS`,
`SCB->NSACR` CP10/CP11, AIRCR PRIS/BFHFNMINS, SFSR AUVIOL, `DAUTHCTRL`, SG instruction for entry. Removed: the
STM32 GTZC function name and source, `SPNIDEN`/`SPIDEN` wording, the claim that NS NVIC writes are ignored.
Gated: ALLNS semantics. `cmse_nonsecure_call`, `--cmse-implib` and BLXNS behaviour are compiler/architecture
behaviour the unreadable Arm and GCC attribute pages would confirm.
Method: documentation only; no commands were run.
