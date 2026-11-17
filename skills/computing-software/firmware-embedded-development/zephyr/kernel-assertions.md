---
id: computing-software.firmware-embedded-development.zephyr.kernel-assertions
name: kernel-assertions
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-assert, config-assert, assert-no-msg-info, assert-post-action, build-assert, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Use Zephyr __ASSERT and BUILD_ASSERT effectively: CONFIG_ASSERT levels, message vs no-message size trade-offs, assert_post_action override, and assert use in tests."
sources:
  - https://docs.zephyrproject.org/latest/kernel/services/other/assert.html
  - https://docs.zephyrproject.org/latest/kernel/services/other/fatal.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/v4.4.2/include/zephyr/sys/__assert.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kernel assertions

## Runtime asserts
Release note: on the main branch (after v4.4.2) the docs make `ZASSERT()` the recommended API
(`#include <zephyr/sys/zassert.h>`, one `ZASSERT_MODULE(NAME);` per file, per-module level
`Off` / `Terse` / `Normal` / `Verbose`), and describe `__ASSERT()` and the `CONFIG_ASSERT*` options as deprecated
compatibility over a `DEFAULT` module (`CONFIG_ASSERT_MODULE_DEFAULT_LEVEL_*`); `CONFIG_ASSERT` stays the master
switch. The rest of this skill describes the `__ASSERT()` family used up to v4.4.x, which still works on main.
Note the lowercase `zassert_*` macros of ztest are unrelated.
```c
#include <zephyr/sys/__assert.h>

__ASSERT(len <= sizeof(buf), "len %u too big", len);
__ASSERT_NO_MSG(dev != NULL);
__ASSERT_EVAL(expr_when_off, expr_when_on, test, "msg");   /* keep side effects either way */
```
```
CONFIG_ASSERT=y
CONFIG_ASSERT_LEVEL=2          # 0 off, 1 on with a compile-time warning, 2 on
CONFIG_ASSERT_VERBOSE=y        # print the message through assert_print()
CONFIG_ASSERT_NO_COND_INFO=n   # y drops the condition text
CONFIG_ASSERT_NO_MSG_INFO=n    # y drops the message
```
Zephyr's kernel and drivers are full of `__ASSERT`s (wrong context, invalid objects, double
gives). Turning `CONFIG_ASSERT=y` on is one of the first steps when debugging a weird failure:
misuse is reported at the call instead of corrupting state.

## Size trade-off
Asserts with messages pull in strings and formatting. For constrained release builds that still
want checks, drop the optional text (the doc notes the compiler must be able to prune it, so
low optimisation levels can leave artifacts):
```
CONFIG_ASSERT=y
CONFIG_ASSERT_VERBOSE=n
CONFIG_ASSERT_NO_COND_INFO=y
CONFIG_ASSERT_NO_MSG_INFO=y
```
Check the cost with `rom_report`.

## What happens on failure
A failed runtime assertion induces a fatal error. In the `__ASSERT()` implementation the message goes
through `assert_print()` and then `assert_post_action(file, line)` runs; the application can override
`assert_post_action` (see `include/zephyr/sys/__assert.h`) and the fatal error ends in
`k_sys_fatal_error_handler()`. Override for products:
```c
void assert_post_action(const char *file, unsigned int line)
{
    crashlog_save(file, line);   /* to retained RAM */
    sys_reboot(SYS_REBOOT_COLD);
}
```
(`CONFIG_ASSERT_NO_FILE_INFO` changes the signature; match your config.)

## Compile-time asserts
```c
BUILD_ASSERT(sizeof(struct hdr) == 8, "hdr must be packed to 8 bytes");
BUILD_ASSERT(DT_PROP(DT_NODELABEL(adc0), resolution) >= 12, "ADC resolution too low");
```
Same semantics as C `_Static_assert`: always checked, free at runtime, and the message must be a static
string (no formatting). Use for struct layouts, DT/Kconfig consistency, array sizes.

## Tests
ztest's `zassert_*` macros are separate (test assertions). With `CONFIG_ASSERT_TEST` the post-action
handler is allowed to return instead of aborting, so tests can validate assertion behaviour with a
custom hook.

## Verify
- [ ] Debug/CI builds have `CONFIG_ASSERT=y`.
- [ ] Release policy decided (off, or on with no-info options plus custom post action).
- [ ] Assert expressions have no side effects (or use `__ASSERT_EVAL`).

## Checked

Checked 2026-10-26 against the Zephyr documentation and sources on the main branch (repository head 2026-10-25; latest release v4.4.2).
- `ZASSERT` as the recommended API, `__ASSERT` and `CONFIG_ASSERT*` deprecated on main, `BUILD_ASSERT` semantics, assert
  testing option (doc: kernel/services/other/assert, main branch only; not present in the v4.4.2 tree).
- `__ASSERT`, `__ASSERT_NO_MSG`, `__ASSERT_EVAL`, `CONFIG_ASSERT_LEVEL`, `assert_print`, `assert_post_action` signatures and
  the `NO_FILE_INFO` variant (`include/zephyr/sys/__assert.h` at v4.4.2).
- Wrong or stale: the draft presented `__ASSERT` as the current API; the default-action chain `k_panic()` was removed
  (unconfirmed for the legacy path); the `CONFIG_ZTEST_FATAL_HOOK` / `ztest_set_assert_valid` testing recipe was not
  confirmed and was replaced with `CONFIG_ASSERT_TEST`; the "several KB" size figure was removed.

Method: documentation only; no commands were run.
