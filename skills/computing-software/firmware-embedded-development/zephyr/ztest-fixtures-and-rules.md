---
id: computing-software.firmware-embedded-development.zephyr.ztest-fixtures-and-rules
name: ztest-fixtures-and-rules
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [ztest-fixture, ztest-f, ztest-rule, ztest-suite-predicate, test-setup-teardown, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Share setup state across ztest cases with suite fixtures and ZTEST_F, run code around every test with ZTEST_RULE, and gate suites with predicates."
sources:
  - https://docs.zephyrproject.org/latest/develop/test/ztest.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ztest fixtures and rules

## Suite lifecycle
```c
ZTEST_SUITE(name, predicate, setup, before, after, teardown);
```
| Hook | Runs | Typical use |
|---|---|---|
| `predicate(global_state)` | before the suite, decides if it runs | skip on a hardware variant |
| `setup()` | once, returns fixture pointer | allocate/initialise shared object |
| `before(fixture)` | before each test | reset state |
| `after(fixture)` | after each test | cleanup, check leaks |
| `teardown(fixture)` | once at end | free |

## Fixture
```c
struct ringbuf_fixture {
    struct ring_buf rb;
    uint8_t storage[64];
};

static void *rb_setup(void)
{
    static struct ringbuf_fixture f;
    return &f;
}

static void rb_before(void *data)
{
    struct ringbuf_fixture *f = data;
    ring_buf_init(&f->rb, sizeof f->storage, f->storage);
}

ZTEST_SUITE(ringbuf, NULL, rb_setup, rb_before, NULL, NULL);

ZTEST_F(ringbuf, test_put_get)            /* fixture available as `fixture` */
{
    uint8_t in[4] = {1, 2, 3, 4}, out[4];
    zassert_equal(ring_buf_put(&fixture->rb, in, 4), 4);
    zassert_equal(ring_buf_get(&fixture->rb, out, 4), 4);
    zassert_mem_equal(in, out, 4);
}
```
`ZTEST_F(suite, name)` gives the test a variable named `fixture` of type `<suite>_fixture`.
`ZTEST_USER_F` also runs the test in a userspace thread when `CONFIG_USERSPACE` is enabled; fixture
memory must then be declared user-accessible (the `ZTEST_DMEM` / `ZTEST_BMEM` macros).

## Rules (cross-suite hooks)
```c
static void check_heap_before(const struct ztest_unit_test *t, void *data) { heap_mark(); }  /* heap_mark/heap_unchanged: your own helpers */
static void check_heap_after(const struct ztest_unit_test *t, void *data)
{
    zassert_true(heap_unchanged(), "%s leaked heap", t->name);
}
ZTEST_RULE(heap_leak_check, check_heap_before, check_heap_after);
```
Rules run the same logic for **every** test and every suite in the binary; the docs suggest them
for resetting mocks, resetting emulators or flushing the UART. A rule takes a before-each and an
after-each function (either may be `NULL`), each with the signature
`void fn(const struct ztest_unit_test *test, void *fixture)`.

## Predicates
```c
static bool only_with_sensor(const void *state) { return device_is_ready(sensor_dev); }
ZTEST_SUITE(sensor_hw, only_with_sensor, NULL, NULL, NULL, NULL);
```
The predicate receives the global state passed to `ztest_run_all(const void *state, bool shuffle,
int suite_iter, int case_iter)`; a custom `test_main()` can call it several times with different
state (for example one phase of a multi-phase test per call).

## Skipping and expectations
- `ztest_test_skip()` inside a test; `zassume_*` assertions skip instead of failing.
- `ZTEST_EXPECT_FAIL(suite, test)` / `ZTEST_EXPECT_SKIP(suite, test)` mark known failing or
  skipped tests; a test that behaves as expected is then reported as passed.
- `CONFIG_ZTEST_SHUFFLE=y` randomises the order (default is alphanumerical); the output shows the
  seed for failed tests. `CONFIG_ZTEST_REPEAT=y` repeats suites and cases (default factor 3).

## Verify
- [ ] Each test independent (passes with `CONFIG_ZTEST_SHUFFLE=y`).
- [ ] Shared state reset in `before`, not left from previous tests.

## Checked

2026-10-26. Zephyr docs main branch (latest release v4.4.2), ztest page (doc/develop/test/ztest.rst). Confirmed ZTEST_SUITE argument roles, ZTEST_F fixture variable and <suite>_fixture type, ZTEST_USER_F and ZTEST_DMEM/ZTEST_BMEM, ZTEST_RULE purpose and signature, predicate and ztest_run_all signature, ZTEST_EXPECT_FAIL/SKIP, CONFIG_ZTEST_SHUFFLE and CONFIG_ZTEST_REPEAT defaults. Removed the unconfirmed claims that skipped suites are reported as skipped and that before-rules run before the suite before hook.
Method: documentation only; no commands were run.
