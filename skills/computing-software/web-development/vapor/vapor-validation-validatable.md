---
id: computing-software.web-development.vapor.vapor-validation-validatable
name: vapor-validation-validatable
category: computing-software
field: web-development
product: vapor
tags: [vapor,validatable,validators,validation,swift,request-validation]
level: practitioner
status: docs-checked
description: "Validate Vapor request content and query with Validatable, Validations.add, built-in validators, operators and custom failure messages."
sources:
  - https://docs.vapor.codes/basics/validation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reject bad request data with human-readable errors, reporting every failure at once, before decoding with Content.

Why: Codable stops at the first decode error with terse messages (for example for an invalid enum value); the Validation API reports all failures in one response and offers content checks (email, ranges, charsets).

## Method
1. Conform the Content type to `Validatable` (an extension works):
```swift
extension CreateUser: Validatable {
    static func validations(_ validations: inout Validations) {
        validations.add("email", as: String.self, is: .email)
    }
}
```
`add(key, as:, is:)`: key matches the property name, `as` is the expected type (usually, not always, the property type), then one or more validators.
2. Call before decoding: `try CreateUser.validate(content: req)`, then `req.content.decode(...)`. For query strings use `try CreateUser.validate(query: req)`.
3. Example validators: `.range(13...)` on Int, `!.empty`, `.count(3...) && .alphanumeric` on String.
4. Optional enum-like field: validate as String, since an invalid enum cannot be decoded:
```swift
validations.add("favoriteColor", as: String.self,
    is: .in("red", "blue", "green"), required: false)
```
A missing key passes with `required: false`, but explicit `null` fails. To allow null use `as: String?.self, is: .nil || .in("red", "blue", "green"), required: false`.
5. Custom message: pass `customFailureDescription: "Provided name is empty!"` to `add`.

Multiple failures are joined in one message, e.g. `age is less than minimum of 13, email is not a valid email address`.

## Built-in validators
`.ascii`, `.alphanumeric`, `.characterSet(_:)`, `.count(_:)`, `.email`, `.empty`, `.in(_:)`, `.nil`, `.range(_:)`, `.url`, `.custom(_:, validationClosure:)`.
Operators: `!` (invert), `&&` (both), `||` (either).

Related: computing-software.web-development.vapor.vapor-custom-validators

## Checked
Read the whole Validation page (vapor/docs, docs/4.0/basics/validation.md, source of the cited page) on 2026-11-08. Confirmed Validatable, `validations.add` parameters, `validate(content:)` and `validate(query:)`, the example validators, the optional enum and null handling, `customFailureDescription`, the combined error message, and both the validator and operator tables. No claims removed.
Method: docs-only read of cited pages, 2026-11-08
