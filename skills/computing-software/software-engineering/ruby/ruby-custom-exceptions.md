---
id: computing-software.software-engineering.ruby.ruby-custom-exceptions
name: ruby-custom-exceptions
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-errors, custom-exceptions]
level: practitioner
status: docs-checked
description: "Define an exception hierarchy per library inheriting from StandardError with useful data."
sources: ["https://docs.ruby-lang.org/en/master/Exception.html", "https://docs.ruby-lang.org/en/master/StandardError.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Custom exception classes
- Define your own errors as subclasses of `StandardError` (or a library base error class that itself inherits it); `Exception` carries a class, an optional message, optional backtrace and an optional `cause`.
- `message` is the human-readable text; the `Exception.exception` / `#exception` methods build or copy an exception; `full_message(highlight:, order:)` formats it for logs.
- Rescue the base class of your library to catch all its errors, and avoid matching on message text.
Verify: a caller can `rescue` the base class and catch every subclass.

## Checked
2026-11-02. Confirmed against: Exception page: hierarchy, message, cause, exception, full_message options. Removed or softened (not stated on those pages): initialize(msg, code:) example, attr_reader guidance.
Method: documentation only; no commands were run.
