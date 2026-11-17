---
id: computing-software.firmware-embedded-development.platformio.mocking-hardware-in-native-tests
name: mocking-hardware-in-native-tests
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [pio-mock, fakeit, arduinofake, fake-function-framework, hardware-abstraction, link-seams, native-tests, platformio, firmware-embedded-development]
level: advanced
status: draft
description: "Test firmware on the native platform by faking hardware: link-time fakes, fff, ArduinoFake/FakeIt for Arduino APIs, HAL interfaces, and build_src_filter to swap implementations."
sources:
  - https://docs.platformio.org/en/latest/advanced/unit-testing/simulators/index.html
  - https://github.com/FabioBatSilva/ArduinoFake
  - https://github.com/meekrosoft/fff
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mocking hardware in native tests

The native platform has no registers, no `digitalWrite`, no HAL. Give the code something to call.

## Strategy 1: thin HAL + link seams (C projects)
Code calls `hal_gpio_write(pin, v)`, declared in `hal_gpio.h`. Target builds link `hal_gpio_stm32.c`;
native tests link a fake:
```ini
[env:native]
platform = native
build_src_filter = +<*> -<hal/stm32/> -<main.c>
test_build_src = yes
```
```c
/* test/test_led/fake_hal_gpio.c */
int fake_gpio_state[32]; int fake_gpio_writes;
void hal_gpio_write(int pin, int v) { fake_gpio_state[pin] = v; fake_gpio_writes++; }
```
Tests assert on the recorded state.

## Strategy 2: fff (Fake Function Framework)
Header-only macros generating fakes with call counts and argument history:
```c
#include "fff.h"
DEFINE_FFF_GLOBALS;
FAKE_VALUE_FUNC(int, i2c_read, uint8_t, uint8_t, uint8_t*, size_t);
FAKE_VOID_FUNC(delay_ms, uint32_t);

void setUp(void) { RESET_FAKE(i2c_read); RESET_FAKE(delay_ms); FFF_RESET_HISTORY(); }
void test_sensor_retries(void) {
    int seq[] = {-1, -1, 0}; SET_RETURN_SEQ(i2c_read, seq, 3);
    TEST_ASSERT_EQUAL(0, sensor_init());
    TEST_ASSERT_EQUAL(3, i2c_read_fake.call_count);
    TEST_ASSERT_EQUAL(2, delay_ms_fake.call_count);
}
```
Add `fff` via `lib_deps = meekrosoft/fff` or vendor the header.

## Strategy 3: Arduino code with ArduinoFake
```ini
[env:native]
platform = native
lib_deps = fabiobatsilva/ArduinoFake
```
```cpp
#include <ArduinoFake.h>
using namespace fakeit;
void test_blink(void) {
  When(Method(ArduinoFake(), digitalWrite)).AlwaysReturn();
  When(Method(ArduinoFake(), millis)).Return(0, 600);
  blink_step();  blink_step();
  Verify(Method(ArduinoFake(), digitalWrite).Using(13, HIGH)).Once();
}
```
Covers `Arduino.h`, `Serial`, `Wire`, `SPI` partially; extend for missing APIs.

## Strategy 4: C++ interfaces + gMock
Inject an interface (`I2cBus&`) into drivers; mock it with GoogleMock (see googletest skill).

## Time
Fake the clock (`millis()`, `HAL_GetTick`) as a variable the test advances. Tests of timeouts then
run instantly and deterministically.

## Verify
- [ ] Native env builds with zero vendor headers included.
- [ ] Fakes reset between tests (no order dependence: run with `-f` on single tests too).
