---
id: computing-software.software-engineering.rust.mocking-with-mockall-and-trait-seams
name: mocking-with-mockall-and-trait-seams
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-testing, rust-mockall, mockall, mocking, test-doubles, trait-seams]
level: practitioner
status: docs-checked
description: "Isolate Rust code in tests by defining narrow traits as seams and generating mocks with mockall: expectations, call counts, sequences, checkpoints."
sources:
  - https://docs.rs/mockall/latest/mockall/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Mocking with mockall and trait seams

**Goal:** unit-test logic that depends on I/O, time or services without running them.

First create a **seam**: depend on a small trait, not a concrete client. Prefer a hand-written fake for simple cases; use mockall when you need call-count or argument expectations.

```rust
use mockall::{automock, predicate::*};

#[automock]
pub trait Mailer { fn send(&self, to: &str, body: &str) -> Result<(), MailError>; }

fn notify(m: &dyn Mailer, user: &User) -> Result<(), MailError> {
    m.send(&user.email, "welcome")
}

#[test]
fn sends_welcome() {
    let mut m = MockMailer::new();
    m.expect_send()
        .with(eq("a@x.com"), eq("welcome"))
        .times(1)
        .returning(|_, _| Ok(()));
    notify(&m, &User::new("a@x.com")).unwrap();
}
```

- `#[automock]` mocks most traits, or structs with a single `impl` block; `mock!` handles what it cannot. The mock is named like the original with `Mock` prepended, built with `new` or `default`.
- Each expectation can have argument matchers, a required call count (`times`, `never`) and a position in a `Sequence` (`in_sequence`); each needs a return value (`returning`, `return_const`, and so on). Accesses contrary to expectations panic.
- By default an expectation may be called any number of times and in any order. A `Sequence` fixes order and can span several mock objects.
- `mock.checkpoint()` immediately validates all expectations (for example that a `times(2)` call count was met) and lets you add new ones afterwards.
- Mock objects are always `Send`; for non-`Send` argument types the docs describe wrapper matchers.
- Methods returning `impl Trait` are supported with limitations: the expectation returns a `Box<dyn Trait>`, and `Sized` traits like `Clone` or multiple non-auto traits cannot be used.
- Non-`Clone` return values can be supplied with an `FnOnce` closure in `returning`.

## Gotchas
- Over-specified expectations couple tests to implementation; assert outcomes where you can.
- A call that exceeds `times` panics at the call; a shortfall is only detected when expectations are validated (at a checkpoint or when the mock is dropped).

## Verify
Temporarily remove the `send` call and confirm the test fails because the expectation was not satisfied.

## Checked
Method: docs-checked 2026-11-09 against the mockall crate page at docs.rs (usage, call counts, sequences, checkpoints, impl Trait sections read). Dropped unconfirmed claims about async traits, #[double], Arc and Mutex sharing, wiremock and httpmock, and automock limits on complex generics.
