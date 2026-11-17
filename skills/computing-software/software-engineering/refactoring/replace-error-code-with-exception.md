---
id: computing-software.software-engineering.refactoring.replace-error-code-with-exception
name: replace-error-code-with-exception
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, refactoring-apis, replace-error-code-with-exception, error-handling, exceptions, result-types, fowler-catalog]
level: practitioner
status: docs-checked
description: "Replace error-code returns with exceptions so failures cannot be silently ignored: steps, benefits, the goto-like misuse risk, and Rust's Result alternative."
sources:
  - https://refactoring.guru/replace-error-code-with-exception
  - https://doc.rust-lang.org/book/ch09-00-error-handling.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replace Error Code with Exception

**Smell:** `if (withdraw(amount) == -1) ...` - callers must check a special return value, and forgetting means the error passes silently.

## Before / after
```java
int withdraw(int amount) {
    if (amount > balance) return -1;
    balance -= amount; return 0;
}
// after
void withdraw(int amount) throws BalanceException {
    if (amount > balance) throw new BalanceException();
    balance -= amount;
}
```

## Mechanics
Do one error code at a time, so you keep the details in your head.
1. Find every call to the method and, instead of checking the code, wrap the call in try/catch.
2. Inside the method, throw an exception instead of returning the code.
3. Change the signature to declare the exception (a throws or @throws section).

## Benefits
- Removes many conditionals that check error codes; handlers separate normal and abnormal paths concisely.
- Exception classes can carry their own methods, holding part of the error handling.
- Unlike exceptions, error codes cannot be used in a constructor, which must return only the new object.

## Drawback
An exception handler can become a goto-like crutch. Do not use exceptions to manage execution flow; throw them only to signal an error or critical situation.

## Alternative
Rust has no exceptions: its book describes `Result<T, E>` for recoverable errors and the `panic!` macro for unrecoverable ones, and in many cases Rust requires you to acknowledge a possible error before the code compiles.

## Verify
- [ ] No caller compares the return value to the old error code.
- [ ] Each call site handles or declares the exception.

## Checked
2026-11-01. Confirmed against the Refactoring Guru page (steps, benefits, drawback) and the Rust book chapter 9 introduction (Result and panic!). Removed: claims about Go, Kotlin, F#, Swift and TypeScript error values, exception-type design advice, atomicity and boundary-translation advice, and the Replace Exception with Precheck note, which those pages do not state. The refactoring.com catalog page returns no text and is not cited.
Method: documentation only; no commands were run.
