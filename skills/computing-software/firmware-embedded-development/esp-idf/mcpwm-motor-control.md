---
id: computing-software.firmware-embedded-development.esp-idf.mcpwm-motor-control
name: mcpwm-motor-control
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-peripherals, mcpwm, motor-control-pwm, complementary-pwm, mcpwm-dead-time, bldc, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Generate motor-control PWM with the ESP-IDF MCPWM driver: timers, operators, comparators and generators, complementary outputs with dead time, fault shutdown and capture."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/peripherals/mcpwm/index.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/peripherals/mcpwm/mcpwm_gen.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/peripherals/mcpwm/mcpwm_fault.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/peripherals/mcpwm/mcpwm_cmpr.rst
  - https://github.com/espressif/esp-idf/blob/master/components/esp_driver_mcpwm/include/driver/mcpwm_oper.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MCPWM motor control

MCPWM (on chips that have it) is built from objects: timer -> operator -> comparator ->
generator, plus fault and capture units. Use it for half-bridges, BLDC, servo and power
stages; LEDC is enough for simple dimming.

## Complementary pair with dead time
```c
mcpwm_timer_handle_t tim; mcpwm_oper_handle_t op; mcpwm_cmpr_handle_t cmp;
mcpwm_gen_handle_t gh, gl;
mcpwm_timer_config_t tc = { .group_id = 0, .clk_src = MCPWM_TIMER_CLK_SRC_DEFAULT,
    .resolution_hz = 10000000, .period_ticks = 500,                 /* 10 kHz in up-down mode */
    .count_mode = MCPWM_TIMER_COUNT_MODE_UP_DOWN };                  /* centre aligned: period is 2 x period_ticks */
mcpwm_new_timer(&tc, &tim);
mcpwm_operator_config_t oc = { .group_id = 0 }; mcpwm_new_operator(&oc, &op);
mcpwm_operator_connect_timer(op, tim);
mcpwm_comparator_config_t cc = { .flags.update_cmp_on_tez = true }; mcpwm_new_comparator(op, &cc, &cmp);
mcpwm_generator_config_t g1 = { .gen_gpio_num = 25 }, g2 = { .gen_gpio_num = 26 };
mcpwm_new_generator(op, &g1, &gh); mcpwm_new_generator(op, &g2, &gl);

mcpwm_generator_set_actions_on_compare_event(gh,
    MCPWM_GEN_COMPARE_EVENT_ACTION(MCPWM_TIMER_DIRECTION_UP, cmp, MCPWM_GEN_ACTION_HIGH),
    MCPWM_GEN_COMPARE_EVENT_ACTION(MCPWM_TIMER_DIRECTION_DOWN, cmp, MCPWM_GEN_ACTION_LOW),
    MCPWM_GEN_COMPARE_EVENT_ACTION_END());
mcpwm_dead_time_config_t dt_h = { .posedge_delay_ticks = 5 };                  /* 500 ns */
mcpwm_dead_time_config_t dt_l = { .negedge_delay_ticks = 5, .flags.invert_output = true };
mcpwm_generator_set_dead_time(gh, gh, &dt_h);
mcpwm_generator_set_dead_time(gh, gl, &dt_l);        /* low side derived from high side */

mcpwm_comparator_set_compare_value(cmp, 250);        /* 50% */
mcpwm_timer_enable(tim); mcpwm_timer_start_stop(tim, MCPWM_TIMER_START_NO_STOP);
```
`update_cmp_on_tez` buffers a new compare value until the counter reaches zero, so duty changes land at a cycle boundary.
In up-down mode both legs count toward the period, so output frequency = resolution_hz / (2 x period_ticks).

## Fault shutdown
```c
mcpwm_gpio_fault_config_t fc = { .group_id = 0, .gpio_num = 27, .flags.active_level = 0 };
mcpwm_fault_handle_t f; mcpwm_new_gpio_fault(&fc, &f);
mcpwm_brake_config_t bc = { .fault = f, .brake_mode = MCPWM_OPER_BRAKE_MODE_CBC,
                            .flags.cbc_recover_on_tez = true };
mcpwm_operator_set_brake_on_fault(op, &bc);
mcpwm_generator_set_action_on_brake_event(gh, MCPWM_GEN_BRAKE_EVENT_ACTION(MCPWM_TIMER_DIRECTION_UP, MCPWM_OPER_BRAKE_MODE_CBC, MCPWM_GEN_ACTION_LOW));
```
CBC (cycle-by-cycle) braking recovers automatically at a cycle boundary after the fault clears; OST (one-shot)
braking stays latched until software recovers it, which suits overcurrent that must latch. Soft faults
(`mcpwm_new_soft_fault`) let application code trigger the same brake.

## Capture
MCPWM capture timers timestamp edges (hall sensors, pulse widths) with `mcpwm_new_capture_channel`.

## Verify
- [ ] Scope both gate signals: dead time visible on every edge, never overlapping.
- [ ] Fault pin asserted: outputs go to the configured brake level (measure the reaction time on a scope).
- [ ] Gate driver input polarity matches (`invert_output` correct).

## Checked

2026-10-26, against ESP-IDF master docs and headers (espressif/esp-idf, pushed 2026-10-24). Confirmed in peripherals/mcpwm (index, generator, comparator, fault pages) and the mcpwm headers: object chain, up-down mode frequency counts both legs, update_cmp_on_tez, mcpwm_generator_set_dead_time(in, out, config) usage with invert_output, complementary generators need dead time, brake config with cbc_recover_on_tez, CBC versus OST definitions, soft fault, mcpwm_new_capture_channel. Fixed: the example comment said 20 kHz but period_ticks 500 at 10 MHz in up-down mode is 10 kHz. Removed the chip list and the microseconds fault-response claim.

Method: documentation only; no commands were run.
