---
id: computing-software.software-engineering.objective-c.secure-input-handling
name: secure-input-handling
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-security, secure-input-handling]
level: practitioner
status: draft
description: "Defend against format-string, unarchiving, SQL, path traversal and URL-scheme injection when handling untrusted input."
sources:
  - https://developer.apple.com/documentation/security
  - https://developer.apple.com/documentation/foundation
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Secure input handling
**Goal:** treat external data as hostile.

- Format strings: never pass user text as the format (`NSLog(userString)`); use `NSLog(@"%@", userString)`; compile with `-Wformat-security`.
- Unarchiving: use `NSSecureCoding` and `unarchivedObjectOfClass:fromData:error:` with explicit classes; never `unarchiveObjectWithData:` on untrusted data.
- SQL (SQLite C API): bind parameters instead of string-building:
```objc
sqlite3_stmt *st; sqlite3_prepare_v2(db, "SELECT id FROM users WHERE name = ?", -1, &st, NULL);
sqlite3_bind_text(st, 1, name.UTF8String, -1, SQLITE_TRANSIENT);
```
- Paths: standardize and verify that a file path stays inside an expected directory (`[url URLByStandardizingPath]`, then prefix check) before reading or writing.
- URLs/deep links: validate scheme, host and parameters in `application:openURL:options:`; do not act on unvalidated parameters; prefer universal links.
- JSON/plist: type-check values (see nsjsonserialization); bound sizes.
- C buffers: use `snprintf`, `strlcpy`, length-checked `NSData` operations; build with ASan in tests; enable stack protector (default in clang) and `-D_FORTIFY_SOURCE=2` where appropriate.
- Pasteboard and web views: treat contents as untrusted; disable JavaScript where unnecessary (`WKWebViewConfiguration`).

## Gotchas
- `SQLITE_TRANSIENT` makes SQLite copy the string; `SQLITE_STATIC` requires it to outlive the statement.
- Client-side validation does not replace server validation.

## Self-check
Fuzz your URL handler with malformed schemes and long parameters under ASan.
