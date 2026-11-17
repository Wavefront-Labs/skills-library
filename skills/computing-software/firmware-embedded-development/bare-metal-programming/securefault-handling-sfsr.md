---
id: computing-software.firmware-embedded-development.bare-metal-programming.securefault-handling-sfsr
name: securefault-handling-sfsr
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [securefault, trustzone-m, sfsr, sfar, invep, fault-triage, firmware-embedded-development]
level: advanced
status: draft
description: "Enable and decode ARMv8-M SecureFault: SFSR bits (INVEP, INVIS, INVER, AUVIOL, INVTRAN, LSPERR, LSERR), SFAR, and the usual causes in TrustZone firmware."
sources:
  - https://developer.arm.com/documentation/100235/latest/
  - https://developer.arm.com/documentation/ddi0553/latest/
  - https://developer.arm.com/documentation/100690/latest/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SecureFault handling (SFSR and SFAR)

SecureFault (exception 7) exists only with the Security Extension and is always handled in the
secure state. Enable it, otherwise it escalates to the secure HardFault.

```c
/* secure world, early init */
SCB->SHCSR |= SCB_SHCSR_SECUREFAULTENA_Msk;
NVIC_SetPriority(SecureFault_IRQn, 0);
```

## SFSR (0xE000EDE4) bits
| Bit | Name | Meaning | Typical cause |
|---|---|---|---|
| 0 | INVEP | invalid entry point | NS code called secure code not at an SG instruction in an NSC region (missing veneer, NSC region wrong in SAU) |
| 1 | INVIS | invalid integrity signature on exception return | stack corruption or wrong EXC_RETURN manipulation |
| 2 | INVER | invalid exception return | EXC_RETURN with wrong security bits |
| 3 | AUVIOL | attribution unit violation | NS access to a secure address (SAU/IDAU) |
| 4 | INVTRAN | invalid transition | branch from secure to NS without BXNS/BLXNS (e.g. calling an NS callback directly) |
| 5 | LSPERR | lazy state preservation error | FP lazy stacking to an address that violates SAU |
| 6 | SFARVALID | SFAR holds the faulting address | |
| 7 | LSERR | lazy state error | |
SFAR (0xE000EDE8) holds the address for AUVIOL and similar.

## Handler
```c
void SecureFault_Handler(void) {
    uint32_t sfsr = SAU->SFSR, sfar = SAU->SFAR;   /* CMSIS: in SAU_Type */
    uint32_t *frame;
    /* faulting context may be NS: check EXC_RETURN.S (bit 6); NS stack via __TZ_get_MSP_NS()/__TZ_get_PSP_NS() */
    record_fault(sfsr, (sfsr & SAU_SFSR_SFARVALID_Msk) ? sfar : 0);
    SAU->SFSR = sfsr;                               /* write-1-to-clear */
    NVIC_SystemReset();                             /* or kill the NS world and continue secure services */
}
```

## Triage by symptom
- **INVEP when calling a secure API**: the function lacks `__attribute__((cmse_nonsecure_entry))`,
  the veneer isn't in the NSC region, or the NS image was built against a stale `_CMSE_import.o`
  (veneer addresses moved). Rebuild NS with the current import library.
- **AUVIOL from NS code**: NS app touching a secure peripheral/RAM alias, or a DMA configured by
  NS code pointing at secure memory (also check GTZC illegal access flags).
- **INVTRAN**: secure code calling a function pointer received from NS code without
  `cmse_nsfptr_create` / `__attribute__((cmse_nonsecure_call))`.
- **LSPERR**: FPU context stacking for NS state into memory the SAU marks secure (NS stack placed
  in secure RAM).

## Verify
- [ ] SHCSR.SECUREFAULTENA set; a deliberate NS read of a secure address lands in SecureFault with AUVIOL and the right SFAR.
- [ ] Fault record survives reset for field triage.
