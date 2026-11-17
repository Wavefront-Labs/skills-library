---
id: computing-software.firmware-embedded-development.zephyr.ztest-suites
name: ztest-suites
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [twister, ztest, ztest-suite, zassert, testcase-yaml, ztest-fixtures, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Write Zephyr unit and integration tests with the ztest framework: ZTEST_SUITE/ZTEST, fixtures and lifecycle hooks, assertions, testcase.yaml, and running them with twister."
sources:
  - https://docs.zephyrproject.org/latest/develop/test/ztest.html
  - https://docs.zephyrproject.org/latest/develop/twister/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ztest suites

## Layout
```
tests/lib/ringbuf/
├── CMakeLists.txt     # find_package(Zephyr) + target_sources(app PRIVATE src/main.c)
├── prj.conf           # CONFIG_ZTEST=y
├── testcase.yaml
└── src/main.c
```

## Suite and tests
```c
#include <zephyr/ztest.h>
#include "ringbuf.h"

struct rb_fixture { struct ringbuf rb; uint8_t storage[16]; };

static void *rb_setup(void)                    /* once per suite */
{
    static struct rb_fixture f;
    return &f;
}
static void rb_before(void *data)              /* before each test */
{
    struct rb_fixture *f = data;
    ringbuf_init(&f->rb, f->storage, sizeof(f->storage));
}

ZTEST_SUITE(ringbuf, NULL, rb_setup, rb_before, NULL, NULL);
/*          name    predicate setup  before   after teardown */

ZTEST_F(ringbuf, test_put_get_roundtrip)
{
    zassert_ok(ringbuf_put(&fixture->rb, 0x42));
    uint8_t v;
    zassert_ok(ringbuf_get(&fixture->rb, &v));
    zassert_equal(v, 0x42, "got 0x%02x", v);
}

ZTEST_F(ringbuf, test_full_rejects)
{
    for (int i = 0; i < 15; i++) zassert_ok(ringbuf_put(&fixture->rb, i));
    zassert_equal(ringbuf_put(&fixture->rb, 99), -ENOSPC);
}
```
- `ZTEST(suite, name)` for tests without a fixture; `ZTEST_F` exposes `fixture`.
- Assertions: `zassert_true/false`, `zassert_equal`, `zassert_not_null`, `zassert_ok`,
  `zassert_mem_equal`, `zassert_within(a, b, delta)`. `zassume_*` skips instead of failing
  when a precondition (hardware present) isn't met; `ztest_test_skip()` skips explicitly.
- `ZTEST_USER` runs the test in a userspace thread when `CONFIG_USERSPACE` is enabled.
- The predicate gets the global state passed to `ztest_run_all()`, so one image can run a suite
  only in certain states (multi-phase tests via a custom `test_main`).
- `ZTEST_EXPECT_FAIL` / `ZTEST_EXPECT_SKIP` mark known failures or skips; `CONFIG_ZTEST_SHUFFLE`
  randomises order and `CONFIG_ZTEST_REPEAT` repeats suites and cases.

## testcase.yaml
```yaml
common:
  tags: [lib, ringbuf]
  integration_platforms: [native_sim]
tests:
  lib.ringbuf.default: {}
  lib.ringbuf.small_buf:
    extra_configs:
      - CONFIG_RINGBUF_SMALL=y
  lib.ringbuf.hw:
    platform_allow: [nucleo_l476rg]
    harness: ztest
```
Test names are dotted; each entry is a separate build/run with its own config.

## Running
```bash
west twister -T tests/lib/ringbuf -p native_sim          # build + run + report
west build -b native_sim tests/lib/ringbuf -t run         # quick single run, output on stdout
west twister -T tests -p native_sim --tag ringbuf -v      # filter by tag
```
Results: `twister-out/twister.json` and JUnit `twister.xml` / `twister_report.xml` for CI.
`native_sim` boots the full Zephyr OS as a host binary (Linux hosts).

## Pure unit tests
For host-only code with stubs or mocks and no kernel, use the `unit_testing` pseudo-board
(`-DBOARD=unit_testing`, chosen automatically by twister for scenarios with `type: unit`). The
Zephyr kernel, devicetree and drivers are not built; only the code you add to the `testbinary`
CMake target plus ztest:
```cmake
find_package(Zephyr COMPONENTS unittest REQUIRED HINTS $ENV{ZEPHYR_BASE})
target_sources(testbinary PRIVATE main.c)
```
```yaml
tests:
  lib.ringbuf.unit:
    type: unit
```
Unit tests run as native host applications and are supported on Linux only.

## Verify
- [ ] Suite passes on native_sim in CI with JUnit results published.
- [ ] Each test is independent: `before` resets state; tests pass in any order (`CONFIG_ZTEST_SHUFFLE=y`).
- [ ] Tests that need hardware use `zassume`/`platform_allow`, not failures, on other targets.

## Checked

2026-10-26. Zephyr docs main branch (latest release v4.4.2). Confirmed ZTEST/ZTEST_F/ZTEST_USER semantics and suite hooks (ztest page), the assertion macros zassert_ok/equal/mem_equal/within/not_null (ztest_assert.h), testcase.yaml keys common, tags, extra_configs, platform_allow, integration_platforms, harness (twister page), twister --tag, and the unit_testing board rules (type: unit, testbinary, Linux only). Wrong in the draft: unit tests need type: unit and the unittest CMake component, not just -p unit_testing; moved the old twister URL to develop/twister.
Method: documentation only; no commands were run.
