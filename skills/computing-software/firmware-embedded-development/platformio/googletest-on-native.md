---
id: computing-software.firmware-embedded-development.platformio.googletest-on-native
name: googletest-on-native
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [googletest, gmock, test-framework, native-platform, host-testing, pio-test, platformio, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Run GoogleTest/GoogleMock unit tests for firmware logic on the PlatformIO native platform: test_framework = googletest, main(), fixtures, mocks, and keeping code host-compilable."
sources:
  - https://docs.platformio.org/en/latest/advanced/unit-testing/frameworks/googletest.html
  - https://google.github.io/googletest/primer.html
  - https://google.github.io/googletest/gmock_for_dummies.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GoogleTest on native

## Config
```ini
[env:native]
platform = native
test_framework = googletest
build_flags = -std=c++17 -Wall -Wextra -DUNIT_TEST
build_src_filter = +<logic/> -<main.cpp>      ; only hardware-independent sources
test_build_src = yes                          ; compile src/ into the test program
```
`test_framework = googletest` selects the framework and you write your own `main()`. The docs list embedded
tests only for the Espressif ESP8266 and ESP32 platforms; keep it to native.

## Test file
```cpp
// test/test_filter/test_main.cpp
#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "logic/debounce.h"

class DebounceTest : public ::testing::Test {
 protected:
  Debounce d{/*stable_ms=*/20};
};
TEST_F(DebounceTest, IgnoresShortGlitch) {
  d.update(true, 0); d.update(false, 5);
  EXPECT_FALSE(d.pressed());
}
TEST_F(DebounceTest, AcceptsStableLevel) {
  d.update(true, 0); d.update(true, 25);
  EXPECT_TRUE(d.pressed());
}
int main(int argc, char **argv) {
  ::testing::InitGoogleMock(&argc, argv);
  return RUN_ALL_TESTS();
}
```
`pio test -e native -v` shows each test; filter suites with `pio test -e native -f test_filter` and
pass GoogleTest flags with `-a "--gtest_filter=Debounce*"` (`--program-arg`) or `test_testing_command`.

## Mocking hardware with gMock
Put hardware behind an interface and inject it:
```cpp
struct I2cBus { virtual ~I2cBus() = default; virtual bool read(uint8_t a, uint8_t r, uint8_t *b, size_t n) = 0; };
struct MockI2c : I2cBus { MOCK_METHOD(bool, read, (uint8_t, uint8_t, uint8_t*, size_t), (override)); };

TEST(Bme280, ReadsChipId) {
  MockI2c bus; Bme280 s(bus);
  EXPECT_CALL(bus, read(0x76, 0xD0, testing::_, 1))
      .WillOnce(testing::DoAll(testing::SetArgPointee<2>(0x60), testing::Return(true)));
  EXPECT_TRUE(s.begin());
}
```

## Keeping code host-compilable
- Separate pure logic (parsers, state machines, filters, protocol framing) from drivers.
- Avoid including vendor headers in logic files; use fixed-width types and your own abstractions.
- Watch type-size differences (int is 32-bit on host and ARM, 16-bit on AVR; long is 64-bit on
  Linux x86_64).

## Verify
- [ ] Native tests run in CI in seconds without hardware.
- [ ] A bug injected in the logic is caught by a failing test.

## Checked
2026-11-01. Confirmed in the platformio-docs repo (advanced/unit-testing/frameworks/googletest.rst, core/userguide/cmd_test.rst,
projectconf test options): `test_framework = googletest`, own `main()` with `InitGoogleMock`/`RUN_ALL_TESTS`, native and ESP
embedded support, `-a`/`--program-arg` with `--gtest_filter`, `test_testing_command`, `test_build_src`, `-f` filter. Removed the
claims that PlatformIO installs GoogleTest automatically and about host compiler choice. gMock usage is GoogleTest API, not
PlatformIO-specific.
Method: documentation only; no commands were run.
