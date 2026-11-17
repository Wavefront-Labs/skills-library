---
id: computing-software.software-engineering.v-lang.v-result-type-and-errors
name: v-result-type-and-errors
category: computing-software
field: software-engineering
product: v-lang
tags: [v-result-type-and-errors, option-and-result-types, result, int, error, err, or block, void, ierror, msg, v-lang]
level: practitioner
status: docs-checked
description: "Return !T results with error() values, handle with or blocks and err, and use !void functions and custom error types."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Result types !T and returning errors

Goal: fail with a reason.

- Result types use `!`: `!User`. A Result stores either a value or an `IError`. Return a failure with `return error('User ${id} not found')`; V wraps a plain returned value automatically.
- Handle: `user := repo.find_user_by_id(7) or { println(err) return }`. In a Result's `or` block and failed `if` guard, `err` is the `IError`; use `err.msg()` and `err.code()`.
- Propagate with `!` after the call: `resp := http.get(url)!` in a function returning `!T`; it is a shorthand for `or { return err }`. If propagation is used in `main()` it panics, since the error cannot propagate further.
- Default value: `a := do_something('bar') or { 'default' }`. Early break: `or { return }`, `or { panic(err) }`, `or { continue }`/`break` inside a `for`.
- `if resp := http.get(url) { ... } else { println(err) }`: `err` is only in scope for the `else` branch.
- A function returning only `!` has no success payload (a Result of `void`); callers still use `or` or propagation.
- Multiple values with an error: `fn multi_return(v int) !(int, int)`; only one Option or Result may be returned.
- Custom errors: implement `IError` (`msg() string` and `code() int`); embedding the builtin `Error` gives empty defaults, so you implement only what you need: `struct PathError { Error  path string }` with `fn (err PathError) msg() string`. Returning it from a `!` function casts it to `IError` automatically.
- Compare errors with `err is io.Eof`.
- V does not use `throw/try/catch`; errors cannot be left unhandled.

Verify: `assert (parse('') or { -1 }) == -1`.

## Checked

Date: 2026-11-02. Confirmed in the V documentation (doc/docs.md, "Option/Result types and error handling", "Custom error types"). Removed as not stated there: `error_with_code`, "main exits with the error printed" (the docs say it panics), the `$err` interpolation form, "or after `!void` must not yield a value".

Method: documentation only; no commands were run.
