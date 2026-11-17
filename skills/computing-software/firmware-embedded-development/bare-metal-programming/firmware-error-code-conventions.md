---
id: computing-software.firmware-embedded-development.bare-metal-programming.firmware-error-code-conventions
name: firmware-error-code-conventions
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [error-codes, embedded-c-coding-standard, status-enum, errno-style, error-propagation, firmware-embedded-development]
level: practitioner
status: draft
description: "Design consistent firmware error reporting: one status type, negative errno-style vs enum codes, propagation macros, warn_unused_result, and mapping errors to logs and telemetry."
sources:
  - https://docs.zephyrproject.org/latest/develop/api/terminology.html
  - https://gcc.gnu.org/onlinedocs/gcc/Common-Function-Attributes.html
  - https://barrgroup.com/embedded-systems/books/embedded-c-coding-standard
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Error code conventions

## Pick one convention per codebase
| Style | Example | Used by |
|---|---|---|
| Negative errno, 0 = OK, positive = count | `return -EIO;` `int n = read(...)` | Zephyr, Linux, Mbed, many RTOS APIs |
| Status enum, 0 = OK | `return HAL_TIMEOUT;` | ST HAL (`HAL_StatusTypeDef`), Nordic (`ret_code_t`) |
| bool success + out-param | `bool read(uint8_t *out)` | small libraries; loses the reason |
Negative errno has two advantages: standard names (`-EINVAL`, `-ETIMEDOUT`, `-EBUSY`, `-ENOMEM`,
`-EAGAIN`) everyone recognises, and a function can return a byte count or an error in one `int`.

## Define it once
```c
typedef int fw_err_t;                       /* 0 OK, <0 -errno */
#define FW_TRY(expr) do { fw_err_t _e = (expr); if (_e < 0) return _e; } while (0)

__attribute__((warn_unused_result))
fw_err_t sensor_read(sensor_t *s, int32_t *out_mdegc);
```
`warn_unused_result` (or C23 `[[nodiscard]]`) turns ignored errors into compiler warnings;
`-Werror` makes them build failures. Cast to `(void)` deliberately when ignoring is correct.

## Wrapping vendor codes at the boundary
```c
static fw_err_t hal_to_err(HAL_StatusTypeDef s) {
    switch (s) { case HAL_OK: return 0; case HAL_BUSY: return -EBUSY;
                 case HAL_TIMEOUT: return -ETIMEDOUT; default: return -EIO; }
}
```
Don't let `HAL_StatusTypeDef` leak into application code.

## Context for diagnosis
A bare `-EIO` from five layers down says little. Options:
- Log at the point of detection with module and detail, return the code upward unchanged.
- Keep a per-module "last error detail" (register value, bus address) readable by a CLI command.
- Count errors per type in a telemetry struct (`i2c_nack_count`, `crc_fail_count`): field trends
  matter more than single events.

## Rules of thumb
- Errors for runtime conditions, asserts for bugs (see assert strategy).
- Never return a code the caller can't act on differently; merge them.
- Timeouts are errors with retries at the right layer: drivers report, policy layers retry.
- Document the codes each public function can return in its header comment.

## Verify
- [ ] `-Wunused-result` enabled; no ignored status in the build output.
- [ ] Vendor status types appear only in driver/BSP files (`grep -rn HAL_StatusTypeDef app/`).
