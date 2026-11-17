---
id: computing-software.software-engineering.c.format-string-vulnerabilities
name: format-string-vulnerabilities
category: computing-software
field: software-engineering
product: c
tags: [c, format-string-vulnerability, printf-user-input, wformat-security, percent-n]
level: advanced
status: docs-checked
description: "Recognise and eliminate format string vulnerabilities in printf, syslog and logging wrappers."
sources: ["https://man7.org/linux/man-pages/man3/printf.3.html", "https://man7.org/linux/man-pages/man3/syslog.3.html", "https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html", "https://gcc.gnu.org/onlinedocs/gcc-14.2.0/gcc/Common-Function-Attributes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Format string vulnerabilities

Goal: no attacker-controlled format strings.

- If an attacker controls the format, `%n` can write to memory (see printf(3)). Applies to `printf`, `fprintf`, `snprintf`, `syslog` and your own wrappers.
- Fix: always use a constant format: `printf("%s", s)`, `syslog(LOG_ERR, "%s", msg)`, `fputs(s, stdout)`.
- Annotate wrappers: `void log_msg(const char *fmt, ...) __attribute__((format(printf, 1, 2)));` so the compiler checks callers.
- Build with `-Wformat -Wformat-security -Werror=format-security`.

Verify: write `printf(argv[1])`, run with `%p.%p.%p` and confirm the warning at compile time and the leak at run time, then fix.

## Checked

- Date: 2026-11-02
- Confirmed: man7 printf(3) (`%n` from untrusted input writes to memory); syslog(3) takes a format string; GCC manual `-Wformat-security` (warns on `printf(foo)` with a non-literal format and no arguments) and `-Wformat=2`; GCC `format` function attribute. Removed: the `%x`/`%p` leak claim, `err`/`warn`, fortify behaviour on `%n`, distribution defaults and the gettext bullet (none stated in the sources read).
Method: documentation only; no commands were run.
