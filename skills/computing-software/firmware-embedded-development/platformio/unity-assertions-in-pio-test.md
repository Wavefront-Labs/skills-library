---
id: computing-software.firmware-embedded-development.platformio.unity-assertions-in-pio-test
name: unity-assertions-in-pio-test
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [unity-test, unity-assertions, test-assert, setup-teardown, unity-begin, test-framework-unity, pio-test, platformio, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Write Unity tests for pio test: UNITY_BEGIN/RUN_TEST/UNITY_END, assertion families, setUp/tearDown, unity_config.h and build_flags options."
sources:
  - https://docs.platformio.org/en/latest/advanced/unit-testing/frameworks/unity.html
  - https://github.com/ThrowTheSwitch/Unity/blob/master/docs/UnityAssertionsReference.md
  - https://github.com/ThrowTheSwitch/Unity/blob/master/docs/UnityConfigurationGuide.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unity assertions in pio test

Select Unity in `platformio.ini` with `test_framework = unity`. It supports native and embedded tests.

## File structure
A test file includes `unity.h` and the header of the component under test, defines `setUp()` and
`tearDown()` (no arguments, no return value; either may be empty), the test functions, and a runner.
```c
#include <unity.h>
#include "file_to_test.h"

void setUp(void)    { /* runs before each test */ }
void tearDown(void) { /* runs after each test */ }

void test_function_should_doBlah(void) { /* assertions */ }

int runUnityTests(void) {
    UNITY_BEGIN();
    RUN_TEST(test_function_should_doBlah);
    return UNITY_END();
}

int main(void) { return runUnityTests(); }   /* native */
/* Arduino:  void setup() { delay(2000); runUnityTests(); }  void loop() {}   */
/* ESP-IDF:  void app_main() { runUnityTests(); }                             */
```
- Test functions conventionally start with `test_` or `spec_`, take no arguments and return nothing.
- Every test needs its own `RUN_TEST` call; add each new test to the runner.
- Keep only the `main` variant for your framework (the PlatformIO example warns to remove the others).
- On Arduino the PlatformIO example waits about 2 seconds (`delay(2000)`) before the runner so the host's
  serial connection is established.

## Assertion families (Unity Assertions Reference)
- Booleans and pointers: `TEST_ASSERT_TRUE`, `TEST_ASSERT_FALSE`, `TEST_ASSERT_NULL`,
  `TEST_ASSERT_NOT_NULL`, `TEST_ASSERT_EQUAL_PTR`.
- Integers: `TEST_ASSERT_EQUAL_INT`, `_INT8/16/32/64`, `TEST_ASSERT_EQUAL_UINT8`, `TEST_ASSERT_EQUAL_HEX8/16/32`,
  `TEST_ASSERT_INT_WITHIN(delta, expected, actual)`, `TEST_ASSERT_BITS`, and comparisons such as
  `TEST_ASSERT_GREATER_THAN_INT8` and `TEST_ASSERT_LESS_THAN_INT32`.
- Floats: `TEST_ASSERT_FLOAT_WITHIN(delta, expected, actual)` and `TEST_ASSERT_EQUAL_FLOAT` (equal if "close
  enough"). Exact float equality is not guaranteed, so prefer a delta.
- Arrays: `TEST_ASSERT_EQUAL_UINT8_ARRAY(expected, actual, num_elements)` and the same pattern for other types.
- Memory and strings: `TEST_ASSERT_EQUAL_MEMORY`, `TEST_ASSERT_EQUAL_STRING`, `TEST_ASSERT_EQUAL_STRING_LEN`.
- Messages: assertions have a `_MESSAGE` variant that takes a custom message; `TEST_FAIL_MESSAGE`,
  `TEST_IGNORE_MESSAGE` and `TEST_PASS` exist.
- Argument order for comparisons is expected, then actual.

## Configuration
Unity options are `#define`s, so most can be passed through `build_flags`:
```ini
[env:extra_unity_options]
platform = native
build_flags =
    -D UNITY_INT_WIDTH=16
    -D UNITY_FLOAT_TYPE=float16_t
```
- PlatformIO's runner defines `UNITY_INCLUDE_CONFIG_H` and looks for a custom `unity_config.h` in the current
  test folder, then walks up the test hierarchy to `test_dir`.
- If none is found, PlatformIO generates a default one that routes output to standard input/output on the
  native platform and to the first available Serial interface on embedded platforms.
- Per the Unity configuration guide: float support is on by default and double support is off, controlled by
  `UNITY_INCLUDE_FLOAT`, `UNITY_EXCLUDE_FLOAT`, `UNITY_INCLUDE_DOUBLE` and `UNITY_EXCLUDE_DOUBLE`; define
  `UNITY_SUPPORT_64` only if 64-bit support is not auto-detected (it costs size and speed on small targets);
  define `UNITY_OUTPUT_COLOR` for ANSI colours; `UNITY_OUTPUT_CHAR` customises character output.

## Verify
- [ ] Each test fails when the code under test is broken (mutate once to check).
- [ ] Every test function has a `RUN_TEST` line.

## Checked
2026-11-08. Read: PlatformIO Unity page (runner layout, configuration, unity_config.h lookup), Unity Assertions
Reference (assertion names, argument order) and Unity Configuration Guide (float, 64-bit, colour and output
options). Removed unconfirmed claims: the CRC example vector, per-folder test program build, `pio test`
filter flags and CI exit-code behaviour, plain `TEST_ASSERT_GREATER_THAN` and `TEST_ASSERT_EACH_EQUAL_INT`
names, and the statement that float support is on by default for most targets.
Method: documentation only; no commands were run.
