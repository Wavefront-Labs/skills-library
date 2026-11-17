---
id: computing-software.firmware-embedded-development.zephyr.pinctrl-pin-control
name: pinctrl-pin-control
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [devicetree, pinctrl, pinctrl-0, pinctrl-names, pinctrl-apply-state, pin-muxing, sleep-pin-state, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Route peripheral signals to pins in Zephyr with pinctrl: pinctrl-0/pinctrl-names in overlays, vendor pin nodes (STM32, nRF), sleep states, and driver-side apply."
sources:
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/doc/hardware/pinctrl/index.rst
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/drivers/pinctrl.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/dts/bindings/pinctrl/nordic,nrf-pinctrl.yaml
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/dts/bindings/pinctrl/st,stm32-pinctrl.yaml
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/dts/bindings/pinctrl/pincfg-node.yaml
  - https://github.com/zephyrproject-rtos/hal_stm32/tree/main/dts/st
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pin control (pinctrl)

Pin muxing is described in devicetree. A peripheral node lists pin configurations per
**state** (`default`, `sleep`) and its driver applies them at init and on PM transitions.

## Remap a UART in an overlay (STM32)
STM32 pin nodes come predefined by the `hal_stm32` module (`dts/st/<series>/<soc>-pinctrl.dtsi`), named
`<periph>_<signal>_<pin>` (for example `usart1_tx_pb6`):
```dts
&usart1 {
    pinctrl-0 = <&usart1_tx_pb6 &usart1_rx_pb7>;
    pinctrl-names = "default";
    current-speed = <115200>;
    status = "okay";
};
```
If no predefined node exists for your pin/AF combination, define one:
```dts
&pinctrl {
    usart1_tx_pb6_custom: usart1_tx_pb6_custom {
        pinmux = <STM32_PINMUX('B', 6, AF7)>;
        slew-rate = "very-high-speed";
    };
};
```

## nRF: groups with psels
```dts
&pinctrl {
    uart0_default: uart0_default {
        group1 { psels = <NRF_PSEL(UART_TX, 0, 6)>; };
        group2 { psels = <NRF_PSEL(UART_RX, 0, 8)>; bias-pull-up; };
    };
    uart0_sleep: uart0_sleep {
        group1 { psels = <NRF_PSEL(UART_TX, 0, 6)>, <NRF_PSEL(UART_RX, 0, 8)>; low-power-enable; };
    };
};
&uart0 { pinctrl-0 = <&uart0_default>; pinctrl-1 = <&uart0_sleep>;
         pinctrl-names = "default", "sleep"; };
```
`pinctrl-N` index matches the position in `pinctrl-names`. Pin properties such as `bias-pull-up`,
`bias-pull-down`, `bias-disable` and `low-power-enable` (input with the input buffer disconnected) apply to every
pin in the group; the bias options are mutually exclusive. `NRF_PSEL_DISCONNECTED` explicitly disconnects a pin.

## In a driver
```c
#include <zephyr/drivers/pinctrl.h>
PINCTRL_DT_INST_DEFINE(n);                       /* per instance, before the config struct */
static const struct my_cfg cfg_##n = { .pcfg = PINCTRL_DT_INST_DEV_CONFIG_GET(n), ... };

static int my_init(const struct device *dev) {
    const struct my_cfg *cfg = dev->config;
    int ret = pinctrl_apply_state(cfg->pcfg, PINCTRL_STATE_DEFAULT);
    if (ret < 0) return ret;
    ...
}
/* PM action: PINCTRL_STATE_SLEEP on suspend (-ENOENT if the state does not exist: treat as OK) */
```
Needs `CONFIG_PINCTRL=y`; check that your board or driver enables it.

## Gotchas
- Review `build/zephyr/zephyr.dts` for two peripherals that claim the same pin in their `default` state.
- Plain GPIOs used via `gpios = <...>` are configured through the GPIO API (flags in the specifier), not pinctrl.
- A sleep state that leaves pins floating or driving into an unpowered device costs current;
  set bias or low-power mode explicitly (see gpio-leakage-and-floating-pin-elimination).
- Check the datasheet or reference manual alternate-function table for any custom pinmux node you write.

## Verify
- [ ] `zephyr.dts` shows the intended `pinctrl-0` per enabled peripheral, no pin used twice.
- [ ] Scope/logic analyser confirms signals on the new pins.
- [ ] With `CONFIG_PM_DEVICE`, sleep current drops after suspend (sleep state applied).

## Checked

Checked 2026-10-26 against the Zephyr pinctrl guide, `include/zephyr/drivers/pinctrl.h` and the nRF and STM32 pinctrl bindings on
main, and the `hal_stm32` devicetree sources: state model and `PINCTRL_STATE_DEFAULT`/`PINCTRL_STATE_SLEEP`,
`PINCTRL_DT_INST_DEFINE()`, `PINCTRL_DT_INST_DEV_CONFIG_GET()`, `pinctrl_apply_state()` returning -ENOENT for a missing state,
`pinctrl-names` index mapping, `psels` with `NRF_PSEL()`, `bias-pull-up`, `low-power-enable`, STM32 `pinmux` with
`STM32_PINMUX()` and `slew-rate` "very-high-speed", and predefined node names such as `usart1_tx_pb6`. Removed the unconfirmed
"last initialised wins" claim and the statement that `CONFIG_PINCTRL` is selected by drivers.

Method: documentation only; no commands were run.
