---
id: computing-software.firmware-embedded-development.bare-metal-programming.board-support-package-layering
name: board-support-package-layering
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [board-support-package, superloop, firmware-layering, bsp, hardware-variants, firmware-embedded-development]
level: advanced
status: draft
description: "Structure firmware as app / services / BSP / MCU drivers so one codebase supports several board revisions and MCUs, with pin maps and board quirks kept in the BSP."
sources:
  - https://docs.zephyrproject.org/latest/hardware/porting/board_porting.html
  - https://embeddedartistry.com/fieldmanual-terms/board-support-package/
  - https://www.state-machine.com/doc/AN_OOP_in_C.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Board support package layering

## Layers
```
app/            product logic: state machines, protocols. No #include of vendor headers.
services/       logging, storage, comms stacks, timers. Hardware-independent.
bsp/<board>/    this PCB: pin assignments, which UART is the console, sensor I2C address,
                LED polarity, power-rail enable GPIOs, board revision quirks.
drivers/        MCU peripheral drivers (or the vendor HAL/LL) and external chip drivers.
cmsis/ vendor/  device headers, startup, system file.
```
Rule: dependencies point down only. `app` calls `bsp_led_set(BSP_LED_STATUS, true)`, never
`HAL_GPIO_WritePin(GPIOB, GPIO_PIN_7, ...)`.

## BSP interface
```c
/* bsp.h: same for every board */
void bsp_init(void);                    /* clocks, pins, power rails */
void bsp_led_set(bsp_led_t led, bool on);
const struct uart_dev *bsp_console(void);
const struct i2c_dev *bsp_sensor_bus(void);
uint8_t bsp_board_revision(void);       /* read strap resistors / ADC divider / OTP */
```
Each board directory implements it. CMake picks one: `-DBOARD=sensor_v3`,
`add_subdirectory(bsp/${BOARD})`.

## Board revisions
- Read the revision at runtime (strap GPIOs, an ADC voltage divider, or a value programmed in
  OTP/flash at manufacturing) and branch inside the BSP: `if (rev >= 3) { led_active_low = false; }`.
- Compile-time board variants for different MCUs or pinouts; runtime revision for small PCB changes.
  Mixing them avoids an explosion of build targets.

## What belongs where
| Item | Layer |
|---|---|
| "Sensor reset is on PA4, active low" | BSP |
| "BME280 register map and compensation maths" | driver (external chip) |
| "Read temperature every 10 s and publish" | app/service |
| "Errata workaround for this MCU's I2C" | MCU driver |
| "Rev B board needs a 2 ms delay after rail enable" | BSP |

## Testing benefit
A `bsp/host` implementation (stubs or a simulator) lets services and app compile and run unit
tests on the PC. If the app does not build for `host`, a vendor header has leaked upward.

## Verify
- [ ] `grep -rn "stm32\|HAL_\|nrf_" app/ services/` returns nothing.
- [ ] Building for two boards changes only the BSP and the linker script.
- [ ] Host build of app + services links against `bsp/host`.
