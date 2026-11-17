---
id: computing-software.software-engineering.objective-c.string-formatting
name: string-formatting
category: computing-software
field: software-engineering
product: objective-c
tags: [objective-c, objc-foundation-text, string-formatting]
level: practitioner
status: draft
description: "Use correct printf-style specifiers for NSInteger, doubles, pointers and objects (%@, %ld, %lu, %p) and avoid format-string vulnerabilities."
sources:
  - https://developer.apple.com/documentation/foundation
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# String formatting
**Goal:** format correctly across 32/64-bit.

```objc
NSString *s = [NSString stringWithFormat:@"%@ has %ld items, %.2f total, ptr %p", name, (long)count, total, obj];
NSLog(@"%@", userInput);        // never NSLog(userInput)
```
- `%@` object (calls `description`), `%d` int, `%ld` long (use with NSInteger cast), `%lu` unsigned long (NSUInteger), `%lld`, `%f` double, `%g`, `%c`, `%s` C string, `%p` pointer, `%%` percent. `%zd`/`%zu` for ssize_t/size_t.
- Positional arguments allow reordering for localization: `@"%2$@ %1$@"`.
- Override `description` (and `debugDescription` for lldb `po`) in your classes to control `%@`.
- Format strings must be literals or `NS_FORMAT_ARGUMENT` annotated; compile with `-Wformat-security` to flag non-literal formats.
- Custom variadic helpers: `- (void)log:(NSString *)fmt, ... NS_FORMAT_FUNCTION(1,2);` and use `initWithFormat:arguments:` with `va_list`.
- Numbers for UI: `NSNumberFormatter`/`NSMeasurementFormatter`, not `%f`.

## Gotchas
- Passing user text as the format string allows `%n`-style crashes and leaks.
- `%d` with `NSInteger` is wrong on 64-bit.

## Self-check
Build with `-Wformat -Wformat-security` and confirm zero warnings.
