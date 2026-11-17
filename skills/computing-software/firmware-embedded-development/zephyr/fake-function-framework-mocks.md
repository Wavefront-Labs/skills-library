---
id: computing-software.firmware-embedded-development.zephyr.fake-function-framework-mocks
name: fake-function-framework-mocks
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [fff, fake-value-func, fake-void-func, unit-test-mocks, ztest-mocking, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Mock dependencies in Zephyr unit tests with the Fake Function Framework (fff): define fakes, control return values and sequences, reset between tests, and check call history."
sources:
  - https://docs.zephyrproject.org/latest/develop/test/ztest.html#mocking-via-fff
  - https://github.com/meekrosoft/fff
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/testsuite/include/zephyr/fff.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fake Function Framework mocks

fff ships with Zephyr (`zephyr/fff.h`). It generates fake C functions that record calls and
return programmable values, so the unit under test can be compiled against fakes instead of real
drivers or kernel calls.

## Test layout
```
tests/unit/battery/
  CMakeLists.txt
  prj.conf            # CONFIG_ZTEST=y
  testcase.yaml
  src/main.c
```
```cmake
cmake_minimum_required(VERSION 3.20)
find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(battery_test)
target_sources(app PRIVATE src/main.c <path-to>/battery.c)   # unit under test only
```
This layout builds on `native_sim` (full Zephyr OS as a host binary). For code with no kernel
dependency, use the `unit_testing` board instead: `type: unit` in the scenario, and
`find_package(Zephyr COMPONENTS unittest ...)` with `target_sources(testbinary ...)`.

## Defining fakes
```c
#include <zephyr/fff.h>
#include <zephyr/ztest.h>
#include "battery.h"

DEFINE_FFF_GLOBALS;

/* fake the ADC wrapper the unit uses */
FAKE_VALUE_FUNC(int, adc_read_mv, uint8_t, int32_t *);
FAKE_VOID_FUNC(led_set, bool);

static int adc_returns_3700(uint8_t ch, int32_t *mv) { *mv = 3700; return 0; }

static void reset_fakes(const struct ztest_unit_test *test, void *fixture)
{
    ARG_UNUSED(test);
    ARG_UNUSED(fixture);
    RESET_FAKE(adc_read_mv);
    RESET_FAKE(led_set);
    FFF_RESET_HISTORY();
}
ZTEST_RULE(fff_reset, reset_fakes, NULL);    /* runs before every test */

ZTEST(battery, test_low_battery_turns_led_on)
{
    adc_read_mv_fake.custom_fake = adc_returns_3700;
    battery_check();
    zassert_equal(led_set_fake.call_count, 1);
    zassert_false(led_set_fake.arg0_val, "LED should be off at 3.7 V");
}

ZTEST(battery, test_adc_error_propagates)
{
    adc_read_mv_fake.return_val = -EIO;
    zassert_equal(battery_check(), -EIO);
}

ZTEST_SUITE(battery, NULL, NULL, NULL, NULL, NULL);
```

## Useful controls
| Field / macro | Use |
|---|---|
| `x_fake.return_val` | fixed return value |
| `SET_RETURN_SEQ(x, arr, n)` | different value per call |
| `x_fake.custom_fake` | function to run (fill out-params, simulate behaviour) |
| `x_fake.custom_fake_seq` | sequence of custom fakes |
| `x_fake.call_count`, `argN_val`, `argN_history[]` | assertions on calls |
| `fff.call_history[]` | global call order across fakes |

## Faking Zephyr APIs
Static inline device APIs (`gpio_pin_set_dt`, `i2c_write_dt`) can't be faked directly. Either:
- wrap hardware access in your own thin functions (best), or
- use the FFF-based fake drivers Zephyr provides, configured via devicetree and Kconfig
  (bindings `zephyr,fake-can`, `zephyr,fake-comp`, `zephyr,fake-eeprom`, `zephyr,fake-leds`,
  `zephyr,fake-pwm`, `zephyr,fake-regulator`, `zephyr,fake-rtc`, `zephyr,fake-stepper-ctrl`,
  `zephyr,fake-stepper-driver`), or the emulators under `zephyr,*-emul*` bindings.

## Gotchas
- One definition per fake per binary; put shared fakes in a `fakes.c` with the matching
  declaration macros in a header (Zephyr adds `DECLARE_FAKE_*`/`DEFINE_FAKE_*` extensions to FFF).
- History arrays are bounded by `FFF_ARG_HISTORY_LEN` (50 in Zephyr's `fff.h`) and
  `FFF_CALL_HISTORY_LEN`, which you can define before including `fff.h`.
- Forgetting the reset rule leaks state between tests, causing order-dependent failures.

## Verify
- [ ] Tests reset fakes before each case (ZTEST_RULE or before() hook).
- [ ] Unit test build links only the unit and fakes (no real drivers).

## Checked

2026-10-26. Zephyr docs main branch (latest release v4.4.2) plus upstream FFF README and Zephyr subsys/testsuite/include/zephyr/fff.h. Confirmed FAKE_VALUE_FUNC/FAKE_VOID_FUNC, RESET_FAKE, FFF_RESET_HISTORY, SET_RETURN_SEQ, fff.call_history, arg history length default 50, the ZTEST_RULE reset pattern and signature, the Zephyr fake-driver bindings and the unit_testing board rules (ztest page). Fixed the ZTEST_RULE callback signature, the unit_testing CMake component, and the dead fff.html source link; removed the unconfirmed syscall-faking advice and APP_ROOT variable.
Method: documentation only; no commands were run.
