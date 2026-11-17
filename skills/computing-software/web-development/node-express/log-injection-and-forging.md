---
id: computing-software.web-development.node-express.log-injection-and-forging
name: log-injection-and-forging
category: computing-software
field: web-development
product: node-express
tags: [security-logging, log-injection, crlf-injection, log4shell, structured-logging]
level: practitioner
status: gated
description: "Preventing log injection and forging: CRLF in user input, structured JSON logging, encoding for log viewers, and lookup-style vulnerabilities like Log4Shell."
sources:
  - https://owasp.org/www-community/attacks/Log_Injection
  - https://cwe.mitre.org/data/definitions/117.html
  - https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
  - https://logging.apache.org/log4j/2.x/security.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Log injection and forging

## 1. Forging with newlines
```js
console.log(`Login failed for ${req.body.username}`);
// username = "bob\n2026-10-16T10:00:00Z INFO Login succeeded for admin"
```
Plain-text logs now show a fake success line, misleading investigators and log-based alerting. Variants: ANSI escape sequences that rewrite terminal output, `\r` overwrites, very long values truncating real fields.

## 2. Fix: structured logs
JSON loggers (pino, winston json, structlog; Serilog gated: unconfirmed, source is paywalled or blocked) put user data in escaped string fields - newlines become `\n` inside the value:
```js
logger.warn({ event: "authn_login_fail", username: req.body.username }, "login failed");
```
Never interpolate user input into the message template. If text logs are unavoidable, encode CR/LF and control characters: `s.replace(/[\r\n\u0000-\u001f\u007f\u2028\u2029]/g, c => `\\u${c.charCodeAt(0).toString(16).padStart(4, "0")}`)` and cap length.

## 3. Viewer-side injection
Logs rendered in web dashboards (custom admin pages, some SIEMs) can execute stored XSS from logged user agents/usernames. Escape on display; CSV exports need formula-injection protection.

## 4. Lookup/format-string bugs
- Log4Shell (CVE-2021-44228): Log4j 2 evaluated `${jndi:ldap://...}` in logged strings -> RCE. Patch to a current 2.x (first fix 2.15.0, follow-up CVEs fixed through 2.17.1); similar "lookup" features exist in other libraries - disable message lookups.
- Python `logging`: pass args, do not pre-format: `log.info("user %s", name)` (also avoids `%` errors); never use user input as the format string.
- Node `util.format`/`console.log` treat the first argument as a format string - `console.log(userInput, x)` with `%o` can mangle; keep user input out of the first argument.

## Verify
Unit test logging a value with `\n`, `\r`, ANSI `\u001b[2J` and `${jndi:...}`: output stays one line/one JSON record with the value escaped.

## Checked
Run on Windows with Node 24.22: pino and winston (JSON format) each kept a username with a newline, an ESC clear-screen sequence and `${jndi:...}` inside one JSON line with the control characters escaped; the control-character encoder in section 2 (built with `new RegExp`, covering U+2028 and U+2029, which cannot be typed literally inside a regex literal) encoded all of them; `util.format` consumes `%s`/`%d` from the following arguments, but with a single argument it leaves `%%` alone (`100%% sure`) and prints `%s` as is. Python `logging` with `log.info("user %s", name)` logged the newline raw (arguments are not escaped, so use a JSON formatter) and a pre-formatted message containing `100% bad` plus an argument printed a `--- Logging error ---` trace instead of raising; structlog's `JSONRenderer` escaped the newline and ESC. Apache's security page lists CVE-2021-44228 as fixed in log4j-core 2.15.0 (2.12.2 for Java 7, 2.3.1 for Java 6), with follow-ups CVE-2021-45046 (fixed 2.16.0) and CVE-2021-44832 (JDBC appender, 2.17.1 for Java 8); Log4Shell itself was not run (gated: unconfirmed, source is paywalled or blocked; no Java 11+ here). Serilog and SIEM viewers were not run (gated: unconfirmed, source is paywalled or blocked).
