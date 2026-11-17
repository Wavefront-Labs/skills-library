---
id: computing-software.firmware-embedded-development.bare-metal-programming.host-unit-testing-unity-cmock-ceedling
name: host-unit-testing-unity-cmock-ceedling
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [ceedling, unity, cmock, host-testing, tdd-embedded, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Unit test firmware modules on the PC with Unity, CMock-generated mocks of driver headers and Ceedling: install, project creation, CMock plugins and generated Expect functions."
sources:
  - https://www.throwtheswitch.org/ceedling
  - https://github.com/ThrowTheSwitch/CMock/blob/master/docs/CMock_Summary.md
  - https://github.com/ThrowTheSwitch/Unity/blob/master/docs/UnityAssertionsReference.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Host unit testing with Unity, CMock and Ceedling

Run module tests on the build machine. Unity is the assertion framework, CMock generates mocks from
headers, and Ceedling (a Ruby gem) discovers tests, generates the runner, builds and runs them.

## Setup (from the Ceedling page)
```sh
gem install ceedling --no-document
ceedling new MyProject        # creates project.yml, src, test, test/support
ceedling module:create[Demo]  # src/Demo.c, src/Demo.h, test/test_Demo.c
ceedling test:all             # discover, build and run every test
```
- Configuration lives in one YAML file (`project.yml`) that can be kept in version control.
- Ceedling needs no hand-written test list or `main`; it generates the runner.
- By default it builds with native gcc or clang; it can be configured for cross-compilers and
  simulators. A prebuilt Docker image, `throwtheswitch/madsciencelab:latest`, is offered as an
  alternative to a local install.
- Console output summarises TESTED, PASSED, FAILED and IGNORED counts; failures show the test
  name and line, and each test stops at its first failed assertion.

## CMock configuration (from CMock_Summary)
```yaml
:cmock:
  :mock_prefix: Mock
  :plugins:
    - :ignore
    - :expect_any_args
    - :callback
  :treat_externs: :include
```
- `:mock_prefix` defaults to `Mock` (so `USART.h` yields a mock named `MockUSART`). Set it to
  match the `#include` you write in tests.
- `:expect` is always active. Optional plugins: `:ignore`, `:ignore_stateless`, `:ignore_arg`,
  `:expect_any_args`, `:array`, `:cexception`, `:callback`, `:return_thru_ptr`.
- `:treat_externs` takes `:include` (mock externed functions) or `:exclude` (the default).
- Generated functions per mocked `func`: `func_Expect(expected_params)` for a void function,
  `func_ExpectAndReturn(expected_params, retval)` for a function with a return value, and
  `func_IgnoreAndReturn(retval)`. `func_StubWithCallback` is an older name and is documented as
  deprecated.

## A test with a mocked driver
```c
#include "unity.h"
#include "battery.h"          /* module under test */
#include "MockAdc.h"          /* CMock generates this from adc.h with the default prefix */

void test_low_battery_flagged(void) {
    adc_read_mv_ExpectAndReturn(ADC_CH_VBAT, 3300);
    TEST_ASSERT_TRUE(battery_is_low());
}
void test_adc_error_reported(void) {
    adc_read_mv_ExpectAndReturn(ADC_CH_VBAT, -1);
    TEST_ASSERT_EQUAL_INT(BATT_ERR_ADC, battery_status());
}
```
`TEST_ASSERT_TRUE(condition)` and `TEST_ASSERT_EQUAL_INT(expected, actual)` are in the Unity
assertions reference.

## Dealing with hardware (design advice)
- Mock at your own driver boundary rather than at a vendor HAL, so tests are not coupled to HAL
  signatures.
- Keep vendor device headers out of headers that tests include, or provide test doubles.
- Use `<stdint.h>` fixed-width types in production code so host and target sizes agree.

## Verify
- [ ] `ceedling test:all` passes from a clean checkout.
- [ ] Removing an expected call from the code under test makes its test fail.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Ceedling page (install command, `ceedling new`, `module:create`, `test:all`, YAML config, Docker image, console summary), the CMock_Summary (`:mock_prefix` default, plugin names, `:treat_externs`, `_Expect`/`_ExpectAndReturn`/`_IgnoreAndReturn`, deprecated `_StubWithCallback`) and the Unity assertions reference (`TEST_ASSERT_TRUE`, `TEST_ASSERT_EQUAL_INT`). Removed because no cited page states them: the `:paths`, `:defines` and `:test_file_prefix` project.yml excerpt, `ceedling gcov:all`, JUnit report plugin names, `TEST_FILE`, the exact failure message for a missing call, the `-m32` advice and the `long` size note. The mock prefix in the example was changed from `mock_` to the documented default. The Unity reference page does not show the `unity.h` include; that line is unconfirmed project convention.
